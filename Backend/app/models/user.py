# backend/app/models/user.py
from sqlalchemy import Column, String, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    title = Column(String)
    industry = Column(String)
    skills = Column(JSON, default=list)
    target_audience = Column(String)
    brand_voice = Column(String)
    
    # LinkedIn OAuth
    linkedin_id = Column(String, unique=True, index=True)
    linkedin_access_token = Column(String)
    linkedin_refresh_token = Column(String)
    linkedin_token_expires_at = Column(DateTime)
    
    # Account details
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)