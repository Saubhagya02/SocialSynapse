# backend/app/schemas/content.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class ContentTone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    HUMOROUS = "humorous"
    THOUGHT_PROVOKING = "thought_provoking"

class ContentCreate(BaseModel):
    topic: str = Field(..., description="Topic or idea for content")
    content_type: str = Field(..., description="Type of content to generate")
    tone: ContentTone = Field(ContentTone.PROFESSIONAL, description="Tone of content")
    include_hashtags: bool = Field(True, description="Include hashtags")
    include_emojis: bool = Field(False, description="Include emojis")
    target_length: Optional[int] = Field(1200, description="Target character count")
    include_trends: bool = Field(True, description="Include trending topics")
    creativity: float = Field(0.7, ge=0.3, le=1.0, description="Creativity level")

class ContentResponse(BaseModel):
    id: str
    content: str
    hashtags: List[str]
    content_type: str
    tone: str
    estimated_engagement: float
    best_posting_time: str
    virality_score: Optional[float] = None

class ContentOptimization(BaseModel):
    original_content: str
    optimized_content: str
    improvements: List[str]
    predicted_engagement_increase: float

class TrendingTopic(BaseModel):
    topic: str
    relevance_score: float
    suggested_angles: List[str]
    best_content_type: str