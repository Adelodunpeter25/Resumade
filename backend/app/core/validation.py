"""Input validation and sanitization utilities"""
import bleach
from typing import Optional
from app.core.constants import ValidationConfig
from app.core.validators import Validators

class InputValidator:
    """Validate and sanitize user inputs"""
    
    @staticmethod
    def sanitize_text(text: Optional[str], max_length: int = None) -> Optional[str]:
        """Remove HTML tags and limit length"""
        if not text:
            return text
        
        cleaned = bleach.clean(text, tags=[], strip=True)
        
        if max_length and len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
        
        return cleaned.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        return Validators.validate_email(email)
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone format"""
        return Validators.validate_phone(phone)
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        return Validators.validate_url(url)
    
    @staticmethod
    def sanitize_resume_data(resume_data: dict) -> dict:
        """Sanitize all text fields in resume data"""
        sanitized = {}
        
        # Personal info
        if "personal_info" in resume_data:
            pi = resume_data["personal_info"]
            sanitized["personal_info"] = {
                "full_name": InputValidator.sanitize_text(pi.get("full_name"), ValidationConfig.MAX_NAME_LENGTH),
                "email": pi.get("email", "").strip()[:ValidationConfig.MAX_EMAIL_LENGTH],
                "phone": InputValidator.sanitize_text(pi.get("phone"), ValidationConfig.MAX_PHONE_LENGTH),
                "location": InputValidator.sanitize_text(pi.get("location"), ValidationConfig.MAX_LOCATION_LENGTH),
                "linkedin": InputValidator.sanitize_text(pi.get("linkedin"), ValidationConfig.MAX_LOCATION_LENGTH),
                "website": InputValidator.sanitize_text(pi.get("website"), ValidationConfig.MAX_LOCATION_LENGTH),
                "summary": InputValidator.sanitize_text(pi.get("summary"), ValidationConfig.MAX_SUMMARY_LENGTH)
            }
        
        # Experience
        if "experience" in resume_data:
            sanitized["experience"] = [
                {
                    "company": InputValidator.sanitize_text(exp.get("company"), ValidationConfig.MAX_NAME_LENGTH),
                    "position": InputValidator.sanitize_text(exp.get("position"), ValidationConfig.MAX_NAME_LENGTH),
                    "start_date": InputValidator.sanitize_text(exp.get("start_date"), 50),
                    "end_date": InputValidator.sanitize_text(exp.get("end_date"), 50),
                    "description": InputValidator.sanitize_text(exp.get("description"), ValidationConfig.MAX_DESCRIPTION_LENGTH),
                    "achievements": [
                        InputValidator.sanitize_text(ach, 500)
                        for ach in (exp.get("achievements") or [])[:ValidationConfig.MAX_ACHIEVEMENTS_PER_EXPERIENCE]
                    ]
                }
                for exp in resume_data["experience"][:ValidationConfig.MAX_EXPERIENCE_ITEMS]
            ]
        
        # Education
        if "education" in resume_data:
            sanitized["education"] = [
                {
                    "institution": InputValidator.sanitize_text(edu.get("institution"), ValidationConfig.MAX_NAME_LENGTH),
                    "degree": InputValidator.sanitize_text(edu.get("degree"), ValidationConfig.MAX_NAME_LENGTH),
                    "field": InputValidator.sanitize_text(edu.get("field"), ValidationConfig.MAX_NAME_LENGTH),
                    "start_date": InputValidator.sanitize_text(edu.get("start_date"), 50),
                    "end_date": InputValidator.sanitize_text(edu.get("end_date"), 50),
                    "gpa": InputValidator.sanitize_text(edu.get("gpa"), 10)
                }
                for edu in resume_data["education"][:ValidationConfig.MAX_EDUCATION_ITEMS]
            ]
        
        # Skills
        if "skills" in resume_data:
            sanitized["skills"] = [
                {
                    "name": InputValidator.sanitize_text(skill.get("name"), 100),
                    "level": InputValidator.sanitize_text(skill.get("level"), 50)
                }
                for skill in resume_data["skills"][:ValidationConfig.MAX_SKILLS_ITEMS]
            ]
        
        # Certifications
        if "certifications" in resume_data:
            sanitized["certifications"] = [
                {
                    "name": InputValidator.sanitize_text(cert.get("name"), ValidationConfig.MAX_NAME_LENGTH),
                    "issuer": InputValidator.sanitize_text(cert.get("issuer"), ValidationConfig.MAX_NAME_LENGTH),
                    "date": InputValidator.sanitize_text(cert.get("date"), 50),
                    "credential_id": InputValidator.sanitize_text(cert.get("credential_id"), 100)
                }
                for cert in resume_data["certifications"][:ValidationConfig.MAX_CERTIFICATIONS_ITEMS]
            ]
        
        # Projects
        if "projects" in resume_data:
            sanitized["projects"] = [
                {
                    "name": InputValidator.sanitize_text(proj.get("name"), ValidationConfig.MAX_NAME_LENGTH),
                    "description": InputValidator.sanitize_text(proj.get("description"), ValidationConfig.MAX_DESCRIPTION_LENGTH),
                    "technologies": [
                        InputValidator.sanitize_text(tech, 50)
                        for tech in (proj.get("technologies") or [])[:ValidationConfig.MAX_TECHNOLOGIES_PER_PROJECT]
                    ],
                    "link": InputValidator.sanitize_text(proj.get("link"), 500)
                }
                for proj in resume_data["projects"][:ValidationConfig.MAX_PROJECTS_ITEMS]
            ]
        
        return sanitized
