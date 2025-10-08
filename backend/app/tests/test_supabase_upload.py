#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.storage_service import StorageService
from app.core.config import settings

def test_supabase_upload():
    """Test uploading a file to Supabase bucket"""
    try:
        print("Testing Supabase Storage Upload...")
        print(f"Supabase URL: {settings.supabase_url}")
        print(f"Bucket Name: {settings.bucket_name}")
        
        # Initialize storage service
        storage = StorageService()
        print("✅ StorageService initialized")
        
        # Create a test PDF content (simple bytes)
        test_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n179\n%%EOF"
        
        # Test filename
        test_filename = "test_invoice_123_modern.pdf"
        
        print(f"Attempting to upload test file: {test_filename}")
        
        # Try to upload the test PDF
        upload_success = storage.upload_pdf(test_pdf_content, test_filename)
        
        if upload_success:
            print("✅ File uploaded successfully!")
            
            # Try to check if file exists
            exists = storage.pdf_exists(test_filename)
            print(f"✅ File exists check: {exists}")
            
            # Try to download the file
            downloaded_content = storage.download_pdf(test_filename)
            if downloaded_content:
                print("✅ File downloaded successfully!")
                print(f"Downloaded size: {len(downloaded_content)} bytes")
                
                # Clean up - delete the test file
                delete_success = storage.delete_pdf(test_filename)
                print(f"✅ File deleted: {delete_success}")
            else:
                print("❌ Failed to download file")
        else:
            print("❌ Failed to upload file")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supabase_upload()
