# backend/app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.utils.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    get_current_user
)
from app.services.linkedin_service import linkedin_service
from app.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        title=user_data.title,
        industry=user_data.industry,
        skills=user_data.skills,
        target_audience=user_data.target_audience,
        brand_voice=user_data.brand_voice,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/linkedin")
async def linkedin_auth(request: Request):
    """Initiate LinkedIn OAuth flow"""
    state = str(uuid.uuid4())
    # Store state in session or cache for verification
    authorization_url = linkedin_service.get_authorization_url(state)
    return RedirectResponse(url=authorization_url)

@router.get("/linkedin/callback")
async def linkedin_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle LinkedIn OAuth callback"""
    try:
        # Exchange code for token
        token_data = await linkedin_service.exchange_code_for_token(code)
        
        # Get user profile from LinkedIn
        linkedin_profile = await linkedin_service.get_user_profile(token_data['access_token'])
        
        # Update user with LinkedIn data
        current_user.linkedin_id = linkedin_profile['id']
        current_user.linkedin_access_token = token_data['access_token']
        current_user.linkedin_refresh_token = token_data.get('refresh_token')
        
        db.commit()
        
        return {
            "message": "LinkedIn account connected successfully",
            "linkedin_profile": linkedin_profile
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to connect LinkedIn: {str(e)}"
        )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user"""
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user