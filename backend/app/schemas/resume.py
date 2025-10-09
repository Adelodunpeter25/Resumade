from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PersonalInfo(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None

class Experience(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    current: Optional[bool] = False
    description: Optional[str] = None
    achievements: Optional[List[str]] = []

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None

class Skill(BaseModel):
    name: str
    level: Optional[str] = None

class Certification(BaseModel):
    name: str
    issuer: str
    date: str
    credential_id: Optional[str] = None

class Project(BaseModel):
    name: str
    description: str
    technologies: Optional[List[str]] = []
    link: Optional[str] = None

class ResumeCreate(BaseModel):
    title: str
    template: str = "modern"
    personal_info: PersonalInfo
    experience: List[Experience] = []
    education: List[Education] = []
    skills: List[Skill] = []
    certifications: List[Certification] = []
    projects: List[Project] = []

class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    template: Optional[str] = None
    personal_info: Optional[PersonalInfo] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    skills: Optional[List[Skill]] = None
    certifications: Optional[List[Certification]] = None
    projects: Optional[List[Project]] = None

class Resume(BaseModel):
    id: int
    user_id: Optional[int]
    title: str
    template: str
    personal_info: dict
    experience: List[dict]
    education: List[dict]
    skills: List[dict]
    certifications: List[dict]
    projects: List[dict]
    views: int = 0
    downloads: int = 0
    ats_score: Optional[float] = None
    feedback: Optional[dict] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
