from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.resume_progress import ResumeProgressService
from app.models.resume import Resume
from typing import Dict

router = APIRouter(tags=["Resumes"])

@router.get("/resumes/{resume_id}/progress")
async def get_resume_progress(
    resume_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    resume = await db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    progress = await ResumeProgressService.update_progress(resume, db)
    
    return {
        "completion_percentage": progress.completion_percentage,
        "section_scores": progress.section_scores
    }
