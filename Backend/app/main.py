# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.models import user, post, analytics
from app.database import engine, Base
from contextlib import asynccontextmanager
import logging
from typing import Any, Dict

# Import routers to register API endpoints
from app.api import analytics, users, content, auth, health

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting LinkedIn AI Agent...")
    yield
    # Shutdown
    logger.info("Shutting down LinkedIn AI Agent...")


# Create FastAPI app
app = FastAPI(
    title="LinkedIn AI Agent",
    version="1.0.0",
    description="AI-powered LinkedIn Personal Branding Agent",
    lifespan=lifespan
)

# Register routers for API endpoints
app.include_router(analytics.router, prefix="/api/analytics")
app.include_router(users.router, prefix="/api/users")
app.include_router(content.router, prefix="/api/content")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(health.router, prefix="/api/health") 

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint"""
    return {
        "name": "LinkedIn AI Agent",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )