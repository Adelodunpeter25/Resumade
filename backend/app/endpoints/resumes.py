from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.auth import get_current_user_optional, get_current_user
from app.core.constants import ResponseMessages
from app.models import Resume, User, ResumeVersion, ShareLink
from app.schemas import Resume as ResumeSchema, ResumeCreate, ResumeUpdate
from app.schemas.response import APIResponse, PaginatedResponse
from app.services import PDFService, ATSService, DOCXService

router = APIRouter(prefix="/resumes", tags=["Resumes"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=APIResponse[ResumeSchema], status_code=status.HTTP_201_CREATED)
def create_resume(
    resume: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Create a new resume"""
    user_info = f"user: {current_user.email}" if current_user else "guest"
    logger.info(f"Creating resume '{resume.title}' by {user_info}")
    
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
    return APIResponse(success=True, message=ResponseMessages.RESUME_CREATED, data=db_resume)

@router.get("/", response_model=PaginatedResponse[ResumeSchema])
def get_resumes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get paginated resumes for authenticated user"""
    logger.info(f"Fetching resumes for user: {current_user.email}")
    
    query = db.query(Resume).filter(Resume.user_id == current_user.id)
    total = query.count()
    resumes = query.offset((page - 1) * size).limit(size).all()
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        success=True,
        message="Resumes retrieved",
        data=resumes,
        page=page,
        size=size,
        total=total,
        pages=pages
    )

@router.get("/{resume_id}", response_model=APIResponse[ResumeSchema])
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get specific resume by ID"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    resume.views += 1
    db.commit()
    
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=ResponseMessages.UNAUTHORIZED)
    
    return APIResponse(success=True, message="Resume retrieved", data=resume)

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
                    # Handle both dict and Pydantic model
                    setattr(resume, field, value.dict() if hasattr(value, 'dict') else value)
                else:
                    # Handle both list of dicts and list of Pydantic models
                    if value and hasattr(value[0], 'dict'):
                        setattr(resume, field, [item.dict() for item in value])
                    else:
                        setattr(resume, field, value)
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

@router.post("/generate-pdf")
def generate_guest_pdf(
    resume_data: dict,
    template: str = Query("professional-blue"),
):
    """Generate PDF for guest users (no authentication required)"""
    try:
        # Create a mock Resume object with required attributes
        class MockResume:
            def __init__(self, data, template_name):
                self.id = 0  # Mock ID for guest resumes
                self.title = data.get("title", "Resume")
                self.template = template_name
                self.personal_info = data.get("personal_info", {})
                self.experience = data.get("experience", [])
                self.education = data.get("education", [])
                self.skills = data.get("skills", [])
                self.certifications = data.get("certifications", [])
                self.projects = data.get("projects", [])
        
        resume_obj = MockResume(resume_data, template)
        pdf_service = PDFService()
        content = pdf_service.generate_resume_pdf(resume_obj, template)
        
        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=resume.pdf"}
        )
    except Exception as e:
        logger.error(f"Guest PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

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
    return APIResponse(
        success=True,
        message="Templates retrieved",
        data=PDFService.get_available_templates()
    )

@router.get("/templates/preview")
def preview_templates():
    """Get template previews with sample data"""
    sample_resume = {
        "personal_info": {"full_name": "John Doe", "email": "john@example.com", "phone": "+1234567890"},
        "experience": [{"company": "Tech Corp", "position": "Developer", "start_date": "2020", "description": "Built applications"}],
        "education": [{"institution": "University", "degree": "BS", "field": "Computer Science"}],
        "skills": [{"name": "Python"}, {"name": "JavaScript"}]
    }
    
    templates = PDFService.get_available_templates()
    return APIResponse(
        success=True,
        message="Template previews",
        data={"templates": templates, "sample_data": sample_resume}
    )

# Version History
@router.get("/{resume_id}/versions")
def get_resume_versions(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get version history for resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    versions = db.query(ResumeVersion).filter(ResumeVersion.resume_id == resume_id).order_by(ResumeVersion.version_number.desc()).all()
    return APIResponse(success=True, message="Versions retrieved", data=versions)

@router.post("/{resume_id}/versions")
def create_resume_version(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new version snapshot"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    last_version = db.query(ResumeVersion).filter(ResumeVersion.resume_id == resume_id).order_by(ResumeVersion.version_number.desc()).first()
    version_number = (last_version.version_number + 1) if last_version else 1
    
    version = ResumeVersion(
        resume_id=resume_id,
        version_number=version_number,
        title=resume.title,
        template=resume.template,
        personal_info=resume.personal_info,
        experience=resume.experience,
        education=resume.education,
        skills=resume.skills,
        certifications=resume.certifications,
        projects=resume.projects
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    
    return APIResponse(success=True, message="Version created", data=version)

# Share Links
@router.post("/{resume_id}/share")
def create_share_link(
    resume_id: int,
    expires_in_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a public share link for resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    share_link = ShareLink(
        resume_id=resume_id,
        token=ShareLink.generate_token(),
        expires_at=datetime.utcnow() + timedelta(days=expires_in_days)
    )
    db.add(share_link)
    db.commit()
    db.refresh(share_link)
    
    return APIResponse(
        success=True,
        message="Share link created",
        data={"token": share_link.token, "expires_at": share_link.expires_at}
    )

@router.get("/shared/{token}")
def get_shared_resume(token: str, db: Session = Depends(get_db)):
    """Access resume via public share link"""
    share_link = db.query(ShareLink).filter(ShareLink.token == token, ShareLink.is_active == True).first()
    
    if not share_link:
        raise HTTPException(status_code=404, detail="Share link not found")
    
    if share_link.expires_at and share_link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Share link expired")
    
    resume = db.query(Resume).filter(Resume.id == share_link.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    resume.views += 1
    db.commit()
    
    return APIResponse(success=True, message="Resume retrieved", data=resume)

@router.delete("/{resume_id}/share/{token}")
def delete_share_link(
    resume_id: int,
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deactivate a share link"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    share_link = db.query(ShareLink).filter(ShareLink.token == token, ShareLink.resume_id == resume_id).first()
    if not share_link:
        raise HTTPException(status_code=404, detail="Share link not found")
    
    share_link.is_active = False
    db.commit()
    
    return APIResponse(success=True, message="Share link deactivated", data=None)
