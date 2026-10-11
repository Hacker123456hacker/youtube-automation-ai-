from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Basic syntax check keeps the API importable without Pydantic's optional
# email-validator package. For full RFC validation, add email-validator.
EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"


class UserBase(BaseModel):
    email: str = Field(..., max_length=255, pattern=EMAIL_PATTERN)
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=255, pattern=EMAIL_PATTERN)
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class ChannelResponse(BaseModel):
    id: int
    channel_id: str
    channel_name: str
    subscriber_count: int
    is_connected: bool

    class Config:
        from_attributes = True


class ContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    topic: str = Field(..., min_length=1, max_length=255)
    keywords: Optional[list[str]] = None


class ContentResponse(ContentCreate):
    id: int
    script: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
