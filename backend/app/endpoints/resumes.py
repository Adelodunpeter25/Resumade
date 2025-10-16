from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import Response, HTMLResponse
from sqlalchemy.orm import joinedload, Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.auth import get_current_user_optional, get_current_user
from app.core.constants import ResponseMessages, CacheConstants
from app.core.rate_limit import limiter, RATE_LIMITS
from app.core.constants import FileConstants
from app.core.cache import cached
from app.models import Resume, User, ResumeVersion, ShareLink
from app.schemas import Resume as ResumeSchema, ResumeCreate, ResumeUpdate, ResumeVersion as ResumeVersionSchema
from app.schemas.response import APIResponse, PaginatedResponse
from app.services import PDFService, ATSService, DOCXService
from app.services.pdf_parser_service import PDFParserService

router = APIRouter(prefix="/resumes", tags=["Resumes"])
logger = logging.getLogger(__name__)

@cached(CacheConstants.RESUME_CACHE_TTL)
def _get_resume_by_id(resume_id: int, db: Session) -> Resume:
    """Cached resume retrieval by ID"""
    return db.query(Resume).options(
        joinedload(Resume.user),
        joinedload(Resume.progress)
    ).filter(Resume.id == resume_id).first()

@router.post("/", response_model=APIResponse[ResumeSchema], status_code=status.HTTP_201_CREATED)
@limiter.limit(RATE_LIMITS["create_resume"])
def create_resume(
    request: Request,
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
        full_name=resume.personal_info.full_name,
        email=resume.personal_info.email,
        template_name=resume.template,
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
    
    query = db.query(Resume).options(
        joinedload(Resume.user),
        joinedload(Resume.progress)
    ).filter(Resume.user_id == current_user.id)
    
    total = query.count()
    resumes = query.order_by(Resume.updated_at.desc()).offset((page - 1) * size).limit(size).all()
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
async def get_resume(
    resume_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get specific resume by ID"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    # Track view in background
    background_tasks.add_task(lambda: setattr(resume, 'views', resume.views + 1) or db.commit())
    
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
                    personal_data = value.dict() if hasattr(value, 'dict') else value
                    setattr(resume, field, personal_data)
                    # Update extracted fields
                    resume.full_name = personal_data.get('full_name')
                    resume.email = personal_data.get('email')
                else:
                    # Handle both list of dicts and list of Pydantic models
                    if value and hasattr(value[0], 'dict'):
                        setattr(resume, field, [item.dict() for item in value])
                    else:
                        setattr(resume, field, value)
        else:
            setattr(resume, field, value)
    
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
    from app.models.resume_version import ResumeVersion
    from app.models.share_link import ShareLink
    
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Delete related records first
    db.query(ResumeVersion).filter(ResumeVersion.resume_id == resume_id).delete()
    db.query(ShareLink).filter(ShareLink.resume_id == resume_id).delete()
    
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted"}

@router.post("/generate-pdf")
@limiter.limit(RATE_LIMITS["pdf_generate"])
def generate_guest_pdf(
    request: Request,
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
            headers={"Content-Disposition": "attachment; filename=resume.pdf"}
        )
    except Exception as e:
        logger.error(f"Guest PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

def _generate_txt_resume(resume) -> bytes:
    """Generate plain text resume"""
    lines = []
    
    # Personal Info
    if resume.personal_info:
        pi = resume.personal_info
        if pi.get('full_name'):
            lines.append(pi['full_name'].upper())
            lines.append('=' * len(pi['full_name']))
            lines.append('')
        
        contact = []
        if pi.get('email'): contact.append(f"Email: {pi['email']}")
        if pi.get('phone'): contact.append(f"Phone: {pi['phone']}")
        if pi.get('location'): contact.append(f"Location: {pi['location']}")
        if pi.get('linkedin'): contact.append(f"LinkedIn: {pi['linkedin']}")
        if pi.get('website'): contact.append(f"Website: {pi['website']}")
        
        if contact:
            lines.extend(contact)
            lines.append('')
        
        if pi.get('summary'):
            lines.append('PROFESSIONAL SUMMARY')
            lines.append('-' * 20)
            lines.append(pi['summary'])
            lines.append('')
    
    # Experience
    if resume.experience:
        lines.append('EXPERIENCE')
        lines.append('-' * 10)
        for exp in resume.experience:
            lines.append(f"{exp.get('position', '')} | {exp.get('company', '')}")
            dates = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
            lines.append(dates)
            if exp.get('location'):
                lines.append(exp['location'])
            if exp.get('description'):
                lines.append(exp['description'])
            lines.append('')
    
    # Education
    if resume.education:
        lines.append('EDUCATION')
        lines.append('-' * 9)
        for edu in resume.education:
            lines.append(f"{edu.get('degree', '')} in {edu.get('field_of_study', '')}")
            lines.append(edu.get('institution', ''))
            dates = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
            lines.append(dates)
            if edu.get('gpa'):
                lines.append(f"GPA: {edu['gpa']}")
            lines.append('')
    
    # Skills
    if resume.skills:
        lines.append('SKILLS')
        lines.append('-' * 6)
        for skill in resume.skills:
            skill_line = skill.get('name', '')
            if skill.get('level'):
                skill_line += f" ({skill['level']})"
            lines.append(skill_line)
        lines.append('')
    
    # Projects
    if resume.projects:
        lines.append('PROJECTS')
        lines.append('-' * 8)
        for project in resume.projects:
            lines.append(project.get('name', ''))
            if project.get('description'):
                lines.append(project['description'])
            if project.get('technologies'):
                lines.append(f"Technologies: {', '.join(project['technologies'])}")
            if project.get('url'):
                lines.append(f"URL: {project['url']}")
            lines.append('')
    
    # Certifications
    if resume.certifications:
        lines.append('CERTIFICATIONS')
        lines.append('-' * 14)
        for cert in resume.certifications:
            lines.append(f"{cert.get('name', '')} | {cert.get('issuer', '')}")
            if cert.get('date'):
                lines.append(cert['date'])
            lines.append('')
    
    return '\n'.join(lines).encode('utf-8')

@router.get("/{resume_id}/export")
@limiter.limit(RATE_LIMITS["export"])
async def export_resume(
    request: Request,
    resume_id: int,
    format: str = Query("pdf", regex="^(pdf|docx|txt)$"),
    template: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Export resume as PDF, DOCX, or TXT"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Track download in background
    background_tasks.add_task(lambda: setattr(resume, 'downloads', resume.downloads + 1) or db.commit())
    
    try:
        if format == "pdf":
            pdf_service = PDFService()
            template_name = template or resume.template
            content = pdf_service.generate_resume_pdf(resume, template_name)
            media_type = "application/pdf"
            filename = f"resume_{resume_id}.pdf"
        elif format == "docx":
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
        else:  # txt
            content = _generate_txt_resume(resume)
            media_type = "text/plain"
            filename = f"resume_{resume_id}.txt"
        
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/{resume_id}/score")
@limiter.limit(RATE_LIMITS["ats_score"])
def get_resume_score(
    request: Request,
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
        "ai_feedback": ats_result.get("ai_feedback"),
        "ai_suggestions": ats_result.get("ai_suggestions", []),
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

@router.post("/parse-pdf", response_model=APIResponse[dict])
@limiter.limit(RATE_LIMITS["pdf_upload"])
async def parse_pdf_resume(request: Request, file: UploadFile = File(...)):
    """Parse PDF resume and extract data"""
    logger.info(f"Parsing PDF file: {file.filename}")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Check file size
    content = await file.read()
    if len(content) > FileConstants.MAX_PDF_SIZE_BYTES:
        raise HTTPException(status_code=400, detail=f"File size exceeds {FileConstants.MAX_PDF_SIZE_MB}MB limit")
    
    try:
        
        # Parse PDF using PDFParserService
        parser = PDFParserService()
        extracted_data = parser.parse_resume_pdf(content)
        
        logger.info(f"Successfully parsed PDF: {file.filename}")
        return APIResponse(
            success=True,
            message="PDF parsed successfully",
            data=extracted_data
        )
        
    except Exception as e:
        logger.error(f"Failed to parse PDF {file.filename}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")

@router.get("/templates/list")
def list_templates():
    """Get available resume templates organized by category"""
    templates = PDFService.get_available_templates()
    
    # Organize templates by category
    categorized = {}
    for template in templates:
        category = template["category"]
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(template)
    
    return APIResponse(
        success=True,
        message="Templates retrieved",
        data={
            "categories": categorized,
            "all_templates": templates
        }
    )

@router.get("/templates/preview", response_class=HTMLResponse)
def preview_template(template: str = Query(default="professional-blue")):
    """Render HTML preview of a template with sample data"""
    from types import SimpleNamespace
    
    # Sample resume data as simple object
    sample_data = SimpleNamespace(
        id=0,
        title="Sample Resume",
        template=template,
        personal_info={
            "full_name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "(555) 123-4567",
            "location": "New York, NY",
            "linkedin": "https://linkedin.com/in/johndoe",
            "website": "https://johndoe.com",
            "summary": "Results-driven professional with 5+ years of experience in delivering innovative solutions. Proven track record of leading cross-functional teams and driving business growth through strategic initiatives."
        },
        experience=[
            {
                "company": "Tech Solutions Inc",
                "position": "Senior Software Engineer",
                "location": "New York, NY",
                "start_date": "2021",
                "end_date": "",
                "current": True,
                "description": "Led development of microservices architecture serving 1M+ users\nMentored team of 5 junior developers and improved deployment efficiency by 40%\nImplemented CI/CD pipelines reducing release time by 60%"
            },
            {
                "company": "Digital Innovations",
                "position": "Software Engineer",
                "location": "Boston, MA",
                "start_date": "2019",
                "end_date": "2021",
                "current": False,
                "description": "Developed RESTful APIs and React applications\nCollaborated with product team to deliver features on time\nOptimized database queries improving performance by 35%"
            }
        ],
        education=[
            {
                "institution": "Massachusetts Institute of Technology",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "location": "Cambridge, MA",
                "start_date": "2015",
                "end_date": "2019",
                "gpa": "3.8/4.0"
            }
        ],
        skills=[
            {"name": "JavaScript", "level": "Expert"},
            {"name": "Python", "level": "Advanced"},
            {"name": "React", "level": "Expert"},
            {"name": "Node.js", "level": "Advanced"},
            {"name": "AWS", "level": "Intermediate"},
            {"name": "Docker", "level": "Intermediate"}
        ],
        certifications=[
            {
                "name": "AWS Certified Solutions Architect",
                "issuer": "Amazon Web Services",
                "date": "2022"
            },
            {
                "name": "Professional Scrum Master",
                "issuer": "Scrum.org",
                "date": "2021"
            }
        ],
        projects=[
            {
                "name": "E-Commerce Platform",
                "description": "Built scalable e-commerce platform handling 10K+ daily transactions with real-time inventory management",
                "technologies": ["React", "Node.js", "MongoDB", "Stripe"],
                "url": "https://github.com/johndoe/ecommerce"
            },
            {
                "name": "Analytics Dashboard",
                "description": "Created data visualization dashboard processing 1M+ events daily with custom reporting features",
                "technologies": ["Python", "Django", "PostgreSQL", "D3.js"],
                "url": "https://github.com/johndoe/analytics"
            }
        ]
    )
    
    pdf_service = PDFService()
    html_content = pdf_service.render_resume_html(sample_data, template)
    
    return HTMLResponse(content=html_content)

@router.get("/{resume_id}/preview", response_class=HTMLResponse)
def preview_resume_by_id(
    resume_id: str,
    db: Session = Depends(get_db)
):
    """Render HTML preview of a specific resume"""
    # Handle guest mode
    if resume_id == "new":
        raise HTTPException(status_code=400, detail="Cannot preview unsaved guest resume. Please save first.")
    
    try:
        resume_id_int = int(resume_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid resume ID")
    
    resume = db.query(Resume).filter(Resume.id == resume_id_int).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    pdf_service = PDFService()
    html_content = pdf_service.render_resume_html(resume, resume.template_name)
    
    return HTMLResponse(content=html_content)

@router.post("/preview", response_class=HTMLResponse)
async def preview_resume_live(request: Request):
    """Render HTML preview with user's live data"""
    from types import SimpleNamespace
    import json
    
    # Get form data
    form_data = await request.form()
    resume_json = form_data.get('resume_data')
    
    if resume_json:
        resume_data = json.loads(resume_json)
    else:
        # Fallback to empty data
        resume_data = {
            'template_name': 'professional-blue',
            'personal_info': {},
            'experience': [],
            'education': [],
            'skills': [],
            'certifications': [],
            'projects': []
        }
    
    # Convert dict to object for template rendering
    resume_obj = SimpleNamespace(
        id=resume_data.get('id', 0),
        title=resume_data.get('title', 'Resume'),
        template=resume_data.get('template_name', 'professional-blue'),
        personal_info=resume_data.get('personal_info', {}),
        experience=resume_data.get('experience', []),
        education=resume_data.get('education', []),
        skills=resume_data.get('skills', []),
        certifications=resume_data.get('certifications', []),
        projects=resume_data.get('projects', []),
        customization=resume_data.get('customization', {}),
        section_names=resume_data.get('section_names', {}),
        custom_sections=resume_data.get('custom_sections', [])
    )
    
    pdf_service = PDFService()
    html_content = pdf_service.render_resume_html(resume_obj, resume_obj.template)
    
    return HTMLResponse(content=html_content)

# Version History
@router.get("/{resume_id}/versions", response_model=APIResponse[list[ResumeVersionSchema]])
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
    return APIResponse(success=True, message="Versions retrieved", data=[ResumeVersionSchema.from_orm(v) for v in versions])

@router.post("/{resume_id}/versions", response_model=APIResponse[ResumeVersionSchema])
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
    
    return APIResponse(success=True, message="Version created", data=ResumeVersionSchema.from_orm(version))

# Share Links
@router.get("/{resume_id}/share")
def get_share_links(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active share links for a resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    share_links = db.query(ShareLink).filter(
        ShareLink.resume_id == resume_id,
        ShareLink.is_active == True
    ).all()
    
    from app.models.resume_analytics import ResumeAnalytics
    
    links_data = []
    for link in share_links:
        # Get analytics counts
        views = db.query(func.count(ResumeAnalytics.id)).filter(
            ResumeAnalytics.share_token == link.token,
            ResumeAnalytics.event_type == 'view'
        ).scalar() or 0
        
        downloads = db.query(func.count(ResumeAnalytics.id)).filter(
            ResumeAnalytics.share_token == link.token,
            ResumeAnalytics.event_type == 'download'
        ).scalar() or 0
        
        links_data.append({
            "id": link.id,
            "token": link.token,
            "slug": link.slug,
            "resume_id": link.resume_id,
            "expires_at": link.expires_at,
            "is_active": link.is_active,
            "created_at": link.created_at,
            "views": views,
            "downloads": downloads
        })
    
    return APIResponse(success=True, message="Share links retrieved", data=links_data)

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
    
    # Check for existing active non-expired link
    from datetime import timezone
    now = datetime.now(timezone.utc)
    existing_link = db.query(ShareLink).filter(
        ShareLink.resume_id == resume_id,
        ShareLink.is_active == True
    ).first()
    
    if existing_link:
        expires_at = existing_link.expires_at if existing_link.expires_at.tzinfo else existing_link.expires_at.replace(tzinfo=timezone.utc)
        if expires_at > now:
            raise HTTPException(status_code=400, detail="Active link found for this resume")
        else:
            existing_link.is_active = False
            db.commit()
    
    username = current_user.full_name or current_user.email.split('@')[0]
    slug = ShareLink.generate_slug(username, resume.title)
    
    share_link = ShareLink(
        resume_id=resume_id,
        token=ShareLink.generate_token(),
        slug=slug,
        expires_at=datetime.utcnow() + timedelta(days=expires_in_days)
    )
    
    try:
        db.add(share_link)
        db.commit()
        db.refresh(share_link)
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create share link: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create share link")
    
    return APIResponse(
        success=True,
        message="Share link created",
        data={"id": share_link.id, "token": share_link.token, "slug": share_link.slug, "expires_at": share_link.expires_at, "resume_id": share_link.resume_id, "is_active": share_link.is_active, "created_at": share_link.created_at}
    )

@router.get("/shared/{slug:path}/preview", response_class=HTMLResponse)
def preview_shared_resume(slug: str, db: Session = Depends(get_db)):
    """Render shared resume with its template"""
    from types import SimpleNamespace
    
    share_link = db.query(ShareLink).filter(ShareLink.slug == slug, ShareLink.is_active == True).first()
    if not share_link:
        share_link = db.query(ShareLink).filter(ShareLink.token == slug, ShareLink.is_active == True).first()
    
    if not share_link:
        return HTMLResponse(content="<h1>Share link not found</h1>", status_code=404)
    
    if share_link.expires_at:
        from datetime import timezone
        now = datetime.now(timezone.utc)
        expires_at = share_link.expires_at if share_link.expires_at.tzinfo else share_link.expires_at.replace(tzinfo=timezone.utc)
        if expires_at < now:
            return HTMLResponse(content="<h1>Share link expired</h1>", status_code=410)
    
    resume = db.query(Resume).filter(Resume.id == share_link.resume_id).first()
    if not resume:
        return HTMLResponse(content="<h1>Resume not found</h1>", status_code=404)
    
    resume.views += 1
    db.commit()
    
    resume_obj = SimpleNamespace(
        id=resume.id,
        title=resume.title,
        template=resume.template,
        personal_info=resume.personal_info,
        experience=resume.experience,
        education=resume.education,
        skills=resume.skills,
        certifications=resume.certifications,
        projects=resume.projects
    )
    
    pdf_service = PDFService()
    html_content = pdf_service.render_resume_html(resume_obj, resume.template)
    
    return HTMLResponse(content=html_content)

@router.get("/shared/{slug:path}", response_model=APIResponse[ResumeSchema])
def get_shared_resume(slug: str, request: Request, db: Session = Depends(get_db)):
    """Access resume via public share link"""
    from app.models.resume_analytics import ResumeAnalytics
    
    share_link = db.query(ShareLink).filter(ShareLink.slug == slug, ShareLink.is_active == True).first()
    if not share_link:
        share_link = db.query(ShareLink).filter(ShareLink.token == slug, ShareLink.is_active == True).first()
    
    if not share_link:
        raise HTTPException(status_code=404, detail="Share link not found")
    
    if share_link.expires_at:
        from datetime import timezone
        now = datetime.now(timezone.utc)
        expires_at = share_link.expires_at if share_link.expires_at.tzinfo else share_link.expires_at.replace(tzinfo=timezone.utc)
        if expires_at < now:
            raise HTTPException(status_code=410, detail="Share link expired")
    
    resume = db.query(Resume).filter(Resume.id == share_link.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail=ResponseMessages.RESUME_NOT_FOUND)
    
    # Track view analytics
    analytics = ResumeAnalytics(
        resume_id=resume.id,
        share_token=share_link.token,
        event_type='view',
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get('user-agent')
    )
    db.add(analytics)
    
    resume.views += 1
    db.commit()
    
    return APIResponse(success=True, message="Resume retrieved", data=ResumeSchema.from_orm(resume))

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
