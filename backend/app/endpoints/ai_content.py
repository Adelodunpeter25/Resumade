"""AI content generation endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from app.core.auth import get_current_user_optional
from app.core.rate_limit import limiter
from app.models import User
from app.services.ai_content_service import AIContentService
from app.schemas.response import APIResponse

router = APIRouter(prefix="/ai", tags=["AI Content"])
logger = logging.getLogger(__name__)

ai_service = AIContentService()

class BulletPointRequest(BaseModel):
    position: str = Field(..., min_length=2, max_length=200)
    company: str = Field(..., min_length=2, max_length=200)
    current_description: Optional[str] = Field(None, max_length=2000)
    seniority_level: str = Field(default="mid", regex="^(entry|mid|senior)$")
    industry: Optional[str] = Field(None, max_length=100)

class ImproveDescriptionRequest(BaseModel):
    current_text: str = Field(..., min_length=10, max_length=2000)
    position: str = Field(..., min_length=2, max_length=200)
    company: str = Field(..., min_length=2, max_length=200)
    seniority_level: str = Field(default="mid", regex="^(entry|mid|senior)$")

class GenerateSummaryRequest(BaseModel):
    position: str = Field(..., min_length=2, max_length=200)
    years_experience: int = Field(..., ge=0, le=50)
    skills: List[str] = Field(..., min_items=1, max_items=20)
    industry: Optional[str] = Field(None, max_length=100)

@router.post("/generate-bullets", response_model=APIResponse[dict])
@limiter.limit("10/minute")
async def generate_bullet_points(
    request: Request,
    data: BulletPointRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Generate AI-powered bullet points for resume experience or projects
    
    Rate limit: 10 requests per minute
    """
    logger.info(f"Generating bullets for position: {data.position} at {data.company}")
    
    result = ai_service.generate_bullet_points(
        position=data.position,
        company=data.company,
        current_description=data.current_description or "",
        seniority_level=data.seniority_level,
        industry=data.industry
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=503,
            detail=result.get("error", "AI service unavailable")
        )
    
    return APIResponse(
        success=True,
        message=f"Generated {result['count']} bullet point suggestions",
        data={
            "suggestions": result["suggestions"],
            "count": result["count"]
        }
    )

@router.post("/improve-description", response_model=APIResponse[dict])
@limiter.limit("10/minute")
async def improve_description(
    request: Request,
    data: ImproveDescriptionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Improve existing description with AI suggestions
    
    Rate limit: 10 requests per minute
    """
    logger.info(f"Improving description for: {data.position}")
    
    context = {
        "position": data.position,
        "company": data.company,
        "seniority_level": data.seniority_level
    }
    
    result = ai_service.improve_description(
        current_text=data.current_text,
        context=context
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=503,
            detail=result.get("error", "AI service unavailable")
        )
    
    return APIResponse(
        success=True,
        message="Description improved successfully",
        data={
            "improved_text": result["improved_text"],
            "original_text": result["original_text"]
        }
    )

@router.post("/generate-summary", response_model=APIResponse[dict])
@limiter.limit("5/minute")
async def generate_summary(
    request: Request,
    data: GenerateSummaryRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Generate professional summary for resume
    
    Rate limit: 5 requests per minute
    """
    logger.info(f"Generating summary for: {data.position}")
    
    result = ai_service.generate_summary(
        position=data.position,
        years_experience=data.years_experience,
        skills=data.skills,
        industry=data.industry
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=503,
            detail=result.get("error", "AI service unavailable")
        )
    
    return APIResponse(
        success=True,
        message="Summary generated successfully",
        data={
            "summary": result["summary"]
        }
    )

@router.get("/status")
async def ai_service_status():
    """Check if AI service is available"""
    return {
        "available": ai_service.enabled,
        "model": "gemini-2.0-flash" if ai_service.enabled else None
    }
