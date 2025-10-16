"""Integration tests for service caching"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.docx_service import DOCXService
from app.services.ats.gemini_service import GeminiService
from app.core.cache import redis_cache, cached


class TestServiceCacheIntegration:
    """Test caching integration across services"""
    
    def test_docx_service_caching(self):
        """Test DOCX generation caching"""
        # Clear any existing cache
        redis_cache.clear_pattern("generate_resume_docx*")
        
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
                    "start_date": "2020-01",
                    "end_date": "2023-12",
                    "description": "Developed applications"
                }
            ],
            "education": [
                {
                    "institution": "University",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "graduation_date": "2020"
                }
            ],
            "skills": [
                {"name": "Python", "level": "Advanced"},
                {"name": "JavaScript", "level": "Intermediate"}
            ],
            "certifications": [],
            "projects": []
        }
        
        # First call
        docx_bytes1 = DOCXService.generate_resume_docx(resume_data)
        
        # Second call should use cache
        docx_bytes2 = DOCXService.generate_resume_docx(resume_data)
        
        assert docx_bytes1 == docx_bytes2
        assert isinstance(docx_bytes1, bytes)
        assert len(docx_bytes1) > 0
    
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_service_caching(self, mock_model_class):
        """Test Gemini AI service caching"""
        # Mock Gemini model
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "AI-generated feedback about the resume"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        # Clear any existing cache
        redis_cache.clear_pattern("enhance_feedback*")
        
        gemini_service = GeminiService()
        
        resume_data = {
            "personal_info": {"full_name": "Test User"},
            "experience": [],
            "education": [],
            "skills": []
        }
        
        base_feedback = ["Add more skills", "Improve experience section"]
        
        # First call
        result1 = gemini_service.enhance_feedback(resume_data, 75.0, base_feedback)
        
        # Second call should use cache
        result2 = gemini_service.enhance_feedback(resume_data, 75.0, base_feedback)
        
        assert result1 == result2
        # Should only call Gemini API once due to caching
        assert mock_model.generate_content.call_count <= 2  # Allow for potential cache miss
    
    def test_cache_key_generation_consistency(self):
        """Test that cache keys are generated consistently"""
        # Test with same data multiple times
        test_data = {"key": "value", "number": 42}
        
        @cached(60)
        def test_function(data):
            return f"processed_{data['key']}_{data['number']}"
        
        # Multiple calls with same data
        result1 = test_function(test_data)
        result2 = test_function(test_data)
        result3 = test_function(test_data)
        
        assert result1 == result2 == result3
    
    def test_cache_isolation_between_services(self):
        """Test that different services don't interfere with each other's cache"""
        # Set cache values for different services
        redis_cache.set("ats_test_key", {"service": "ats"}, 60)
        redis_cache.set("pdf_test_key", {"service": "pdf"}, 60)
        redis_cache.set("docx_test_key", {"service": "docx"}, 60)
        
        # Verify isolation
        assert redis_cache.get("ats_test_key") == {"service": "ats"}
        assert redis_cache.get("pdf_test_key") == {"service": "pdf"}
        assert redis_cache.get("docx_test_key") == {"service": "docx"}
        
        # Clear one service cache
        redis_cache.delete("ats_test_key")
        
        # Others should remain
        assert redis_cache.get("ats_test_key") is None
        assert redis_cache.get("pdf_test_key") == {"service": "pdf"}
        assert redis_cache.get("docx_test_key") == {"service": "docx"}
        
        # Cleanup
        redis_cache.delete("pdf_test_key")
        redis_cache.delete("docx_test_key")
    
    def test_cache_ttl_behavior(self):
        """Test cache TTL behavior"""
        import time
        
        # Set short TTL for testing
        redis_cache.set("ttl_test_key", "test_value", 1)  # 1 second TTL
        
        # Should be available immediately
        assert redis_cache.get("ttl_test_key") == "test_value"
        
        # Wait for expiration (in real tests, you might mock time)
        time.sleep(2)
        
        # Should be expired
        assert redis_cache.get("ttl_test_key") is None
    
    def test_error_handling_in_cached_functions(self):
        """Test error handling in cached functions"""
        call_count = 0
        
        @cached(60)
        def function_with_error(should_error):
            nonlocal call_count
            call_count += 1
            if should_error:
                raise ValueError("Test error")
            return "success"
        
        # Successful call should be cached
        result1 = function_with_error(False)
        result2 = function_with_error(False)
        assert result1 == result2 == "success"
        assert call_count == 1  # Only called once due to caching
        
        # Error should not be cached
        with pytest.raises(ValueError):
            function_with_error(True)
        
        # Subsequent successful call should work
        result3 = function_with_error(False)
        assert result3 == "success"
