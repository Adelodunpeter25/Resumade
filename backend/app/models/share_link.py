from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.base import Base
import secrets
import re

class ShareLink(Base):
    __tablename__ = "share_links"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_slug(username: str, resume_title: str) -> str:
        clean_username = re.sub(r'[^a-zA-Z0-9]', '', username.lower())
        clean_title = re.sub(r'[^a-zA-Z0-9\s-]', '', resume_title.lower())
        clean_title = re.sub(r'\s+', '-', clean_title.strip())
        suffix = secrets.token_urlsafe(4)
        return f"{clean_username}/{clean_title}-{suffix}"
