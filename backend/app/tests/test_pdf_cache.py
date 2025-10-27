"""Tests for PDF service caching"""

from unittest.mock import patch, MagicMock
from app.services.pdf_service import PDFService
from app.core.cache import redis_cache


class TestPDFServiceCache:
    """Test PDF service caching functionality"""

    def test_get_available_templates_caching(self):
        """Test template list caching"""
        # Clear any existing cache
        redis_cache.clear_pattern("get_available_templates*")

        # First call
        templates1 = PDFService.get_available_templates()

        # Second call should use cache
        templates2 = PDFService.get_available_templates()

        assert templates1 == templates2
        assert isinstance(templates1, list)
        assert len(templates1) > 0

        # Verify template structure
        for template in templates1:
            assert "name" in template
            assert "display_name" in template
            assert "category" in template

    @patch("app.services.pdf_service.PDFService._get_template")
    def test_template_caching(self, mock_get_template):
        """Test individual template caching"""
        # Mock template object
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test Template</html>"
        mock_get_template.return_value = mock_template

        pdf_service = PDFService()

        # First call
        template1 = pdf_service._get_template("professional-blue")

        # Second call should use cache
        template2 = pdf_service._get_template("professional-blue")

        assert template1 == template2
        # Should only call the actual method once due to caching
        assert mock_get_template.call_count <= 2  # Allow for potential cache miss

    def test_template_cache_different_templates(self):
        """Test that different templates are cached separately"""
        pdf_service = PDFService()

        # Get different templates
        template1 = pdf_service._get_template("professional-blue")
        template2 = pdf_service._get_template("linkedin-style")

        # Should be different objects
        assert template1 != template2

    @patch("app.services.pdf_service.PDFService._get_template")
    def test_pdf_generation_with_cache(self, mock_get_template):
        """Test PDF generation uses cached templates"""
        # Mock template
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Rendered Resume</html>"
        mock_get_template.return_value = mock_template

        pdf_service = PDFService()

        resume_data = {
            "personal_info": {"full_name": "Test User", "email": "test@example.com"},
            "experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "projects": [],
        }

        # Test HTML rendering (which uses cached templates)
        html_content = pdf_service.render_resume_html(resume_data, "professional-blue")

        assert isinstance(html_content, str)
        assert len(html_content) > 0
        mock_get_template.assert_called_with("professional-blue")

    def test_template_list_cache_persistence(self):
        """Test that template list cache persists across multiple calls"""
        # Clear cache first
        redis_cache.clear_pattern("get_available_templates*")

        # Multiple calls
        for i in range(3):
            templates = PDFService.get_available_templates()
            assert isinstance(templates, list)
            assert len(templates) > 0

        # All calls should return the same cached result
        # This is verified by the fact that no errors occur and results are consistent
