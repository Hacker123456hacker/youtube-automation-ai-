from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.database import Base, engine
from app import models  # Register model tables before create_all.
from app.api.content import router as content_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.APP_ENV.lower() != "production":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered YouTube content automation platform",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(content_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to YouTube Automation AI",
        "version": "0.3.0",
        "docs": "/docs",
        "implemented": ["health checks", "AI script generation endpoint"],
        "not_yet_implemented": ["voice generation", "video rendering", "YouTube upload", "daily scheduler"],
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "app": settings.APP_NAME}


@app.get("/health/ready")
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is not ready") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
