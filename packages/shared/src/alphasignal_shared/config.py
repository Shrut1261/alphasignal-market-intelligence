from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings shared by services."""

    app_env: str = Field(default="local", validation_alias="APP_ENV")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    database_url: str = Field(
        default="postgresql+asyncpg://alphasignal:alphasignal@localhost:5432/alphasignal",
        validation_alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    jwt_secret_key: str = Field(
        default="replace-me-for-local-dev",
        validation_alias="JWT_SECRET_KEY",
    )
    news_api_key: str | None = Field(default=None, validation_alias="NEWS_API_KEY")
    fred_api_key: str | None = Field(default=None, validation_alias="FRED_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
