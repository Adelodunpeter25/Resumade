"""Integration tests for PDF/DOCX export with Supabase"""

from unittest.mock import patch

SAMPLE_RESUME = {
    "title": "Test Resume",
    "template": "modern",
    "personal_info": {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
    },
    "experience": [
        {
            "company": "Tech Corp",
            "position": "Developer",
            "start_date": "2020",
            "end_date": "2023",
            "description": "Built applications",
        }
    ],
    "education": [
        {
            "institution": "University",
            "degree": "BS",
            "field": "Computer Science",
            "start_date": "2015",
            "end_date": "2019",
        }
    ],
    "skills": [{"name": "Python"}, {"name": "JavaScript"}],
    "certifications": [],
    "projects": [],
}


def test_export_pdf_creates_valid_file(client):
    """Test PDF export creates valid PDF file"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["data"]["id"]

    # Export as PDF
    response = client.get(f"/api/resumes/{resume_id}/export?format=pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0
    assert response.content[:4] == b"%PDF"


def test_export_docx_creates_valid_file(client):
    """Test DOCX export creates valid DOCX file"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["data"]["id"]

    # Export as DOCX
    response = client.get(f"/api/resumes/{resume_id}/export?format=docx")

    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]
    assert len(response.content) > 0
    assert response.content[:2] == b"PK"  # ZIP signature


def test_export_increments_download_count(client, db_session):
    """Test that export increments download counter"""
    from app.models import Resume

    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["data"]["id"]

    # Check initial downloads
    resume = db_session.query(Resume).filter(Resume.id == resume_id).first()
    initial_downloads = resume.downloads

    # Export
    client.get(f"/api/resumes/{resume_id}/export?format=pdf")

    # Check downloads incremented
    db_session.refresh(resume)
    assert resume.downloads == initial_downloads + 1


def test_export_with_different_templates(client):
    """Test export with different templates"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["data"]["id"]

    templates = ["modern", "classic", "minimal"]

    for template in templates:
        response = client.get(
            f"/api/resumes/{resume_id}/export?format=pdf&template={template}"
        )
        assert response.status_code == 200
        assert response.content[:4] == b"%PDF"


@patch("app.services.storage_service.StorageService.upload_pdf")
def test_export_uploads_to_supabase(mock_upload, client):
    """Test that export uploads to Supabase storage"""
    mock_upload.return_value = True

    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["data"]["id"]

    # Export
    response = client.get(f"/api/resumes/{resume_id}/export?format=pdf")

    assert response.status_code == 200
    mock_upload.assert_called_once()


def test_export_nonexistent_resume(client):
    """Test export of non-existent resume"""
    response = client.get("/api/resumes/99999/export?format=pdf")

    assert response.status_code == 404


def test_export_invalid_format(client):
    """Test export with invalid format"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["data"]["id"]

    # Try invalid format
    response = client.get(f"/api/resumes/{resume_id}/export?format=invalid")

    assert response.status_code == 422  # Validation error
