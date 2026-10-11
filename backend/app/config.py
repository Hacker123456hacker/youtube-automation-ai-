import os
from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "YouTube Automation AI"
    APP_ENV: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://user:password@localhost/youtube_automation"
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "development-only-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)

    OPENAI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    YOUTUBE_CLIENT_ID: str = ""
    YOUTUBE_CLIENT_SECRET: str = ""

    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"]
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        # Pydantic Settings normally expects JSON for list-valued env vars.
        # Also accept a comma-separated string for simpler deployment platforms.
        if isinstance(value, str) and not value.lstrip().startswith("["):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.APP_ENV.lower() == "production":
            if self.DEBUG:
                raise ValueError("DEBUG must be false in production")
            if len(self.SECRET_KEY) < 32 or self.SECRET_KEY == "development-only-change-me":
                raise ValueError("Set a strong SECRET_KEY (at least 32 characters) in production")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
