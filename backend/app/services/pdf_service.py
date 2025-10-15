import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import logging

from app.models import Resume
from app.services.storage_service import StorageService
from app.core.cache import cached, template_cache
from cachetools import TTLCache

logger = logging.getLogger(__name__)
template_list_cache = TTLCache(maxsize=1, ttl=86400)  # 24 hours

class PDFService:
    
    TEMPLATES = {
        # Existing templates
        "professional-blue": "professional-blue.html",
        "linkedin-style": "linkedin-style.html",
        "gradient-sidebar": "gradient-sidebar.html",
        "minimalist-two-column": "minimalist-two-column.html",
        "executive-modern": "executive-modern.html",
        "creative-gradient": "creative-gradient.html",
        "classic-serif": "seven.html",
        
        # New industry-specific templates
        "modern-tech": "modern-tech.html",
        "creative-designer": "creative-designer.html",
        "executive-corporate": "executive-corporate.html",
        "marketing-professional": "marketing-professional.html",
        "academic-research": "academic-research.html",
    }
    
    def __init__(self):
        self.storage = StorageService()
    
    @staticmethod
    def get_template_path() -> str:
        """Get path to templates directory"""
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(current_dir, "templates")
    
    @staticmethod
    @cached(template_list_cache)
    def get_available_templates() -> list:
        """Get list of available templates with categories"""
        templates = [
            # Technology Templates
            {
                "name": "modern-tech",
                "display_name": "Modern Tech",
                "description": "Clean sidebar design for software engineers",
                "category": "technology",
                "industry": ["software", "engineering", "tech"],
                "ats_score": 95
            },
            {
                "name": "professional-blue",
                "display_name": "Professional Blue",
                "description": "Classic professional layout",
                "category": "professional",
                "industry": ["business", "finance", "consulting"],
                "ats_score": 90
            },
            
            # Creative Templates
            {
                "name": "creative-designer",
                "display_name": "Creative Designer",
                "description": "Vibrant design for creative professionals",
                "category": "creative",
                "industry": ["design", "marketing", "media"],
                "ats_score": 85
            },
            {
                "name": "creative-gradient",
                "display_name": "Creative Gradient",
                "description": "Modern gradient design",
                "category": "creative",
                "industry": ["design", "advertising", "digital"],
                "ats_score": 80
            },
            
            # Executive Templates
            {
                "name": "executive-corporate",
                "display_name": "Executive Corporate",
                "description": "Traditional executive format",
                "category": "executive",
                "industry": ["management", "executive", "leadership"],
                "ats_score": 95
            },
            {
                "name": "executive-modern",
                "display_name": "Executive Modern",
                "description": "Contemporary executive design",
                "category": "executive",
                "industry": ["management", "consulting", "finance"],
                "ats_score": 90
            },
            
            # Marketing Templates
            {
                "name": "marketing-professional",
                "display_name": "Marketing Professional",
                "description": "Dynamic layout for marketing roles",
                "category": "marketing",
                "industry": ["marketing", "sales", "advertising"],
                "ats_score": 88
            },
            
            # Academic Templates
            {
                "name": "academic-research",
                "display_name": "Academic Research",
                "description": "Traditional CV format for academia",
                "category": "academic",
                "industry": ["research", "academia", "education"],
                "ats_score": 93
            },
            
            # Minimalist Templates
            {
                "name": "minimalist-two-column",
                "display_name": "Minimalist Two-Column",
                "description": "Clean two-column layout",
                "category": "minimalist",
                "industry": ["academic", "research", "healthcare"],
                "ats_score": 92
            },
            {
                "name": "linkedin-style",
                "display_name": "LinkedIn Style",
                "description": "Social media inspired layout",
                "category": "modern",
                "industry": ["sales", "marketing", "business"],
                "ats_score": 88
            },
            
            # Specialized Templates
            {
                "name": "gradient-sidebar",
                "display_name": "Gradient Sidebar",
                "description": "Dark sidebar with gradients",
                "category": "modern",
                "industry": ["tech", "startup", "digital"],
                "ats_score": 87
            },
            {
                "name": "classic-serif",
                "display_name": "Classic Serif",
                "description": "Traditional serif typography",
                "category": "traditional",
                "industry": ["law", "academia", "government"],
                "ats_score": 93
            }
        ]
        return templates

    @cached(template_cache)
    def _get_template(self, template: str):
        """Get cached template object"""
        template_file = self.TEMPLATES.get(template, self.TEMPLATES["professional-blue"])
        template_path = self.get_template_path()
        env = Environment(loader=FileSystemLoader(template_path))
        return env.get_template(template_file)
    
    def render_resume_html(self, resume: Resume, template: str = "professional-blue") -> str:
        """Render resume HTML from template"""
        template_obj = self._get_template(template)
        return template_obj.render(resume=resume)
    
    def generate_resume_pdf(self, resume: Resume, template: str = "professional-blue") -> bytes:
        """Generate PDF from resume"""
        html_content = self.render_resume_html(resume, template)
        pdf_bytes = HTML(string=html_content).write_pdf()
        
        # Upload to storage
        filename = self.storage.generate_pdf_filename(resume.id, template)
        self.storage.upload_pdf(pdf_bytes, filename)
        
        return pdf_bytes
