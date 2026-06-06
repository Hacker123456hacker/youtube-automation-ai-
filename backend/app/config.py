from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "YouTube Automation AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    DATABASE_URL: str = "postgresql://user:password@localhost/youtube_automation"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    OPENAI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    YOUTUBE_CLIENT_ID: str = ""
    YOUTUBE_CLIENT_SECRET: str = ""
    
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
