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
    
    # Extracted fields for efficient querying
    full_name = Column(String, index=True)  # From personal_info
    email = Column(String, index=True)  # From personal_info
    template_name = Column(String, index=True, default="professional-blue")  # Template identifier
    
    # JSON fields for flexible resume data
    personal_info = Column(JSON, nullable=False)
    experience = Column(JSON, default=[])
    education = Column(JSON, default=[])
    skills = Column(JSON, default=[])
    certifications = Column(JSON, default=[])
    projects = Column(JSON, default=[])
    
    # Template customization
    customization = Column(JSON, default={
        "primary_color": "#059669",  # emerald-600
        "secondary_color": "#0d9488",  # teal-600
        "font_family": "Inter",
        "font_size": "14",
        "line_height": "1.5",
        "margin": "0.5"
    })
    
    # Analytics
    views = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    
    # Scoring
    ats_score = Column(Float, nullable=True)
    feedback = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    
    user = relationship("User")
    progress = relationship("ResumeProgress", back_populates="resume", uselist=False, cascade="all, delete-orphan")
