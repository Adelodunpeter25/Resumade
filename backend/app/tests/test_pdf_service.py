#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services import PDFService

def test_pdf_service():
    """Test PDF service functions"""
    try:
        # Test available templates
        templates = PDFService.get_available_templates()
        assert "modern" in templates
        assert "classic" in templates
        assert "minimal" in templates
        print("✅ Available templates loaded successfully")
        
        # Test template path
        template_path = PDFService.get_template_path()
        assert os.path.exists(template_path)
        print("✅ Template path exists")
        
        # Test template files exist
        for template_key in PDFService.TEMPLATES:
            template_file = os.path.join(template_path, PDFService.TEMPLATES[template_key])
            assert os.path.exists(template_file), f"Template file {template_file} not found"
        print("✅ All template files exist")
        
        # Test filename generation
        class MockInvoice:
            invoice_number = "INV-12345678"
        
        filename = PDFService.get_invoice_filename(MockInvoice(), "modern")
        assert filename == "invoice_INV-12345678_modern.pdf"
        print("✅ PDF filename generation works")
        
        print("✅ PDF service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ PDF service test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing PDF service...")
    test_pdf_service()
