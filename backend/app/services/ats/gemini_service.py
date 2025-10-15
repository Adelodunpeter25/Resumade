"""Gemini AI integration for enhanced ATS feedback"""
import logging
from typing import Dict
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for Gemini AI-powered resume analysis"""
    
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.enabled = True
        else:
            self.enabled = False
            logger.warning("Gemini API key not found. AI-enhanced feedback disabled.")
    
    def enhance_feedback(self, resume_data: dict, base_score: float, base_feedback: list) -> Dict:
        """Enhance ATS feedback with AI-generated insights"""
        if not self.enabled:
            return {"enhanced_feedback": None, "ai_suggestions": []}
        
        try:
            prompt = self._build_prompt(resume_data, base_score, base_feedback)
            response = self.model.generate_content(prompt)
            
            return {
                "enhanced_feedback": response.text,
                "ai_suggestions": self._parse_suggestions(response.text)
            }
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return {"enhanced_feedback": None, "ai_suggestions": []}
    
    def _build_prompt(self, resume_data: dict, score: float, feedback: list) -> str:
        """Build prompt for Gemini"""
        personal_info = resume_data.get("personal_info", {})
        experience_count = len(resume_data.get("experience", []))
        education_count = len(resume_data.get("education", []))
        skills_count = len(resume_data.get("skills", []))
        certifications_count = len(resume_data.get("certifications", []))
        projects_count = len(resume_data.get("projects", []))
        
        return f"""Analyze this resume for ATS optimization. Current ATS score: {score}%

Resume Summary:
- Name: {personal_info.get('full_name', 'N/A')}
- Experience entries: {experience_count}
- Education entries: {education_count}
- Skills: {skills_count}
- Certifications: {certifications_count}
- Projects: {projects_count}

Current Issues:
{chr(10).join(feedback)}

Provide exactly 4-6 specific, actionable recommendations to improve the ATS score. Cover ALL major resume sections:
1. Personal Information (summary, contact details)
2. Experience (work history, achievements)
3. Education (degrees, institutions)
4. Skills (technical and soft skills)
5. Additional sections (certifications, projects) if applicable

IMPORTANT FORMATTING RULES:
- Write in clear, conversational language
- Use numbered lists (1., 2., 3., etc.) for main recommendations
- Use bullet points (•) for sub-points under each recommendation
- DO NOT use asterisks (*) or markdown bold formatting
- Keep explanations concise and practical
- Each recommendation should have 2-3 bullet points with actionable steps

Format example:
1. Personal Information recommendation
   • Specific action to take
   • Why this improves ATS score

2. Experience section recommendation
   • Action step
   • Expected impact"""
    
    def _parse_suggestions(self, text: str) -> list:
        """Parse AI response into list of suggestions"""
        lines = text.strip().split('\n')
        suggestions = []
        for line in lines:
            line = line.strip()
            if line and line[0].isdigit() and '.' in line[:3]:
                clean = line.split('.', 1)[1].strip()
                if clean and not clean.startswith('•'):
                    suggestions.append(clean)
        return suggestions[:6]
