from sqlalchemy import Column, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ResumeProgress(Base):
    __tablename__ = "resume_progress"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), index=True)
    completion_percentage = Column(Float, default=0)
    section_scores = Column(JSON, default={})
    
    resume = relationship("Resume", back_populates="progress")

    @property
    def sections_weight(self):
        return {
            "personal_info": 20,
            "experience": 30,
            "education": 20,
            "skills": 15,
            "projects": 15
        }
