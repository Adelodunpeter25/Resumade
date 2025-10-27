from app.services.pdf_service import PDFService


def test_pdf_generation_with_resume_object():
    """Test PDF generation with Resume model object"""

    # Create a mock resume object
    class MockResume:
        id = 1
        template = "modern"
        personal_info = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "summary": "Software engineer",
        }
        experience = [
            {
                "company": "Tech Corp",
                "position": "Developer",
                "start_date": "2020",
                "end_date": "2023",
                "description": "Built applications",
            }
        ]
        education = [
            {
                "institution": "University",
                "degree": "BS",
                "field": "Computer Science",
                "start_date": "2015",
                "end_date": "2019",
            }
        ]
        skills = [{"name": "Python"}, {"name": "JavaScript"}]
        certifications = []
        projects = []

    pdf_service = PDFService()
    resume = MockResume()

    # Test PDF generation
    pdf_bytes = pdf_service.generate_resume_pdf(resume, "modern")

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF files start with %PDF
    assert pdf_bytes[:4] == b"%PDF"


def test_get_available_templates():
    """Test getting available templates"""
    templates = PDFService.get_available_templates()

    assert isinstance(templates, dict)
    assert len(templates) == 9
    assert "modern" in templates
    assert "classic" in templates
    assert "tech" in templates


def test_template_path():
    """Test template path resolution"""
    path = PDFService.get_template_path()

    assert isinstance(path, str)
    assert "templates" in path
