from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    channels = relationship("Channel", back_populates="user", cascade="all, delete-orphan")
    content = relationship("Content", back_populates="user", cascade="all, delete-orphan")

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_id = Column(String(255), unique=True, index=True, nullable=False)
    channel_name = Column(String(255), nullable=False)
    description = Column(Text)
    subscriber_count = Column(Integer, default=0)
    is_connected = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="channels")
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    topic = Column(String(255))
    script = Column(Text)
    keywords = Column(JSON)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="content")
    video = relationship("Video", uselist=False, back_populates="content")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"))
    youtube_video_id = Column(String(255), unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="draft")
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    channel = relationship("Channel", back_populates="videos")
    content = relationship("Content", back_populates="video")
