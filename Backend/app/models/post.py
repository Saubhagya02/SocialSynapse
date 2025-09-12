# backend/app/models/post.py
from sqlalchemy import Column, String, Text, DateTime, Float, JSON, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    content_type = Column(String, nullable=False)
    hashtags = Column(JSON, default=list)
    media_urls = Column(JSON, default=list)
    
    # Scheduling
    status = Column(String, default="draft")
    scheduled_time = Column(DateTime)
    published_at = Column(DateTime)
    scheduler_job_id = Column(String)
    
    # LinkedIn
    linkedin_post_id = Column(String)
    
    # Analytics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    virality_score = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)