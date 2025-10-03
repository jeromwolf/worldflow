"""
Database Connection Manager - Async SQLAlchemy
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from .config import settings
import os

# Debug: Print environment variables
print(f"[DEBUG] DATABASE_URL from settings: {settings.DATABASE_URL}")
print(f"[DEBUG] DATABASE_URL from os.getenv: {os.getenv('DATABASE_URL')}")
print(f"[DEBUG] All env vars containing 'DATABASE': {[k for k in os.environ.keys() if 'DATABASE' in k]}")

# Database URL - must be provided via environment variable
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required but not set!")

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database - create all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connection"""
    await engine.dispose()
