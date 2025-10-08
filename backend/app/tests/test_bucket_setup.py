#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.storage_service import StorageService
from app.core.config import settings

def test_bucket_setup():
    """Test bucket setup and permissions"""
    try:
        print("Testing Supabase Bucket Setup...")
        print(f"Supabase URL: {settings.supabase_url}")
        print(f"Bucket Name: {settings.bucket_name}")
        
        # Initialize storage service
        storage = StorageService()
        print("✅ StorageService initialized")
        
        # Try to list buckets first
        try:
            buckets = storage.supabase.storage.list_buckets()
            print(f"Available buckets: {[bucket.name for bucket in buckets]}")
            
            # Check if our bucket exists
            bucket_exists = any(bucket.name == settings.bucket_name for bucket in buckets)
            print(f"Bucket '{settings.bucket_name}' exists: {bucket_exists}")
            
            if not bucket_exists:
                print(f"Creating bucket '{settings.bucket_name}'...")
                # Try to create the bucket
                try:
                    result = storage.supabase.storage.create_bucket(
                        settings.bucket_name,
                        options={"public": False}  # Private bucket
                    )
                    print(f"✅ Bucket created: {result}")
                except Exception as e:
                    print(f"❌ Failed to create bucket: {str(e)}")
                    
        except Exception as e:
            print(f"❌ Failed to list buckets: {str(e)}")
        
        # Try to list files in the bucket
        try:
            files = storage.supabase.storage.from_(settings.bucket_name).list()
            print(f"Files in bucket: {len(files)} files")
            for file in files[:5]:  # Show first 5 files
                print(f"  - {file.get('name', 'unknown')} ({file.get('metadata', {}).get('size', 'unknown size')})")
        except Exception as e:
            print(f"❌ Failed to list files in bucket: {str(e)}")
            
        # Test a simple upload
        test_content = b"Hello Supabase Storage!"
        test_filename = "test_connection.txt"
        
        print(f"Testing upload of {test_filename}...")
        try:
            response = storage.supabase.storage.from_(settings.bucket_name).upload(
                path=test_filename,
                file=test_content,
                file_options={"content-type": "text/plain"}
            )
            print(f"✅ Test upload successful")
            
            # Try to download it back
            downloaded = storage.supabase.storage.from_(settings.bucket_name).download(test_filename)
            if downloaded:
                print(f"✅ Test download successful: {len(downloaded)} bytes")
                
                # Clean up
                storage.supabase.storage.from_(settings.bucket_name).remove([test_filename])
                print("✅ Test file cleaned up")
            else:
                print("❌ Test download failed")
                
        except Exception as e:
            print(f"❌ Test upload failed: {str(e)}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bucket_setup()
