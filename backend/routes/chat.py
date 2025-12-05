"""
Chat endpoint for RAG-powered chatbot
Handles query requests and returns responses with sources
"""
import time
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import settings
from models.chat import ChatMessage
from services.rag_service import RAGService, RAGCacheService
from database import get_db

logger = logging.getLogger(__name__)

# Initialize RAG service
rag_service = RAGService(
    openai_api_key=settings.openai_api_key,
    qdrant_url=settings.qdrant_url
)
cache_service = RAGCacheService(ttl_seconds=3600)  # 1 hour cache

router = APIRouter(prefix="/chat", tags=["Chatbot"])


class ChatQueryRequest(BaseModel):
    """Chat query request schema"""
    query: str
    selected_text: Optional[str] = None
    chapter: Optional[str] = None


class SourceInfo(BaseModel):
    """Information about source material"""
    content: str
    source: str
    chapter_id: str
    similarity_score: float


class ChatResponse(BaseModel):
    """Chat response schema"""
    response: str
    sources: list[SourceInfo]
    confidence: float
    response_time_ms: int
    tokens_used: int
    feedback_id: Optional[str] = None  # For user feedback tracking


@router.post("/", response_model=ChatResponse)
async def query_chatbot(
    request: ChatQueryRequest,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """
    Process chat query with RAG

    Query parameters:
    - query: The user's question
    - selected_text: Optional text the user selected from course
    - chapter: Optional specific chapter to focus on

    Returns:
    - response: Generated answer with source citations
    - sources: List of retrieved source materials
    - confidence: Confidence score (0-1) in the response
    - tokens_used: Approximate token count
    - feedback_id: ID for collecting user feedback on response quality
    """

    try:
        start_time = time.time()

        # Validate input
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )

        # Check cache
        cache_key = cache_service.get_cache_key(
            request.query,
            request.selected_text,
            request.chapter
        )
        cached_response = cache_service.get(cache_key)

        if cached_response:
            logger.info(f"Cache hit for query: {request.query[:50]}")
            return ChatResponse(**cached_response)

        # Generate response using RAG
        logger.info(f"Processing query: {request.query[:50]}")

        rag_result = rag_service.query(
            user_query=request.query,
            selected_text=request.selected_text,
            chapter=request.chapter,
            top_k=3
        )

        response_time = int((time.time() - start_time) * 1000)

        # Format sources
        sources = [
            SourceInfo(
                content=s["content"],
                source=s["source"],
                chapter_id=s["chapter_id"],
                similarity_score=s["similarity_score"]
            )
            for s in rag_result["sources"]
        ]

        # Create response
        chat_response = ChatResponse(
            response=rag_result["response"],
            sources=sources,
            confidence=rag_result["confidence"],
            response_time_ms=response_time,
            tokens_used=rag_result["tokens_used"],
            feedback_id=None
        )

        # Store in database for analytics
        try:
            chat_message = ChatMessage(
                user_id=user_id,
                query=request.query,
                selected_text=request.selected_text,
                chapter=request.chapter,
                response=rag_result["response"],
                sources=[s.dict() for s in sources],
                confidence=rag_result["confidence"],
                response_time_ms=response_time,
                tokens_used=rag_result["tokens_used"]
            )
            db.add(chat_message)
            db.commit()

            # Set feedback ID for later user feedback
            chat_response.feedback_id = str(chat_message.id)
        except Exception as e:
            logger.error(f"Error storing chat message: {e}")
            db.rollback()

        # Cache response
        cache_service.set(cache_key, chat_response.dict())

        logger.info(f"Query processed in {response_time}ms")
        return chat_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat query: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error processing your question. Please try again."
        )


@router.post("/feedback")
async def submit_feedback(
    feedback_id: str,
    feedback: str,  # 'helpful' or 'not_helpful'
    db: Session = Depends(get_db)
):
    """
    Submit feedback on chatbot response quality
    Helps improve the system over time
    """

    try:
        # Validate feedback
        if feedback not in ['helpful', 'not_helpful', 'partially_helpful']:
            raise HTTPException(
                status_code=400,
                detail="Invalid feedback type"
            )

        # Update chat message with feedback
        chat_message = db.query(ChatMessage).filter(
            ChatMessage.id == feedback_id
        ).first()

        if not chat_message:
            raise HTTPException(
                status_code=404,
                detail="Chat message not found"
            )

        chat_message.feedback = feedback
        db.commit()

        logger.info(f"Feedback recorded: {feedback} for message {feedback_id}")

        return {
            "status": "success",
            "message": "Thank you for your feedback!"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error recording feedback"
        )


@router.post("/index-chapter")
async def index_chapter_content(
    chapter_id: str,
    title: str,
    content: str
):
    """
    Index chapter content into Qdrant for RAG
    Called during content deployment

    Access control: Should be restricted to admin/deployment service
    """

    try:
        logger.info(f"Indexing chapter: {chapter_id}")

        # Index content
        chunks_indexed = rag_service.index_chapter(chapter_id, title, content)

        return {
            "status": "success",
            "chapter_id": chapter_id,
            "chunks_indexed": chunks_indexed,
            "message": f"Successfully indexed {chunks_indexed} chunks"
        }

    except Exception as e:
        logger.error(f"Error indexing chapter: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error indexing chapter content"
        )


@router.get("/stats")
async def get_chat_stats(db: Session = Depends(get_db)):
    """
    Get statistics on chatbot usage
    For monitoring and improvement
    """

    try:
        total_queries = db.query(ChatMessage).count()

        helpful = db.query(ChatMessage).filter(
            ChatMessage.feedback == 'helpful'
        ).count()

        not_helpful = db.query(ChatMessage).filter(
            ChatMessage.feedback == 'not_helpful'
        ).count()

        avg_confidence = db.query(
            ChatMessage
        ).select_from(ChatMessage).average(ChatMessage.confidence) or 0.0

        avg_response_time = db.query(
            ChatMessage
        ).select_from(ChatMessage).average(
            ChatMessage.response_time_ms
        ) or 0.0

        return {
            "total_queries": total_queries,
            "feedback_helpful": helpful,
            "feedback_not_helpful": not_helpful,
            "feedback_rate": helpful / (helpful + not_helpful) if (
                helpful + not_helpful
            ) > 0 else 0,
            "average_confidence": float(avg_confidence),
            "average_response_time_ms": float(avg_response_time)
        }

    except Exception as e:
        logger.error(f"Error getting chat stats: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving statistics"
        )
