#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.storage_service import StorageService

def test_upload_download_keep():
    """Upload and download test - keep file in bucket"""
    storage = StorageService()
    
    # Test data
    filename = "persistent_test_file.pdf"
    test_content = b"%PDF-1.4\nPersistent test PDF content for verification\n%%EOF"
    
    print(f"1. Uploading {filename}...")
    upload_success = storage.upload_pdf(test_content, filename)
    print(f"   Upload: {'✅ SUCCESS' if upload_success else '❌ FAILED'}")
    
    print(f"2. Downloading {filename}...")
    downloaded_content = storage.download_pdf(filename)
    if downloaded_content:
        print(f"   Download: ✅ SUCCESS ({len(downloaded_content)} bytes)")
        print(f"   Content matches: {'✅ YES' if downloaded_content == test_content else '❌ NO'}")
    else:
        print("   Download: ❌ FAILED")
    
    print(f"3. File kept in bucket - check Supabase dashboard")
    print(f"   Filename: {filename}")
    print(f"   Size: {len(test_content)} bytes")

if __name__ == "__main__":
    test_upload_download_keep()
