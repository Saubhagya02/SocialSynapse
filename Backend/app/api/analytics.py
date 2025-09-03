# backend/app/api/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.models.analytics import Analytics
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    # Get posts count
    total_posts = db.query(func.count(Post.id)).filter(
        Post.user_id == current_user.id,
        Post.status == "published"
    ).scalar()
    
    # Get engagement metrics
    engagement_stats = db.query(
        func.sum(Post.likes).label("total_likes"),
        func.sum(Post.comments).label("total_comments"),
        func.sum(Post.shares).label("total_shares"),
        func.sum(Post.views).label("total_views"),
        func.avg(Post.engagement_rate).label("avg_engagement_rate")
    ).filter(Post.user_id == current_user.id).first()
    
    # Get recent posts performance
    recent_posts = db.query(Post).filter(
        Post.user_id == current_user.id,
        Post.status == "published"
    ).order_by(Post.published_at.desc()).limit(5).all()
    
    # Calculate growth metrics (mock data for now)
    growth_rate = 12.5  # Percentage
    viral_posts = db.query(func.count(Post.id)).filter(
        Post.user_id == current_user.id,
        Post.virality_score > 0.7
    ).scalar()
    
    # Get scheduled posts count
    scheduled_posts = db.query(func.count(Post.id)).filter(
        Post.user_id == current_user.id,
        Post.status == "scheduled"
    ).scalar()
    
    return {
        "totalPosts": total_posts or 0,
        "totalEngagement": (engagement_stats.total_likes or 0) + 
                          (engagement_stats.total_comments or 0) + 
                          (engagement_stats.total_shares or 0),
        "profileViews": engagement_stats.total_views or 0,
        "avgEngagementRate": float(engagement_stats.avg_engagement_rate or 0),
        "connectionGrowth": growth_rate,
        "viralPosts": viral_posts or 0,
        "scheduledPosts": scheduled_posts or 0,
        "recentPosts": [
            {
                "id": str(post.id),
                "content": post.content[:100] + "...",
                "engagement_rate": post.engagement_rate,
                "published_at": post.published_at.isoformat() if post.published_at else None
            }
            for post in recent_posts
        ]
    }

@router.get("/posts/{post_id}/analytics")
async def get_post_analytics(
    post_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed analytics for a specific post"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get analytics data
    analytics = db.query(Analytics).filter(
        Analytics.post_id == post_id
    ).order_by(Analytics.recorded_at.desc()).first()
    
    if not analytics:
        # Return post basic metrics if no detailed analytics
        return {
            "post_id": str(post.id),
            "content_preview": post.content[:200],
            "metrics": {
                "views": post.views,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "engagement_rate": post.engagement_rate,
                "virality_score": post.virality_score
            },
            "published_at": post.published_at.isoformat() if post.published_at else None
        }
    
    return {
        "post_id": str(post.id),
        "content_preview": post.content[:200],
        "metrics": {
            "impressions": analytics.impressions,
            "clicks": analytics.clicks,
            "likes": analytics.likes,
            "comments": analytics.comments,
            "shares": analytics.shares,
            "saves": analytics.saves,
            "engagement_rate": analytics.engagement_rate,
            "click_through_rate": analytics.click_through_rate,
            "virality_score": analytics.virality_score
        },
        "audience_insights": analytics.audience_demographics,
        "peak_engagement_time": analytics.peak_engagement_time.isoformat() if analytics.peak_engagement_time else None,
        "recorded_at": analytics.recorded_at.isoformat()
    }

@router.get("/trends")
async def get_engagement_trends(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get engagement trends over time"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get daily engagement data
    daily_stats = db.query(
        func.date(Post.published_at).label("date"),
        func.sum(Post.likes).label("likes"),
        func.sum(Post.comments).label("comments"),
        func.sum(Post.shares).label("shares"),
        func.avg(Post.engagement_rate).label("avg_engagement")
    ).filter(
        Post.user_id == current_user.id,
        Post.published_at >= start_date,
        Post.status == "published"
    ).group_by(func.date(Post.published_at)).all()
    
    return {
        "period": f"Last {days} days",
        "trends": [
            {
                "date": stat.date.isoformat() if stat.date else None,
                "likes": stat.likes or 0,
                "comments": stat.comments or 0,
                "shares": stat.shares or 0,
                "engagement_rate": float(stat.avg_engagement or 0)
            }
            for stat in daily_stats
        ]
    }

@router.get("/top-content")
async def get_top_performing_content(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get top performing content"""
    top_posts = db.query(Post).filter(
        Post.user_id == current_user.id,
        Post.status == "published"
    ).order_by(Post.engagement_rate.desc()).limit(limit).all()
    
    return {
        "top_posts": [
            {
                "id": str(post.id),
                "content_preview": post.content[:200] + "...",
                "content_type": post.content_type,
                "engagement_rate": post.engagement_rate,
                "virality_score": post.virality_score,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "published_at": post.published_at.isoformat() if post.published_at else None
            }
            for post in top_posts
        ]
    }