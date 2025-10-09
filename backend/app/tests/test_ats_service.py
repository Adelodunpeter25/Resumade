import pytest
from app.services.ats_service import ATSService

def test_calculate_ats_score_complete_resume():
    """Test ATS score calculation for complete resume"""
    resume_data = {
        "personal_info": {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "location": "San Francisco, CA",
            "summary": "Experienced software engineer"
        },
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Developer",
                "description": "Developed and implemented new features. Increased performance by 40%"
            }
        ],
        "education": [
            {"institution": "University", "degree": "BS", "field": "CS"}
        ],
        "skills": [
            {"name": "Python"},
            {"name": "JavaScript"},
            {"name": "SQL"},
            {"name": "Docker"},
            {"name": "AWS"}
        ],
        "certifications": [],
        "projects": []
    }
    
    result = ATSService.calculate_ats_score(resume_data)
    
    assert result["score"] > 0
    assert result["max_score"] == 100
    assert "percentage" in result
    assert "feedback" in result
    assert "grade" in result
    assert result["score"] >= 80  # Should score high with complete data

def test_calculate_ats_score_minimal_resume():
    """Test ATS score for minimal resume"""
    resume_data = {
        "personal_info": {"full_name": "John Doe"},
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": []
    }
    
    result = ATSService.calculate_ats_score(resume_data)
    
    assert result["score"] < 50  # Should score low
    assert len(result["feedback"]) > 0  # Should have feedback

def test_get_grade():
    """Test grade calculation"""
    assert ATSService._get_grade(95) == "A"
    assert ATSService._get_grade(85) == "B"
    assert ATSService._get_grade(75) == "C"
    assert ATSService._get_grade(65) == "D"
    assert ATSService._get_grade(50) == "F"

def test_keyword_suggestions():
    """Test keyword suggestions"""
    resume_data = {
        "personal_info": {},
        "experience": [],
        "education": [],
        "skills": [{"name": "Python"}],
        "certifications": [],
        "projects": []
    }
    
    suggestions = ATSService.get_keyword_suggestions(resume_data)
    
    assert isinstance(suggestions, list)
    assert len(suggestions) <= 10
    assert "python" not in [s.lower() for s in suggestions]  # Already has Python

def test_action_verbs_detection():
    """Test detection of action verbs in experience"""
    resume_with_verbs = {
        "personal_info": {"full_name": "John", "email": "j@e.com"},
        "experience": [
            {"description": "Developed and led team projects"}
        ],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": []
    }
    
    resume_without_verbs = {
        "personal_info": {"full_name": "John", "email": "j@e.com"},
        "experience": [
            {"description": "Was responsible for things"}
        ],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": []
    }
    
    result_with = ATSService.calculate_ats_score(resume_with_verbs)
    result_without = ATSService.calculate_ats_score(resume_without_verbs)
    
    assert result_with["score"] > result_without["score"]
