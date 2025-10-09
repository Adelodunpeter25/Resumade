from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.base import Base

class ResumeVersion(Base):
    __tablename__ = "resume_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    
    # Snapshot of resume data
    title = Column(String, nullable=False)
    template = Column(String)
    personal_info = Column(JSON)
    experience = Column(JSON)
    education = Column(JSON)
    skills = Column(JSON)
    certifications = Column(JSON)
    projects = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
