# backend/app/config.py
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "LinkedIn AI Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    SCHEDULER_TIMEZONE: str = "UTC"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/linkedin_ai_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Gemini - ADD YOUR KEY HERE
    GEMINI_API_KEY: str = "AIzaSyCAiv7EC6ScT3bfoOS_mNd6HNQsPcog_48"
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_TEMPERATURE: float = 0.7
    
    # LinkedIn OAuth - ADD YOUR CREDENTIALS HERE
    LINKEDIN_CLIENT_ID: str = "86l5fcyc8v5evw"
    LINKEDIN_CLIENT_SECRET: str = "WPL_AP1.illIVNcL7Gx1qhPZ.g8oq7w=="
    LINKEDIN_REDIRECT_URI: str = "http://localhost:8000/api/auth/linkedin/callback"
    LINKEDIN_SCOPE: str = "r_liteprofile,r_emailaddress,w_member_social"
    
    # JWT
    SECRET_KEY: str = "IwIE6N0YOVZkxUQzL2pIAVtodXIyLheVRBysAlda43c"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()