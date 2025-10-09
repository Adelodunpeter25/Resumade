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
        "professional-blue": "professional-blue.html",
        "linkedin-style": "linkedin-style.html",
        "gradient-sidebar": "gradient-sidebar.html",
        "minimalist-two-column": "minimalist-two-column.html"
    }
    
    def __init__(self):
        self.storage = StorageService()
    
    @staticmethod
    def get_template_path() -> str:
        """Get path to templates directory"""
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(current_dir, "templates")
    
    @staticmethod
    def get_available_templates() -> list:
        """Get list of available templates"""
        templates = [
            {
                "name": "professional-blue",
                "display_name": "Professional Blue",
                "description": "Elegant with blue accents"
            },
            {
                "name": "linkedin-style",
                "display_name": "LinkedIn Style",
                "description": "Card-based social media layout"
            },
            {
                "name": "gradient-sidebar",
                "display_name": "Gradient Sidebar",
                "description": "Dark sidebar with purple gradients"
            },
            {
                "name": "minimalist-two-column",
                "display_name": "Minimalist Two-Column",
                "description": "Clean layout with dates on left"
            }
        ]
        return templates

    def render_resume_html(self, resume: Resume, template: str = "professional-blue") -> str:
        """Render resume HTML from template"""
        template_file = self.TEMPLATES.get(template, self.TEMPLATES["professional-blue"])
        template_path = self.get_template_path()
        
        env = Environment(loader=FileSystemLoader(template_path))
        template_obj = env.get_template(template_file)
        
        return template_obj.render(resume=resume)
    
    def generate_resume_pdf(self, resume: Resume, template: str = "professional-blue") -> bytes:
        """Generate PDF from resume"""
        html_content = self.render_resume_html(resume, template)
        pdf_bytes = HTML(string=html_content).write_pdf()
        
        # Upload to storage
        filename = self.storage.generate_pdf_filename(resume.id, template)
        self.storage.upload_pdf(pdf_bytes, filename)
        
        return pdf_bytes
