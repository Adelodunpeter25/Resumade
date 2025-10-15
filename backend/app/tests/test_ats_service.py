from app.services.ats_service import ATSService

def test_calculate_ats_score_complete_resume():
    """Test ATS score calculation for complete resume"""
    resume_data = {
        "personal_info": {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "location": "San Francisco, CA",
            "summary": "Experienced software engineer with 5+ years building scalable applications"
        },
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Developer",
                "start_date": "2020",
                "end_date": "2023",
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
            {"name": "AWS"},
            {"name": "React"},
            {"name": "Node.js"},
            {"name": "PostgreSQL"}
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
    assert "section_breakdown" in result
    assert result["score"] >= 70  # Should score well with complete data

def test_calculate_ats_score_with_job_description():
    """Test ATS score with job description matching"""
    resume_data = {
        "personal_info": {"full_name": "John Doe", "email": "j@e.com"},
        "experience": [{"description": "Developed Python applications using Django and PostgreSQL"}],
        "education": [{"institution": "Uni", "degree": "BS", "field": "CS"}],
        "skills": [{"name": "Python"}, {"name": "Django"}, {"name": "PostgreSQL"}],
        "certifications": [],
        "projects": []
    }
    
    job_description = "Looking for Python developer with Django and PostgreSQL experience"
    
    result = ATSService.calculate_ats_score(resume_data, job_description)
    
    assert result["score"] > 0
    assert "section_breakdown" in result

def test_dynamic_weighting_by_role():
    """Test different scoring for different role levels"""
    resume_data = {
        "personal_info": {"full_name": "John", "email": "j@e.com", "phone": "123-456-7890"},
        "experience": [{"company": "Tech", "position": "Dev", "start_date": "2020", "description": "Developed apps"}],
        "education": [{"institution": "Uni", "degree": "BS", "field": "CS"}],
        "skills": [{"name": "Python"}],
        "certifications": [],
        "projects": []
    }
    
    entry_result = ATSService.calculate_ats_score(resume_data, role_level="entry")
    senior_result = ATSService.calculate_ats_score(resume_data, role_level="senior")
    
    # Scores should differ based on weighting
    assert entry_result["score"] != senior_result["score"]

def test_fuzzy_matching():
    """Test fuzzy keyword matching"""
    assert ATSService.fuzzy_match("React.js", "react")
    assert ATSService.fuzzy_match("NodeJS", "node")
    assert ATSService.fuzzy_match("Python3", "python")

def test_normalize_text():
    """Test text normalization"""
    assert ATSService.normalize_text("Python, JavaScript!") == "python javascript"
    assert ATSService.normalize_text("  Multiple   Spaces  ") == "multiple spaces"

def test_detect_quantifiable_achievements():
    """Test detection of quantified achievements"""
    text1 = "Increased sales by 40% and reduced costs by $50K"
    text2 = "Worked on various projects"
    
    assert ATSService.detect_quantifiable_achievements(text1) >= 2
    assert ATSService.detect_quantifiable_achievements(text2) == 0

def test_formatting_issues_detection():
    """Test formatting issue detection"""
    resume_good = {
        "personal_info": {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    }
    
    resume_bad = {
        "personal_info": {
            "full_name": "John ★ Doe",
            "email": "invalid-email",
            "phone": "123"
        }
    }
    
    result_good = ATSService.check_formatting_issues(resume_good)
    result_bad = ATSService.check_formatting_issues(resume_bad)
    
    assert not result_good["has_issues"]
    assert result_bad["has_issues"]
    assert len(result_bad["issues"]) > 0

def test_section_breakdown():
    """Test section-by-section scoring"""
    resume_data = {
        "personal_info": {"full_name": "John", "email": "j@e.com"},
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": []
    }
    
    result = ATSService.calculate_ats_score(resume_data)
    
    assert "section_breakdown" in result
    assert "personal_info" in result["section_breakdown"]
    assert "experience" in result["section_breakdown"]
    assert "skills" in result["section_breakdown"]

def test_keyword_suggestions_with_job_description():
    """Test keyword suggestions based on job description"""
    resume_data = {
        "personal_info": {},
        "experience": [],
        "education": [],
        "skills": [{"name": "Python"}],
        "certifications": [],
        "projects": []
    }
    
    job_description = "Looking for developer with React, Node.js, and Docker experience"
    suggestions = ATSService.get_keyword_suggestions(resume_data, job_description)
    
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    # Should suggest keywords from job description
    assert any("react" in s.lower() or "node" in s.lower() for s in suggestions)

def test_extract_keywords_from_job_description():
    """Test job description keyword extraction"""
    jd = "We are looking for a Python developer with React and Docker experience"
    keywords = ATSService.extract_keywords_from_job_description(jd)
    
    assert isinstance(keywords, list)
    assert "python" in keywords
    assert "react" in keywords or "docker" in keywords
