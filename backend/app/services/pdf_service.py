import os
from io import BytesIO
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import logging

from app.models import Invoice
from app.services.storage_service import StorageService

logger = logging.getLogger(__name__)

class PDFService:
    
    # Available templates
    TEMPLATES = {
        "modern": "modern.html",
        "classic": "classic.html", 
        "minimal": "minimal.html",
        "corporate": "one.html",
        "minimalist": "two.html",
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
            "modern": "Modern - Clean and colorful design with cards",
            "classic": "Classic - Traditional business invoice style", 
            "minimal": "Minimal - Clean and simple typography",
            "corporate": "Corporate - Professional design with elegant styling",
            "minimalist": "Minimalist - Ultra-clean design with simple lines",
            "gradient": "Gradient - Vibrant design with modern cards",
            "formal": "Formal - Corporate letterhead with signature line",
            "bordered": "Bordered - Classic design with structured layout",
            "tech": "Tech - Dark theme with gradient effects and modern styling"
        }
    
    def render_invoice_html(self, invoice: Invoice, template: str = "modern") -> str:
        """
        Render invoice HTML from template
        
        Args:
            invoice: Invoice model instance with related data loaded
            template: Template name to use
            
        Returns:
            str: Rendered HTML content
        """
        if template not in self.TEMPLATES:
            template = "modern"  # Default fallback
        
        # Setup Jinja2 environment
        template_path = self.get_template_path()
        env = Environment(loader=FileSystemLoader(template_path))
        
        # Load and render template
        template_file = self.TEMPLATES[template]
        jinja_template = env.get_template(template_file)
        html_content = jinja_template.render(invoice=invoice)
        
        return html_content
    
    def generate_pdf_bytes(self, html_content: str) -> bytes:
        """
        Generate PDF bytes from HTML content using WeasyPrint
        
        Args:
            html_content: HTML content to convert to PDF
            
        Returns:
            bytes: PDF file content
        """
        # Generate PDF in memory using WeasyPrint
        font_config = FontConfiguration()
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf(font_config=font_config)
        
        return pdf_bytes
    
    def get_or_generate_pdf(self, invoice: Invoice, template: str = "modern") -> Optional[bytes]:
        """
        Get PDF from Supabase storage or generate if not exists
        
        Args:
            invoice: Invoice model instance with related data loaded
            template: Template name to use
            
        Returns:
            bytes: PDF content if successful, None if failed
        """
        try:
            # Generate filename for this invoice and template combination
            filename = self.storage.generate_pdf_filename(invoice.id, template)
            
            # Check if PDF already exists in Supabase storage
            if self.storage.pdf_exists(filename):
                logger.info(f"PDF found in storage, downloading: {filename}")
                pdf_bytes = self.storage.download_pdf(filename)
                if pdf_bytes:
                    return pdf_bytes
                else:
                    logger.warning(f"Failed to download existing PDF: {filename}")
            
            # PDF doesn't exist or download failed, generate new one
            logger.info(f"Generating new PDF: {filename}")
            
            # Step 1: Render HTML from template
            html_content = self.render_invoice_html(invoice, template)
            
            # Step 2: Generate PDF bytes from HTML
            pdf_bytes = self.generate_pdf_bytes(html_content)
            
            # Step 3: Upload PDF to Supabase storage for future use
            upload_success = self.storage.upload_pdf(pdf_bytes, filename)
            if upload_success:
                logger.info(f"PDF generated and uploaded successfully: {filename}")
            else:
                logger.warning(f"PDF generated but upload failed: {filename}")
            
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Failed to get or generate PDF for invoice {invoice.id}: {str(e)}")
            return None
    
    @staticmethod
    def get_invoice_filename(invoice: Invoice, template: str = "modern") -> str:
        """Generate download filename for invoice PDF"""
        return f"invoice_{invoice.invoice_number}_{template}.pdf"
