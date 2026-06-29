"""Database engine and session management (SQLAlchemy 2.0 async)."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from copilot.config import settings

# pool_pre_ping checks a connection is alive before using it (avoids stale-conn errors)
engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields a session, always closes it afterwards."""
    async with SessionLocal() as session:
        yield session
