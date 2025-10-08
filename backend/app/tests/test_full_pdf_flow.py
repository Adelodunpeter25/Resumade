#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.pdf_service import PDFService
from app.core.config import settings

def test_full_pdf_flow():
    """Test the complete PDF generation and storage flow"""
    try:
        print("Testing Full PDF Flow...")
        
        # Create a mock invoice object
        class MockCustomer:
            name = "Test Customer"
            email = "test@example.com"
            address = "123 Test Street"
            phone = "+1234567890"
        
        class MockItem:
            description = "Test Service"
            quantity = 2
            unit_price = 50.0
            total_price = 100.0
            notes = "Test notes"
        
        class MockInvoice:
            id = 999
            invoice_number = "TEST-001"
            customer = MockCustomer()
            items = [MockItem()]
            subtotal = 100.0
            tax_amount = 10.0
            total_amount = 110.0
            status = "draft"
            notes = "Test invoice for PDF generation"
            
            from datetime import datetime
            issue_date = datetime.now()
            due_date = datetime.now()
            created_at = datetime.now()
        
        mock_invoice = MockInvoice()
        
        # Test PDF service
        pdf_service = PDFService()
        print("✅ PDFService initialized")
        
        # Test HTML rendering
        html_content = pdf_service.render_invoice_html(mock_invoice, "modern")
        print(f"✅ HTML rendered: {len(html_content)} characters")
        
        # Test PDF generation
        pdf_bytes = pdf_service.generate_pdf_bytes(html_content)
        print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
        
        # Test the complete flow (should upload to Supabase)
        final_pdf = pdf_service.get_or_generate_pdf(mock_invoice, "modern")
        print(f"✅ Complete flow successful: {len(final_pdf)} bytes")
        
        # Check if file exists in Supabase
        filename = pdf_service.storage.generate_pdf_filename(mock_invoice.id, "modern")
        exists = pdf_service.storage.pdf_exists(filename)
        print(f"✅ PDF exists in Supabase: {exists} (filename: {filename})")
        
        # List files in bucket to verify
        files = pdf_service.storage.supabase.storage.from_(settings.bucket_name).list()
        print(f"Files in bucket after upload: {len(files)}")
        for file in files:
            print(f"  - {file.get('name')} ({file.get('metadata', {}).get('size', 'unknown')} bytes)")
        
        # Test second call (should use cached version)
        print("Testing cached retrieval...")
        cached_pdf = pdf_service.get_or_generate_pdf(mock_invoice, "modern")
        print(f"✅ Cached retrieval: {len(cached_pdf)} bytes")
        
        # Clean up test file
        pdf_service.storage.delete_pdf(filename)
        print("✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pdf_flow()
