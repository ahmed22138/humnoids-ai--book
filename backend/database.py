"""
Database configuration and session management
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Test connection before using
    connect_args={
        "connect_timeout": 10,
        "application_name": settings.app_name,
    }
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency injection for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from models.user import User, Profile
    from models.chat import ChatMessage
    from models.translation import Translation
    from models.agent import SubagentInvocation

    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")


if __name__ == "__main__":
    init_db()
