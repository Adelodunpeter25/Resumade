import os
from io import BytesIO
from typing import Optional
import logging
from supabase import create_client, Client

from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    """Service for managing PDF storage in Supabase"""
    
    def __init__(self):
        # Initialize Supabase client with credentials from environment
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.service_role  # Updated to match config
        )
        self.bucket_name = settings.bucket_name  # Updated to match config
    
    def generate_pdf_filename(self, resume_id: int, template: str) -> str:
        """Generate consistent filename for PDF storage"""
        return f"resume_{resume_id}_{template}.pdf"
    
    def upload_pdf(self, pdf_bytes: bytes, filename: str) -> bool:
        """
        Upload PDF bytes to Supabase Storage
        
        Args:
            pdf_bytes: PDF content as bytes
            filename: Target filename in storage
            
        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            # Upload PDF to Supabase storage bucket
            response = self.supabase.storage.from_(self.bucket_name).upload(
                path=filename,
                file=pdf_bytes,
                file_options={
                    "content-type": "application/pdf"
                }
            )
            
            logger.info(f"PDF uploaded successfully: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload PDF {filename}: {str(e)}")
            return False
    
    def download_pdf(self, filename: str) -> Optional[bytes]:
        """
        Download PDF from Supabase Storage
        
        Args:
            filename: PDF filename in storage
            
        Returns:
            bytes: PDF content if found, None if not found or error
        """
        try:
            # Download PDF from Supabase storage
            response = self.supabase.storage.from_(self.bucket_name).download(filename)
            
            if response:
                logger.info(f"PDF downloaded successfully: {filename}")
                return response
            else:
                logger.warning(f"PDF not found in storage: {filename}")
                return None
                
        except Exception as e:
            logger.warning(f"Failed to download PDF {filename}: {str(e)}")
            return None
    
    def pdf_exists(self, filename: str) -> bool:
        """
        Check if PDF exists in Supabase Storage
        
        Args:
            filename: PDF filename to check
            
        Returns:
            bool: True if PDF exists, False otherwise
        """
        try:
            # List files in bucket to check if PDF exists
            response = self.supabase.storage.from_(self.bucket_name).list()
            
            # Check if any file matches our filename
            return any(file.get('name') == filename for file in response)
            
        except Exception as e:
            logger.error(f"Failed to check PDF existence {filename}: {str(e)}")
            return False
    
    def delete_pdf(self, filename: str) -> bool:
        """
        Delete PDF from Supabase Storage
        
        Args:
            filename: PDF filename to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            # Delete PDF from Supabase storage
            response = self.supabase.storage.from_(self.bucket_name).remove([filename])
            
            logger.info(f"PDF deleted successfully: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete PDF {filename}: {str(e)}")
            return False
