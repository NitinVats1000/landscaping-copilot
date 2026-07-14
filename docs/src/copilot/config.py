"""Application configuration, loaded from environment / .env (never hardcoded)."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "AI Landscaping Copilot"
    database_url: str = (
        "postgresql+asyncpg://copilot:copilot_dev_pw@localhost:5432/copilot"
    )

    @field_validator("database_url")
    @classmethod
    def _normalize_db_url(cls, v: str) -> str:
        """
        Managed hosts (Render, Heroku) hand us a SYNC url. Our engine is async and
        needs the asyncpg driver. Normalize here, once, so nothing downstream cares.
        """
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql://", 1)
        if v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        # asyncpg does not understand libpq's ?sslmode=... param
        if "?" in v:
            base, _, query = v.partition("?")
            kept = [p for p in query.split("&") if not p.startswith("sslmode=")]
            v = base + ("?" + "&".join(kept) if kept else "")
        return v


settings = Settings()
