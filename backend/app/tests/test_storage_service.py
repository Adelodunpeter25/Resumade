"""Supabase storage service tests"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.storage_service import StorageService

@pytest.fixture
def storage_service():
    return StorageService()

@pytest.fixture
def mock_supabase():
    with patch('app.services.storage_service.create_client') as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client

def test_generate_pdf_filename(storage_service):
    """Test PDF filename generation"""
    filename = storage_service.generate_pdf_filename(123, "modern")
    
    assert "resume_123_modern" in filename
    assert filename.endswith(".pdf")

def test_upload_pdf_success(storage_service, mock_supabase):
    """Test successful PDF upload to Supabase"""
    mock_supabase.storage.from_().upload.return_value = {"path": "test.pdf"}
    
    pdf_bytes = b"%PDF-1.4 test content"
    filename = "test_resume.pdf"
    
    result = storage_service.upload_pdf(pdf_bytes, filename)
    
    assert result is True
    mock_supabase.storage.from_().upload.assert_called_once()

def test_upload_pdf_failure(storage_service, mock_supabase):
    """Test PDF upload failure handling"""
    mock_supabase.storage.from_().upload.side_effect = Exception("Upload failed")
    
    pdf_bytes = b"%PDF-1.4 test content"
    filename = "test_resume.pdf"
    
    result = storage_service.upload_pdf(pdf_bytes, filename)
    
    assert result is False

def test_download_pdf_success(storage_service, mock_supabase):
    """Test successful PDF download from Supabase"""
    mock_pdf_content = b"%PDF-1.4 test content"
    mock_supabase.storage.from_().download.return_value = mock_pdf_content
    
    filename = "test_resume.pdf"
    result = storage_service.download_pdf(filename)
    
    assert result == mock_pdf_content
    mock_supabase.storage.from_().download.assert_called_once_with(filename)

def test_download_pdf_not_found(storage_service, mock_supabase):
    """Test PDF download when file doesn't exist"""
    mock_supabase.storage.from_().download.side_effect = Exception("File not found")
    
    filename = "nonexistent.pdf"
    result = storage_service.download_pdf(filename)
    
    assert result is None

def test_pdf_exists_true(storage_service, mock_supabase):
    """Test checking if PDF exists (true case)"""
    mock_supabase.storage.from_().list.return_value = [{"name": "test.pdf"}]
    
    result = storage_service.pdf_exists("test.pdf")
    
    assert result is True

def test_pdf_exists_false(storage_service, mock_supabase):
    """Test checking if PDF exists (false case)"""
    mock_supabase.storage.from_().list.return_value = []
    
    result = storage_service.pdf_exists("nonexistent.pdf")
    
    assert result is False
