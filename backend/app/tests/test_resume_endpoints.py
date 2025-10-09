import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Sample resume data
SAMPLE_RESUME = {
    "title": "Software Engineer Resume",
    "template": "modern",
    "personal_info": {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "location": "San Francisco, CA",
        "summary": "Experienced software engineer with 5 years of experience"
    },
    "experience": [
        {
            "company": "Tech Corp",
            "position": "Senior Developer",
            "start_date": "2020-01",
            "end_date": "2023-12",
            "description": "Led development team",
            "achievements": ["Increased performance by 40%"]
        }
    ],
    "education": [
        {
            "institution": "University of Tech",
            "degree": "Bachelor",
            "field": "Computer Science",
            "start_date": "2015",
            "end_date": "2019"
        }
    ],
    "skills": [
        {"name": "Python", "level": "Expert"},
        {"name": "JavaScript", "level": "Advanced"},
        {"name": "SQL", "level": "Intermediate"}
    ],
    "certifications": [],
    "projects": []
}

def test_create_resume_guest():
    """Test creating resume as guest"""
    response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == SAMPLE_RESUME["title"]
    assert data["user_id"] is None
    assert "ats_score" in data
    assert data["views"] == 0
    assert data["downloads"] == 0

def test_get_resume():
    """Test getting resume by ID"""
    # Create resume first
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["id"]
    
    # Get resume
    response = client.get(f"/api/resumes/{resume_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == resume_id
    assert data["views"] == 1  # Should increment

def test_export_resume_pdf():
    """Test exporting resume as PDF"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["id"]
    
    # Export as PDF
    response = client.get(f"/api/resumes/{resume_id}/export?format=pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_export_resume_docx():
    """Test exporting resume as DOCX"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["id"]
    
    # Export as DOCX
    response = client.get(f"/api/resumes/{resume_id}/export?format=docx")
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]

def test_get_resume_score():
    """Test getting ATS score"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["id"]
    
    # Get score
    response = client.get(f"/api/resumes/{resume_id}/score")
    assert response.status_code == 200
    data = response.json()
    assert "ats_score" in data
    assert "feedback" in data
    assert "suggestions" in data

def test_update_resume():
    """Test updating resume"""
    # Create resume
    create_response = client.post("/api/resumes/", json=SAMPLE_RESUME)
    resume_id = create_response.json()["id"]
    
    # Update
    update_data = {"title": "Updated Resume Title"}
    response = client.put(f"/api/resumes/{resume_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Resume Title"

def test_list_templates():
    """Test listing available templates"""
    response = client.get("/api/resumes/templates/list")
    assert response.status_code == 200
    data = response.json()
    assert "modern" in data
    assert "classic" in data

def test_resume_not_found():
    """Test getting non-existent resume"""
    response = client.get("/api/resumes/99999")
    assert response.status_code == 404
