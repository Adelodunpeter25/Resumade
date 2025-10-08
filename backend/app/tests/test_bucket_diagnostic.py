#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.storage_service import StorageService
from app.core.config import settings
import json

def test_bucket_diagnostic():
    """Comprehensive bucket diagnostic"""
    try:
        print("=== SUPABASE BUCKET DIAGNOSTIC ===")
        print(f"Supabase URL: {settings.supabase_url}")
        print(f"Bucket Name: '{settings.bucket_name}'")
        print(f"Service Role Key: {settings.service_role[:20]}...")
        print()
        
        storage = StorageService()
        
        # 1. List all buckets with details
        print("1. LISTING ALL BUCKETS:")
        try:
            buckets = storage.supabase.storage.list_buckets()
            for bucket in buckets:
                print(f"   Bucket: {bucket.name}")
                print(f"   ID: {bucket.id}")
                print(f"   Public: {bucket.public}")
                print(f"   Created: {bucket.created_at}")
                print()
        except Exception as e:
            print(f"   ❌ Error listing buckets: {e}")
        
        # 2. Check specific bucket details
        print(f"2. CHECKING BUCKET '{settings.bucket_name}':")
        try:
            bucket_info = storage.supabase.storage.get_bucket(settings.bucket_name)
            print(f"   Found bucket: {bucket_info.name}")
            print(f"   Public: {bucket_info.public}")
            print(f"   File size limit: {bucket_info.file_size_limit}")
            print(f"   Allowed MIME types: {bucket_info.allowed_mime_types}")
        except Exception as e:
            print(f"   ❌ Error getting bucket info: {e}")
        
        # 3. List files in bucket with full details
        print(f"3. LISTING FILES IN BUCKET '{settings.bucket_name}':")
        try:
            files = storage.supabase.storage.from_(settings.bucket_name).list()
            print(f"   Total files found: {len(files)}")
            
            if files:
                for i, file in enumerate(files):
                    print(f"   File {i+1}:")
                    print(f"     Name: {file.get('name')}")
                    print(f"     Size: {file.get('metadata', {}).get('size', 'unknown')} bytes")
                    print(f"     Type: {file.get('metadata', {}).get('mimetype', 'unknown')}")
                    print(f"     Last Modified: {file.get('updated_at', 'unknown')}")
                    print(f"     Full metadata: {json.dumps(file, indent=6, default=str)}")
                    print()
            else:
                print("   No files found in bucket")
        except Exception as e:
            print(f"   ❌ Error listing files: {e}")
        
        # 4. Test upload with detailed tracking
        print("4. TESTING FILE UPLOAD:")
        test_filename = "diagnostic_test.pdf"
        test_content = b"%PDF-1.4\nTest PDF content for diagnostic"
        
        try:
            print(f"   Uploading '{test_filename}'...")
            response = storage.supabase.storage.from_(settings.bucket_name).upload(
                path=test_filename,
                file=test_content,
                file_options={"content-type": "application/pdf"}
            )
            print(f"   ✅ Upload response: {response}")
            
            # Immediately check if file appears
            print("   Checking if file appears in listing...")
            files_after = storage.supabase.storage.from_(settings.bucket_name).list()
            uploaded_file = next((f for f in files_after if f.get('name') == test_filename), None)
            
            if uploaded_file:
                print(f"   ✅ File found in listing: {uploaded_file}")
                
                # Try to get public URL (if bucket is public)
                try:
                    public_url = storage.supabase.storage.from_(settings.bucket_name).get_public_url(test_filename)
                    print(f"   Public URL: {public_url}")
                except Exception as e:
                    print(f"   No public URL (bucket might be private): {e}")
                
                # Try to download
                try:
                    downloaded = storage.supabase.storage.from_(settings.bucket_name).download(test_filename)
                    print(f"   ✅ Download successful: {len(downloaded)} bytes")
                except Exception as e:
                    print(f"   ❌ Download failed: {e}")
                
                # Clean up
                try:
                    storage.supabase.storage.from_(settings.bucket_name).remove([test_filename])
                    print(f"   ✅ File deleted successfully")
                except Exception as e:
                    print(f"   ❌ Delete failed: {e}")
            else:
                print(f"   ❌ File not found in listing after upload!")
                
        except Exception as e:
            print(f"   ❌ Upload failed: {e}")
        
        # 5. Check bucket permissions
        print("5. BUCKET PERMISSIONS CHECK:")
        try:
            # Try to create a temporary bucket to test permissions
            temp_bucket_name = "temp-test-bucket"
            try:
                storage.supabase.storage.create_bucket(temp_bucket_name)
                print("   ✅ Can create buckets (admin permissions)")
                # Clean up
                storage.supabase.storage.delete_bucket(temp_bucket_name)
                print("   ✅ Can delete buckets")
            except Exception as e:
                print(f"   ⚠️  Cannot create/delete buckets: {e}")
        except Exception as e:
            print(f"   ❌ Permission check failed: {e}")
            
        print("\n=== DIAGNOSTIC COMPLETE ===")
        print("If files are uploading but not visible in Supabase dashboard:")
        print("1. Check if you're looking at the correct project")
        print("2. Check if the bucket is private (files won't show in public view)")
        print("3. Try refreshing the Supabase dashboard")
        print("4. Check the Storage > Buckets section, not the Database section")
        
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bucket_diagnostic()
