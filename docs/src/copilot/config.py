"""Application configuration, loaded from environment / .env (never hardcoded)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "AI Landscaping Copilot"
    database_url: str = (
        "postgresql+asyncpg://copilot:copilot_dev_pw@localhost:5432/copilot"
    )


settings = Settings()
