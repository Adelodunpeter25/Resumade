from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.resume_analytics import ResumeAnalytics
from app.schemas.response import APIResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/resume/{resume_id}", response_model=APIResponse[Dict[str, Any]])
def get_resume_analytics(
    resume_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics for a specific resume"""
    # Verify ownership
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total views and downloads
    total_views = db.query(func.count(ResumeAnalytics.id)).filter(
        ResumeAnalytics.resume_id == resume_id,
        ResumeAnalytics.event_type == 'view',
        ResumeAnalytics.created_at >= start_date
    ).scalar()
    
    total_downloads = db.query(func.count(ResumeAnalytics.id)).filter(
        ResumeAnalytics.resume_id == resume_id,
        ResumeAnalytics.event_type == 'download',
        ResumeAnalytics.created_at >= start_date
    ).scalar()
    
    # Views by day
    views_by_day = db.query(
        func.date(ResumeAnalytics.created_at).label('date'),
        func.count(ResumeAnalytics.id).label('count')
    ).filter(
        ResumeAnalytics.resume_id == resume_id,
        ResumeAnalytics.event_type == 'view',
        ResumeAnalytics.created_at >= start_date
    ).group_by(func.date(ResumeAnalytics.created_at)).order_by(desc('date')).all()
    
    # Recent activity
    recent_activity = db.query(ResumeAnalytics).filter(
        ResumeAnalytics.resume_id == resume_id,
        ResumeAnalytics.created_at >= start_date
    ).order_by(desc(ResumeAnalytics.created_at)).limit(50).all()
    
    return APIResponse(
        success=True,
        data={
            "total_views": total_views or 0,
            "total_downloads": total_downloads or 0,
            "views_by_day": [{"date": str(v.date), "count": v.count} for v in views_by_day],
            "recent_activity": [
                {
                    "event_type": a.event_type,
                    "created_at": a.created_at.isoformat(),
                    "ip_address": a.ip_address
                }
                for a in recent_activity
            ]
        }
    )

@router.get("/dashboard", response_model=APIResponse[Dict[str, Any]])
def get_dashboard_analytics(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall analytics for user's resumes"""
    # Get user's resume IDs
    resume_ids = [r.id for r in db.query(Resume.id).filter(Resume.user_id == current_user.id).all()]
    
    if not resume_ids:
        return APIResponse(
            success=True,
            data={
                "total_views": 0,
                "total_downloads": 0,
                "top_resumes": []
            }
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total views and downloads
    total_views = db.query(func.count(ResumeAnalytics.id)).filter(
        ResumeAnalytics.resume_id.in_(resume_ids),
        ResumeAnalytics.event_type == 'view',
        ResumeAnalytics.created_at >= start_date
    ).scalar()
    
    total_downloads = db.query(func.count(ResumeAnalytics.id)).filter(
        ResumeAnalytics.resume_id.in_(resume_ids),
        ResumeAnalytics.event_type == 'download',
        ResumeAnalytics.created_at >= start_date
    ).scalar()
    
    # Top resumes by views
    top_resumes = db.query(
        Resume.id,
        Resume.title,
        func.count(ResumeAnalytics.id).label('views')
    ).join(
        ResumeAnalytics, Resume.id == ResumeAnalytics.resume_id
    ).filter(
        Resume.user_id == current_user.id,
        ResumeAnalytics.event_type == 'view',
        ResumeAnalytics.created_at >= start_date
    ).group_by(Resume.id, Resume.title).order_by(desc('views')).limit(5).all()
    
    return APIResponse(
        success=True,
        data={
            "total_views": total_views or 0,
            "total_downloads": total_downloads or 0,
            "top_resumes": [
                {"id": r.id, "title": r.title, "views": r.views}
                for r in top_resumes
            ]
        }
    )
