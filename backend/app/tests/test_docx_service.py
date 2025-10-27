from app.services.docx_service import DOCXService


def test_generate_resume_docx():
    """Test DOCX generation"""
    resume_data = {
        "personal_info": {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "location": "San Francisco, CA",
            "summary": "Experienced software engineer",
        },
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Senior Developer",
                "start_date": "2020-01",
                "end_date": "2023-12",
                "description": "Led development team",
                "achievements": ["Increased performance by 40%"],
            }
        ],
        "education": [
            {
                "institution": "University of Tech",
                "degree": "Bachelor",
                "field": "Computer Science",
                "start_date": "2015",
                "end_date": "2019",
                "gpa": "3.8",
            }
        ],
        "skills": [{"name": "Python", "level": "Expert"}, {"name": "JavaScript"}],
        "certifications": [
            {"name": "AWS Certified", "issuer": "Amazon", "date": "2023-01"}
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Built scalable platform",
                "technologies": ["Python", "React"],
            }
        ],
    }

    docx_bytes = DOCXService.generate_resume_docx(resume_data)

    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 0

    # Verify it's a valid DOCX (starts with PK for ZIP format)
    assert docx_bytes[:2] == b"PK"


def test_generate_minimal_docx():
    """Test DOCX generation with minimal data"""
    resume_data = {
        "personal_info": {"full_name": "Jane Smith", "email": "jane@example.com"},
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": [],
    }

    docx_bytes = DOCXService.generate_resume_docx(resume_data)

    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 0
