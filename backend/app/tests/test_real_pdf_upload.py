#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.storage_service import StorageService
from app.services.pdf_service import PDFService
from app.core.config import settings
from datetime import datetime

def test_real_pdf_upload():
    """Test uploading a real generated PDF"""
    try:
        print("=== TESTING REAL PDF UPLOAD ===")
        
        # Create mock invoice
        class MockCustomer:
            name = "Acme Corporation"
            email = "billing@acme.com"
            address = "123 Business Ave, Suite 100\nNew York, NY 10001"
            phone = "+1 (555) 123-4567"
        
        class MockItem:
            description = "Web Development Services"
            quantity = 40
            unit_price = 125.0
            total_price = 5000.0
            notes = "Custom e-commerce platform development"
        
        class MockInvoice:
            id = 12345
            invoice_number = "INV-2025-001"
            customer = MockCustomer()
            items = [MockItem()]
            subtotal = 5000.0
            tax_amount = 450.0
            total_amount = 5450.0
            status = "pending"
            notes = "Payment due within 30 days. Thank you for your business!"
            issue_date = datetime(2025, 10, 8)
            due_date = datetime(2025, 11, 7)
            created_at = datetime.now()
        
        mock_invoice = MockInvoice()
        
        # Generate PDF using different templates
        pdf_service = PDFService()
        templates_to_test = ["modern", "corporate", "tech", "gradient"]
        
        for template in templates_to_test:
            print(f"\n--- Testing {template.upper()} template ---")
            
            # Generate PDF
            pdf_bytes = pdf_service.get_or_generate_pdf(mock_invoice, template)
            filename = pdf_service.storage.generate_pdf_filename(mock_invoice.id, template)
            
            print(f"✅ Generated PDF: {len(pdf_bytes)} bytes")
            print(f"✅ Filename: {filename}")
            
            # Check if it exists in Supabase
            exists = pdf_service.storage.pdf_exists(filename)
            print(f"✅ Exists in Supabase: {exists}")
            
            if exists:
                # Get file details
                files = pdf_service.storage.supabase.storage.from_(settings.bucket_name).list()
                file_info = next((f for f in files if f.get('name') == filename), None)
                if file_info:
                    print(f"✅ File size in Supabase: {file_info.get('metadata', {}).get('size')} bytes")
                    print(f"✅ File ID: {file_info.get('id')}")
                    print(f"✅ Created: {file_info.get('created_at')}")
                    
                    # Generate public URL (even though bucket is private, this shows the path)
                    public_url = pdf_service.storage.supabase.storage.from_(settings.bucket_name).get_public_url(filename)
                    print(f"✅ Storage path: {public_url}")
        
        # Show all files in bucket
        print(f"\n--- ALL FILES IN BUCKET '{settings.bucket_name}' ---")
        files = pdf_service.storage.supabase.storage.from_(settings.bucket_name).list()
        print(f"Total files: {len(files)}")
        
        for i, file in enumerate(files, 1):
            print(f"{i}. {file.get('name')} ({file.get('metadata', {}).get('size')} bytes)")
        
        print(f"\n✅ SUCCESS! Check your Supabase dashboard:")
        print(f"   1. Go to Storage → Buckets")
        print(f"   2. Click on '{settings.bucket_name}' bucket")
        print(f"   3. You should see {len(files)} PDF files")
        
        # Clean up test files
        print(f"\nCleaning up test files...")
        for template in templates_to_test:
            filename = pdf_service.storage.generate_pdf_filename(mock_invoice.id, template)
            pdf_service.storage.delete_pdf(filename)
        print("✅ Test files cleaned up")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_pdf_upload()
