from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.auth import get_current_user_optional, get_current_user
from app.models import Resume, User
from app.schemas import Resume as ResumeSchema, ResumeCreate, ResumeUpdate
from app.services import PDFService, ATSService, DOCXService

router = APIRouter(prefix="/resumes", tags=["Resumes"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ResumeSchema, status_code=status.HTTP_201_CREATED)
def create_resume(
    resume: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Create a new resume (works for guests and logged-in users)"""
    user_info = f"user: {current_user.email}" if current_user else "guest"
    logger.info(f"Creating resume '{resume.title}' by {user_info}")
    
    # Calculate ATS score
    resume_dict = {
        "personal_info": resume.personal_info.dict(),
        "experience": [e.dict() for e in resume.experience],
        "education": [e.dict() for e in resume.education],
        "skills": [s.dict() for s in resume.skills],
        "certifications": [c.dict() for c in resume.certifications],
        "projects": [p.dict() for p in resume.projects]
    }
    ats_result = ATSService.calculate_ats_score(resume_dict)
    
    db_resume = Resume(
        user_id=current_user.id if current_user else None,
        title=resume.title,
        template=resume.template,
        personal_info=resume.personal_info.dict(),
        experience=[e.dict() for e in resume.experience],
        education=[e.dict() for e in resume.education],
        skills=[s.dict() for s in resume.skills],
        certifications=[c.dict() for c in resume.certifications],
        projects=[p.dict() for p in resume.projects],
        ats_score=ats_result["percentage"],
        feedback=ats_result
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    logger.info(f"Resume created with ID: {db_resume.id}, ATS Score: {ats_result['percentage']}%")
    return db_resume

@router.get("/", response_model=List[ResumeSchema])
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all resumes for authenticated user"""
    logger.info(f"Fetching resumes for user: {current_user.email}")
    return db.query(Resume).filter(Resume.user_id == current_user.id).all()

@router.get("/{resume_id}", response_model=ResumeSchema)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get specific resume by ID"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Track view
    resume.views += 1
    db.commit()
    
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return resume

@router.put("/{resume_id}", response_model=ResumeSchema)
def update_resume(
    resume_id: int,
    resume_update: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Update resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = resume_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field in ["personal_info", "experience", "education", "skills", "certifications", "projects"]:
            if value is not None:
                if field == "personal_info":
                    setattr(resume, field, value.dict())
                else:
                    setattr(resume, field, [item.dict() for item in value])
        else:
            setattr(resume, field, value)
    
    # Recalculate ATS score
    resume_dict = {
        "personal_info": resume.personal_info,
        "experience": resume.experience,
        "education": resume.education,
        "skills": resume.skills,
        "certifications": resume.certifications,
        "projects": resume.projects
    }
    ats_result = ATSService.calculate_ats_score(resume_dict)
    resume.ats_score = ats_result["percentage"]
    resume.feedback = ats_result
    
    db.commit()
    db.refresh(resume)
    return resume

@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete resume (requires login)"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted"}

@router.get("/{resume_id}/export")
def export_resume(
    resume_id: int,
    format: str = Query("pdf", regex="^(pdf|docx)$"),
    template: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Export resume as PDF or DOCX"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Track download
    resume.downloads += 1
    db.commit()
    
    try:
        if format == "pdf":
            pdf_service = PDFService()
            template_name = template or resume.template
            content = pdf_service.generate_resume_pdf(resume, template_name)
            media_type = "application/pdf"
            filename = f"resume_{resume_id}.pdf"
        else:  # docx
            docx_service = DOCXService()
            content = docx_service.generate_resume_docx({
                "personal_info": resume.personal_info,
                "experience": resume.experience,
                "education": resume.education,
                "skills": resume.skills,
                "certifications": resume.certifications,
                "projects": resume.projects
            })
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"resume_{resume_id}.docx"
        
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/{resume_id}/score")
def get_resume_score(
    resume_id: int,
    job_description: Optional[str] = Query(None, description="Job description for context-aware scoring"),
    role_level: str = Query("mid", regex="^(entry|mid|senior)$", description="Job level for dynamic weighting"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get ATS score and feedback for resume with optional job description matching"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Calculate score with job description if provided
    resume_dict = {
        "personal_info": resume.personal_info,
        "experience": resume.experience,
        "education": resume.education,
        "skills": resume.skills,
        "certifications": resume.certifications,
        "projects": resume.projects
    }
    
    ats_result = ATSService.calculate_ats_score(resume_dict, job_description, role_level)
    
    return {
        "resume_id": resume.id,
        "ats_score": ats_result["percentage"],
        "grade": ats_result["grade"],
        "feedback": ats_result["feedback"],
        "section_breakdown": ats_result["section_breakdown"],
        "formatting_check": ats_result["formatting_check"],
        "suggestions": ATSService.get_keyword_suggestions(resume_dict, job_description),
        "role_level": role_level,
        "job_matched": job_description is not None
    }

@router.get("/{resume_id}/analytics")
def get_resume_analytics(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics for resume (requires login)"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {
        "resume_id": resume.id,
        "title": resume.title,
        "views": resume.views,
        "downloads": resume.downloads,
        "ats_score": resume.ats_score,
        "created_at": resume.created_at,
        "updated_at": resume.updated_at
    }

@router.get("/templates/list")
def list_templates():
    """Get available resume templates"""
    return PDFService.get_available_templates()
