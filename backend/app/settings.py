from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@postgres:5432/intelliagent_db"
    REDIS_URL: str = "redis://intelliagent-redis:6379/0"

    # LangSmith Tracing
    LANGCHAIN_TRACING_V2: bool = True
    LANGSMITH_ENDPOINT: str ="https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str
    LANGCHAIN_PROJECT: str ="IntelliAgent"

    # JWT Settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
