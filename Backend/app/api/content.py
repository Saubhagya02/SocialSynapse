# backend/app/api/content.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, logger
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.schemas.content import ContentCreate, ContentResponse
from app.services.ai_service import content_generator, trend_analyzer
from app.services.linkedin_service import linkedin_service
from app.services.scheduler import content_scheduler
from app.utils.auth import get_current_user
from app.models.user import User
from app.models.post import Post

router = APIRouter()

@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered LinkedIn content
    
    ⚠️ This is where the magic happens - AI generates content based on user input
    """
    try:
        # Build user profile for AI context
        user_profile = {
            "name": current_user.name,
            "title": current_user.title,
            "industry": current_user.industry,
            "skills": current_user.skills,
            "target_audience": current_user.target_audience,
            "brand_voice": current_user.brand_voice
        }
        
        # Get trending topics if not provided
        trends = None
        if request.include_trends:
            trends = await trend_analyzer.get_trending_topics(
                current_user.industry,
                timeframe="week"
            )
            trends = [t["topic_name"] for t in trends[:5]]
        
        # Generate content using AI
        generated = await content_generator.generate_content(
            user_profile=user_profile,
            content_type=request.content_type,
            topic=request.topic,
            tone=request.tone,
            industry_trends=trends
        )
        
        # Save to database
        post = Post(
            user_id=current_user.id,
            content=generated.content,
            content_type=generated.content_type,
            hashtags=generated.hashtags,
            scheduled_time=datetime.fromisoformat(generated.best_posting_time),
            status="draft"
        )
        db.add(post)
        db.commit()
        
        # Analyze virality potential in background
        background_tasks.add_task(
            analyze_virality,
            post.id,
            generated.content
        )
        
        return ContentResponse(
            id=str(post.id),
            content=generated.content,
            hashtags=generated.hashtags,
            content_type=generated.content_type,
            tone=generated.tone,
            estimated_engagement=generated.estimated_engagement,
            best_posting_time=generated.best_posting_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/variations")
async def generate_variations(
    content_id: str,
    num_variations: int = 3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate A/B testing variations of existing content
    
    ⚠️ Creates multiple versions for testing what works best
    """
    post = db.query(Post).filter(
        Post.id == content_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Content not found")
    
    variations = await content_generator.generate_variations(
        content=post.content,
        num_variations=num_variations
    )
    
    # Save variations
    for idx, variation in enumerate(variations):
        variant_post = Post(
            user_id=current_user.id,
            content=variation,
            content_type=post.content_type,
            hashtags=post.hashtags,
            parent_id=post.id,
            variant_label=f"Variation {idx + 1}",
            status="draft"
        )
        db.add(variant_post)
    
    db.commit()
    
    return {
        "variations": variations,
        "message": f"Generated {len(variations)} variations"
    }

@router.post("/schedule")
async def schedule_post(
    content_id: str,
    scheduled_time: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Schedule content for automated posting
    
    ⚠️ This sets up automatic posting at optimal times
    """
    post = db.query(Post).filter(
        Post.id == content_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # If no time specified, use AI-recommended time
    if not scheduled_time:
        scheduled_time = datetime.fromisoformat(post.best_posting_time)
    
    # Schedule the post
    job_id = content_scheduler.schedule_post(
        post_id=post.id,
        scheduled_time=scheduled_time,
        user_id=current_user.id
    )
    
    # Update post status
    post.status = "scheduled"
    post.scheduled_time = scheduled_time
    post.scheduler_job_id = job_id
    db.commit()
    
    return {
        "message": "Post scheduled successfully",
        "scheduled_time": scheduled_time.isoformat(),
        "job_id": job_id
    }

@router.post("/publish-now")
async def publish_now(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Publish content immediately to LinkedIn
    
    ⚠️ This posts directly to LinkedIn using the stored access token
    """
    post = db.query(Post).filter(
        Post.id == content_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if not current_user.linkedin_access_token:
        raise HTTPException(
            status_code=400,
            detail="LinkedIn account not connected"
        )
    
    # Publish to LinkedIn
    result = await linkedin_service.create_post(
        access_token=current_user.linkedin_access_token,
        user_id=current_user.linkedin_id,
        content=f"{post.content}\n\n{' '.join(['#' + tag for tag in post.hashtags])}"
    )
    
    if result["success"]:
        post.status = "published"
        post.published_at = datetime.utcnow()
        post.linkedin_post_id = result["post_id"]
        db.commit()
        
        return {
            "message": "Post published successfully",
            "post_id": result["post_id"]
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to publish: {result['error']}"
        )

@router.get("/trending-topics")
async def get_trending_topics(
    industry: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get trending topics for content ideas
    
    ⚠️ AI analyzes current trends in your industry
    """
    target_industry = industry or current_user.industry or "Technology"
    
    trends = await trend_analyzer.get_trending_topics(
        industry=target_industry,
        timeframe="week"
    )
    
    return {
        "industry": target_industry,
        "trends": trends,
        "generated_at": datetime.utcnow().isoformat()
    }

@router.get("/calendar")
async def get_content_calendar(
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get content calendar with scheduled posts
    
    ⚠️ Shows all scheduled content in a calendar view
    """
    posts = db.query(Post).filter(
        Post.user_id == current_user.id,
        Post.scheduled_time >= start_date,
        Post.scheduled_time <= end_date,
        Post.status.in_(["scheduled", "published"])
    ).all()
    
    calendar_data = []
    for post in posts:
        calendar_data.append({
            "id": str(post.id),
            "title": post.content[:50] + "...",
            "date": post.scheduled_time.isoformat(),
            "status": post.status,
            "content_type": post.content_type,
            "engagement_score": post.engagement_score
        })
    
    return {
        "calendar": calendar_data,
        "total_posts": len(calendar_data)
    }

@router.post("/optimize")
async def optimize_content(
    content_id: str,
    target_engagement_rate: float = 0.05,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Optimize content for better engagement
    
    ⚠️ AI analyzes and improves your content
    """
    post = db.query(Post).filter(
        Post.id == content_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Content not found")
    
    optimization = await content_generator.optimize_content(
        content=post.content,
        target_metrics={
            "engagement_rate": f"{target_engagement_rate * 100}%",
            "audience": current_user.target_audience
        }
    )
    
    return {
        "original_content": post.content,
        "optimizations": optimization,
        "recommendations": [
            "Add more emotional triggers",
            "Include industry statistics",
            "End with a question to boost comments",
            "Optimize hashtag selection"
        ]
    }

async def analyze_virality(post_id: str, content: str):
    """Background task to analyze viral potential"""
    try:
        score = await trend_analyzer.predict_virality(content)
        # Update post with virality score
        # This would update the database with the score
        logger.info(f"Post {post_id} virality score: {score}")
    except Exception as e:
        logger.error(f"Error analyzing virality: {e}")

# Additional endpoints for analytics, competitor analysis, etc...