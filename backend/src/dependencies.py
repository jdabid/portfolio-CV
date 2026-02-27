"""Shared FastAPI dependencies for dependency injection."""

from collections.abc import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.shared.database import AsyncSessionLocal
from src.shared.redis_client import get_redis


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_redis_client() -> Redis:
    """Provide a Redis client."""
    return get_redis()


def get_settings():
    """Provide application settings."""
    return settings
