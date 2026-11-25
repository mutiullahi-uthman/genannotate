from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "GenAnnotate"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = Field(...)

    REDIS_URL: str = Field(...)

    FIREBASE_PROJECT_ID: str = Field(...)
    FIREBASE_CLIENT_EMAIL: str = Field(...)
    FIREBASE_PRIVATE_KEY: str = Field(...)

    GCS_BUCKET_NAME: str = Field(...)

    JWT_ALGORITHM: str = "RS256"

    CELERY_BROKER_URL: str = Field(...)
    CELERY_RESULT_BACKEND: str = Field(...)

    DEFAULT_PAGE_SIZE: int = 25
    MAX_PAGE_SIZE: int = 200

    RECORD_LOCK_MINUTES: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()