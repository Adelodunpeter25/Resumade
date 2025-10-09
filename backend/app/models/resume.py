from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    title = Column(String, nullable=False)
    template = Column(String, default="modern")
    
    # JSON fields for flexible resume data
    personal_info = Column(JSON, nullable=False)
    experience = Column(JSON, default=[])
    education = Column(JSON, default=[])
    skills = Column(JSON, default=[])
    certifications = Column(JSON, default=[])
    projects = Column(JSON, default=[])
    
    # Analytics
    views = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    
    # Scoring
    ats_score = Column(Float, nullable=True)
    feedback = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User")
