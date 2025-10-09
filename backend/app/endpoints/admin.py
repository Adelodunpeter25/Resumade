from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import User, Resume, ShareLink
from app.schemas.response import APIResponse

router = APIRouter(prefix="/admin", tags=["Admin"])

def is_admin(current_user: User = Depends(get_current_user)):
    """Check if user is admin (extend this with proper role checking)"""
    # TODO: Add proper admin role checking
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin)
):
    """Get admin dashboard statistics"""
    
    # User stats
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    # Resume stats
    total_resumes = db.query(func.count(Resume.id)).scalar()
    total_views = db.query(func.sum(Resume.views)).scalar() or 0
    total_downloads = db.query(func.sum(Resume.downloads)).scalar() or 0
    
    # Recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = db.query(func.count(User.id)).filter(User.created_at >= week_ago).scalar()
    new_resumes_week = db.query(func.count(Resume.id)).filter(Resume.created_at >= week_ago).scalar()
    
    # Template usage
    template_usage = db.query(
        Resume.template,
        func.count(Resume.id).label('count')
    ).group_by(Resume.template).all()
    
    # Average ATS score
    avg_ats_score = db.query(func.avg(Resume.ats_score)).filter(Resume.ats_score.isnot(None)).scalar()
    
    # Active share links
    active_shares = db.query(func.count(ShareLink.id)).filter(ShareLink.is_active == True).scalar()
    
    return APIResponse(
        success=True,
        message="Dashboard stats retrieved",
        data={
            "users": {
                "total": total_users,
                "active": active_users,
                "new_this_week": new_users_week
            },
            "resumes": {
                "total": total_resumes,
                "new_this_week": new_resumes_week,
                "total_views": total_views,
                "total_downloads": total_downloads,
                "avg_ats_score": round(avg_ats_score, 1) if avg_ats_score else 0
            },
            "templates": {
                "usage": [{"template": t[0], "count": t[1]} for t in template_usage]
            },
            "sharing": {
                "active_links": active_shares
            }
        }
    )

@router.get("/users")
def list_all_users(
    page: int = 1,
    size: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin)
):
    """List all users (admin only)"""
    total = db.query(func.count(User.id)).scalar()
    users = db.query(User).offset((page - 1) * size).limit(size).all()
    
    return APIResponse(
        success=True,
        message="Users retrieved",
        data={
            "users": users,
            "page": page,
            "size": size,
            "total": total
        }
    )

@router.get("/resumes")
def list_all_resumes(
    page: int = 1,
    size: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin)
):
    """List all resumes (admin only)"""
    total = db.query(func.count(Resume.id)).scalar()
    resumes = db.query(Resume).offset((page - 1) * size).limit(size).all()
    
    return APIResponse(
        success=True,
        message="Resumes retrieved",
        data={
            "resumes": resumes,
            "page": page,
            "size": size,
            "total": total
        }
    )
