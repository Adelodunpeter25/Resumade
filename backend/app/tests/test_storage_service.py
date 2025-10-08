#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services import StorageService, PDFService
from app.core.config import settings

def test_storage_service():
    """Test storage service functions"""
    try:
        # Test that storage service can be initialized
        storage = StorageService()
        assert storage.bucket_name == settings.bucket_name
        print("✅ StorageService initialized successfully")
        
        # Test filename generation
        filename = storage.generate_pdf_filename(123, "modern")
        assert filename == "invoice_123_modern.pdf"
        print("✅ PDF filename generation works")
        
        # Test PDF service integration
        pdf_service = PDFService()
        assert pdf_service.storage is not None
        print("✅ PDFService with storage integration works")
        
        # Test template availability
        templates = PDFService.get_available_templates()
        assert "corporate" in templates
        assert "tech" in templates
        assert "gradient" in templates
        print("✅ All templates available with new names")
        
        print("✅ Storage service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Storage service test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Supabase storage integration...")
    
    # Check if Supabase credentials are configured
    if not settings.supabase_url or not settings.service_role:
        print("⚠️  Supabase credentials not configured in .env file")
        print("   Please add SUPABASE_URL and SERVICE_ROLE")
    else:
        print("✅ Supabase credentials found in environment")
    
    test_storage_service()
