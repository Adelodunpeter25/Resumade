"""Tests for ATS service caching"""
from unittest.mock import patch
from app.services.ats.ats_service import ATSService
from app.services.ats.keywords import normalize_text, extract_keywords_from_job_description
from app.core.cache import redis_cache


class TestATSServiceCache:
    """Test ATS service caching functionality"""
    
    def test_normalize_text_caching(self):
        """Test normalize_text function caching"""
        # Clear any existing cache
        redis_cache.clear_pattern("normalize_text*")
        
        test_text = "This is a TEST String with SPECIAL characters!@#"
        
        # First call
        result1 = normalize_text(test_text)
        
        # Second call should use cache
        result2 = normalize_text(test_text)
        
        assert result1 == result2
        assert result1 == "this is a test string with special characters"
    
    def test_extract_keywords_caching(self):
        """Test job description keyword extraction caching"""
        # Clear any existing cache
        redis_cache.clear_pattern("extract_keywords*")
        
        job_description = """
        We are looking for a Python developer with experience in FastAPI, 
        React, and PostgreSQL. The candidate should have strong problem-solving 
        skills and experience with cloud technologies like AWS.
        """
        
        # First call
        keywords1 = extract_keywords_from_job_description(job_description)
        
        # Second call should use cache
        keywords2 = extract_keywords_from_job_description(job_description)
        
        assert keywords1 == keywords2
        assert isinstance(keywords1, list)
        assert len(keywords1) > 0
    
    @patch('app.services.ats.ats_service._gemini_service')
    def test_calculate_ats_score_caching(self, mock_gemini):
        """Test ATS score calculation caching"""
        # Mock Gemini service
        mock_gemini.enhance_feedback.return_value = {
            "enhanced_feedback": "Test feedback",
            "ai_suggestions": ["Test suggestion"]
        }
        
        # Clear any existing cache
        redis_cache.clear_pattern("calculate_ats_score*")
        
        resume_data = {
            "personal_info": {
                "full_name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "location": "San Francisco, CA"
            },
            "experience": [
                {
                    "company": "Tech Corp",
                    "position": "Developer",
                    "start_date": "2020",
                    "end_date": "2023",
                    "description": "Developed applications"
                }
            ],
            "education": [
                {"institution": "University", "degree": "BS", "field": "CS"}
            ],
            "skills": [
                {"name": "Python"},
                {"name": "JavaScript"}
            ],
            "certifications": [],
            "projects": []
        }
        
        # First call
        result1 = ATSService.calculate_ats_score(resume_data)
        
        # Second call should use cache
        result2 = ATSService.calculate_ats_score(resume_data)
        
        assert result1 == result2
        assert "score" in result1
        assert "percentage" in result1
        assert "feedback" in result1
    
    def test_ats_score_different_params(self):
        """Test ATS score caching with different parameters"""
        resume_data = {
            "personal_info": {"full_name": "Jane Doe", "email": "jane@example.com"},
            "experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "projects": []
        }
        
        # Different role levels should produce different cache entries
        result_entry = ATSService.calculate_ats_score(resume_data, role_level="entry")
        result_senior = ATSService.calculate_ats_score(resume_data, role_level="senior")
        
        # Results should be different due to different weighting
        assert result_entry != result_senior
    
    def test_cache_invalidation_on_data_change(self):
        """Test that cache works correctly with different data"""
        resume_data1 = {
            "personal_info": {"full_name": "User One", "email": "user1@example.com"},
            "experience": [], "education": [], "skills": [], "certifications": [], "projects": []
        }
        
        resume_data2 = {
            "personal_info": {"full_name": "User Two", "email": "user2@example.com"},
            "experience": [], "education": [], "skills": [], "certifications": [], "projects": []
        }
        
        # Different data should produce different results
        result1 = ATSService.calculate_ats_score(resume_data1)
        result2 = ATSService.calculate_ats_score(resume_data2)
        
        # Should be cached separately
        assert result1 != result2
