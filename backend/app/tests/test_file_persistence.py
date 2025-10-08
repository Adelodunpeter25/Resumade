#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.storage_service import StorageService
from app.core.config import settings
import time

def test_file_persistence():
    """Test if files persist after download operations"""
    try:
        print("=== TESTING FILE PERSISTENCE ===")
        
        storage = StorageService()
        test_filename = "persistence_test.pdf"
        test_content = b"%PDF-1.4\nTest content for persistence check\n%%EOF"
        
        # 1. Upload a test file
        print("1. Uploading test file...")
        success = storage.upload_pdf(test_content, test_filename)
        print(f"   Upload success: {success}")
        
        # 2. Check if file exists
        print("2. Checking if file exists...")
        exists_before = storage.pdf_exists(test_filename)
        print(f"   File exists before download: {exists_before}")
        
        # 3. List files to confirm
        files_before = storage.supabase.storage.from_(settings.bucket_name).list()
        file_before = next((f for f in files_before if f.get('name') == test_filename), None)
        if file_before:
            print(f"   File found in listing: {file_before.get('name')} ({file_before.get('metadata', {}).get('size')} bytes)")
        
        # 4. Download the file (this is what might be causing the issue)
        print("3. Downloading file...")
        downloaded_content = storage.download_pdf(test_filename)
        if downloaded_content:
            print(f"   Download successful: {len(downloaded_content)} bytes")
        else:
            print("   Download failed!")
        
        # 5. Check if file still exists after download
        print("4. Checking if file exists after download...")
        exists_after = storage.pdf_exists(test_filename)
        print(f"   File exists after download: {exists_after}")
        
        # 6. List files again
        files_after = storage.supabase.storage.from_(settings.bucket_name).list()
        file_after = next((f for f in files_after if f.get('name') == test_filename), None)
        if file_after:
            print(f"   File still in listing: {file_after.get('name')} ({file_after.get('metadata', {}).get('size')} bytes)")
        else:
            print("   ❌ File disappeared from listing!")
        
        # 7. Try downloading again
        print("5. Trying to download again...")
        downloaded_again = storage.download_pdf(test_filename)
        if downloaded_again:
            print(f"   Second download successful: {len(downloaded_again)} bytes")
        else:
            print("   Second download failed!")
        
        # 8. Check the Supabase storage directly
        print("6. Direct Supabase storage check...")
        try:
            direct_download = storage.supabase.storage.from_(settings.bucket_name).download(test_filename)
            if direct_download:
                print(f"   Direct download successful: {len(direct_download)} bytes")
            else:
                print("   Direct download returned None")
        except Exception as e:
            print(f"   Direct download error: {e}")
        
        # 9. Wait a moment and check again (sometimes there's a delay)
        print("7. Waiting 2 seconds and checking again...")
        time.sleep(2)
        
        files_final = storage.supabase.storage.from_(settings.bucket_name).list()
        file_final = next((f for f in files_final if f.get('name') == test_filename), None)
        if file_final:
            print(f"   File found after wait: {file_final.get('name')}")
        else:
            print("   File still not found after wait")
        
        # Clean up if file exists
        if storage.pdf_exists(test_filename):
            storage.delete_pdf(test_filename)
            print("   ✅ Test file cleaned up")
        
        print("\n=== ANALYSIS ===")
        print("If files are disappearing after download:")
        print("1. Check if there's auto-deletion logic in your Supabase bucket")
        print("2. Check Supabase bucket policies and RLS settings")
        print("3. Verify the service role has proper permissions")
        print("4. Check if there are any triggers or functions deleting files")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_file_persistence()
