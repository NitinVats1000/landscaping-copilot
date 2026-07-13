"""FastAPI application entrypoint."""

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from copilot.db import get_session
from copilot.routes import router as projects_router

app = FastAPI(title="AI Landscaping Copilot", version="0.1.0")

app.include_router(projects_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/health/db")
async def health_db(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    """Readiness probe: can we reach the database?"""
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
