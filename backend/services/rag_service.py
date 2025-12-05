"""
RAG (Retrieval-Augmented Generation) Service
Combines semantic search with LLM responses for intelligent chatbot
"""
import logging
from typing import List, Dict, Optional, Tuple
import numpy as np
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

logger = logging.getLogger(__name__)


class RAGService:
    """Retrieval-Augmented Generation service for chatbot"""

    def __init__(self, openai_api_key: str, qdrant_url: str):
        """Initialize RAG service with OpenAI and Qdrant"""
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.qdrant_client = QdrantClient(url=qdrant_url)

        self.embedding_model = "text-embedding-3-small"
        self.llm_model = "gpt-4-turbo"
        self.collection_name = "ai_textbook"

        # Initialize Qdrant collection if needed
        self._initialize_collection()

    def _initialize_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} exists")
        except:
            logger.info(f"Creating collection {self.collection_name}")
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE
                )
            )

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            raise

    def index_chapter(self, chapter_id: str, title: str, content: str) -> int:
        """
        Index a chapter into Qdrant for semantic search
        Split content into chunks and embed each chunk
        """
        # Split content into chunks (roughly 500 characters each)
        chunks = self._split_content(content, chunk_size=500, overlap=100)

        points = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{chapter_id}_chunk_{i}"

            # Embed chunk
            embedding = self.embed_text(chunk)

            # Create point with metadata
            point = PointStruct(
                id=hash(chunk_id) % (2**31),  # Positive hash
                vector=embedding,
                payload={
                    "chapter_id": chapter_id,
                    "title": title,
                    "chunk_index": i,
                    "content": chunk,
                    "source": f"{title} - Section {i+1}"
                }
            )
            points.append(point)

        # Upsert to Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        logger.info(f"Indexed {len(points)} chunks for chapter {chapter_id}")
        return len(points)

    def retrieve_relevant_content(
        self,
        query: str,
        top_k: int = 3
    ) -> List[Dict[str, str]]:
        """
        Retrieve relevant content chunks from Qdrant based on query
        Returns top_k most similar chunks
        """
        # Embed query
        query_embedding = self.embed_text(query)

        # Search Qdrant
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            score_threshold=0.5  # Minimum similarity score
        )

        # Extract relevant content
        sources = []
        for result in results:
            sources.append({
                "content": result.payload.get("content", ""),
                "source": result.payload.get("source", ""),
                "chapter_id": result.payload.get("chapter_id", ""),
                "similarity_score": result.score
            })

        return sources

    def generate_response(
        self,
        query: str,
        context: List[Dict[str, str]],
        selected_text: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Generate LLM response using retrieved context
        Returns: (response_text, confidence_score)
        """

        # Build context string
        context_str = self._format_context(context)

        # Build prompt
        system_prompt = """You are an expert tutor for Physical AI & Humanoid Robotics.
Your role is to provide accurate, clear, and educational responses based on the course material provided.
Always cite the source when using specific information."""

        if selected_text:
            user_prompt = f"""The student has selected this text from the course:
"${selected_text}"

They asked: {query}

Based on the relevant course material below, provide a detailed explanation:

RELEVANT MATERIAL:
{context_str}

Please provide a clear, educational response that helps the student understand the concept."""
        else:
            user_prompt = f"""A student asked the following question about Physical AI & Humanoid Robotics:

Question: {query}

Based on the relevant course material below, provide a detailed explanation:

RELEVANT MATERIAL:
{context_str}

Please provide a clear, educational response that helps the student understand the concept."""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.llm_model,
                temperature=0.7,
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            response_text = response.choices[0].message.content

            # Calculate confidence based on context quality
            confidence = self._calculate_confidence(context)

            return response_text, confidence

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def query(
        self,
        user_query: str,
        selected_text: Optional[str] = None,
        chapter: Optional[str] = None,
        top_k: int = 3
    ) -> Dict[str, any]:
        """
        Complete RAG pipeline: retrieve + generate
        Returns response with sources and metadata
        """

        # Retrieve relevant content
        sources = self.retrieve_relevant_content(user_query, top_k=top_k)

        if not sources:
            return {
                "response": "I couldn't find relevant information to answer your question. "
                           "Please try rephrasing or ask a different question.",
                "sources": [],
                "confidence": 0.0,
                "response_time_ms": 0,
                "tokens_used": 0
            }

        # Generate response using context
        response_text, confidence = self.generate_response(
            user_query,
            sources,
            selected_text
        )

        return {
            "response": response_text,
            "sources": sources,
            "confidence": confidence,
            "response_time_ms": 0,  # Would measure actual time
            "tokens_used": self._estimate_tokens(response_text)
        }

    def _split_content(
        self,
        content: str,
        chunk_size: int = 500,
        overlap: int = 100
    ) -> List[str]:
        """Split content into overlapping chunks"""
        chunks = []
        start = 0

        while start < len(content):
            end = min(start + chunk_size, len(content))

            # Try to split at sentence boundary
            if end < len(content):
                # Find last period before chunk end
                last_period = content.rfind(".", start, end)
                if last_period > start + chunk_size // 2:
                    end = last_period + 1

            chunks.append(content[start:end].strip())

            # Move start for next chunk (with overlap)
            start = end - overlap

        return chunks

    def _format_context(self, sources: List[Dict[str, str]]) -> str:
        """Format retrieved sources into context string"""
        context_parts = []

        for i, source in enumerate(sources, 1):
            context_parts.append(
                f"Source {i} ({source['source']}):\n"
                f"{source['content']}\n"
                f"(Similarity: {source['similarity_score']:.2%})\n"
            )

        return "\n".join(context_parts)

    def _calculate_confidence(self, sources: List[Dict[str, str]]) -> float:
        """
        Calculate confidence score based on retrieval quality
        Returns value between 0 and 1
        """
        if not sources:
            return 0.0

        # Average similarity scores
        avg_similarity = np.mean([s.get("similarity_score", 0) for s in sources])

        # Adjust for number of sources (more sources = higher confidence)
        source_factor = min(len(sources) / 3, 1.0)

        # Combine factors
        confidence = (avg_similarity * 0.7 + source_factor * 0.3)

        return min(confidence, 1.0)

    def _estimate_tokens(self, text: str) -> int:
        """Rough estimate of tokens (1 token ≈ 4 characters)"""
        return len(text) // 4


class RAGCacheService:
    """Cache for RAG responses to reduce API calls"""

    def __init__(self, ttl_seconds: int = 86400):  # 24 hours default
        """Initialize cache with TTL"""
        self.cache = {}
        self.ttl = ttl_seconds

    def get_cache_key(
        self,
        query: str,
        selected_text: Optional[str] = None,
        chapter: Optional[str] = None
    ) -> str:
        """Generate cache key from query parameters"""
        import hashlib
        key_str = f"{query}:{selected_text}:{chapter}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, cache_key: str) -> Optional[Dict]:
        """Get cached response if exists and not expired"""
        import time

        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["response"]
            else:
                del self.cache[cache_key]

        return None

    def set(self, cache_key: str, response: Dict) -> None:
        """Store response in cache"""
        import time
        self.cache[cache_key] = {
            "response": response,
            "timestamp": time.time()
        }
