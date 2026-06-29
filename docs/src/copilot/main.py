"""FastAPI application entrypoint."""

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from copilot.db import get_session

app = FastAPI(title="AI Landscaping Copilot", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: is the service process up?"""
    return {"status": "ok"}


@app.get("/health/db")
async def health_db(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    """Readiness probe: can the service actually reach the database?"""
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
