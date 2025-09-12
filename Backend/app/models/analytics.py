# backend/app/models/analytics.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, default=0.0)
    click_through_rate = Column(Float, default=0.0)
    virality_score = Column(Float, default=0.0)
    
    # Audience insights
    audience_demographics = Column(JSON)
    peak_engagement_time = Column(DateTime)
    
    # Timestamps
    recorded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)