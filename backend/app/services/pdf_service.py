import os
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import logging

from app.models import Resume
from app.services.storage_service import StorageService

logger = logging.getLogger(__name__)

class PDFService:
    
    TEMPLATES = {
        "modern": "modern.html",
        "classic": "classic.html", 
        "minimal": "minimal.html",
        "professional-blue": "professional-blue.html",
        "linkedin-style": "linkedin-style.html",
        "gradient": "three.html",
        "formal": "four.html",
        "bordered": "five.html",
        "tech": "six.html"
    }
    
    def __init__(self):
        self.storage = StorageService()
    
    @staticmethod
    def get_template_path() -> str:
        """Get path to templates directory"""
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(current_dir, "templates")
    
    @staticmethod
    def get_available_templates() -> dict:
        """Get list of available templates"""
        return {
            "modern": "Modern - Clean and colorful design",
            "classic": "Classic - Traditional professional style", 
            "minimal": "Minimal - Clean and simple typography",
            "corporate": "Corporate - Professional elegant styling",
            "minimalist": "Minimalist - Ultra-clean simple lines",
            "gradient": "Gradient - Vibrant modern design",
            "formal": "Formal - Corporate letterhead style",
            "bordered": "Bordered - Structured layout",
            "tech": "Tech - Dark theme with gradients"
        }
    
    def render_resume_html(self, resume: Resume, template: str = "modern") -> str:
        """Render resume HTML from template"""
        template_file = self.TEMPLATES.get(template, self.TEMPLATES["modern"])
        template_path = self.get_template_path()
        
        env = Environment(loader=FileSystemLoader(template_path))
        template_obj = env.get_template(template_file)
        
        return template_obj.render(resume=resume)
    
    def generate_resume_pdf(self, resume: Resume, template: str = "modern") -> bytes:
        """Generate PDF from resume"""
        html_content = self.render_resume_html(resume, template)
        pdf_bytes = HTML(string=html_content).write_pdf()
        
        # Upload to storage
        filename = self.storage.generate_pdf_filename(resume.id, template)
        self.storage.upload_pdf(pdf_bytes, filename)
        
        return pdf_bytes
