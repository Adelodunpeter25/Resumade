"""AI-powered content generation service for resume bullet points"""
import logging
from typing import List, Dict, Optional
import google.generativeai as genai
from app.core.config import settings
from app.core.cache import cached
from app.core.constants import CacheConstants

logger = logging.getLogger(__name__)

class AIContentService:
    """Service for AI-powered resume content generation"""
    
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.enabled = True
        else:
            self.enabled = False
            logger.warning("Gemini API key not found. AI content generation disabled.")
    
    @cached(CacheConstants.ATS_SCORE_CACHE_TTL)
    def generate_bullet_points(
        self, 
        position: str, 
        company: str, 
        current_description: str = "",
        seniority_level: str = "mid",
        industry: Optional[str] = None
    ) -> Dict:
        """Generate improved bullet points for experience/project descriptions"""
        if not self.enabled:
            return {
                "success": False,
                "error": "AI content generation is not available",
                "suggestions": []
            }
        
        try:
            prompt = self._build_bullet_prompt(
                position, 
                company, 
                current_description, 
                seniority_level,
                industry
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7,
                )
            )
            
            bullets = self._parse_bullets(response.text)
            
            return {
                "success": True,
                "suggestions": bullets,
                "count": len(bullets)
            }
            
        except Exception as e:
            logger.error(f"AI content generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": []
            }
    
    def improve_description(
        self,
        current_text: str,
        context: Dict
    ) -> Dict:
        """Improve existing description with AI suggestions"""
        if not self.enabled:
            return {
                "success": False,
                "error": "AI improvement is not available",
                "improved_text": current_text
            }
        
        try:
            prompt = f"""Improve this resume description to be more impactful and ATS-friendly:

Current description:
{current_text}

Context:
- Position: {context.get('position', 'N/A')}
- Company: {context.get('company', 'N/A')}
- Level: {context.get('seniority_level', 'mid')}

Requirements:
- Use strong action verbs
- Add quantifiable metrics where possible
- Keep it concise and impactful
- Make it ATS-friendly
- Maintain the same general meaning
- Format as bullet points if multiple achievements

Return ONLY the improved description, no explanations."""

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=400,
                    temperature=0.7,
                )
            )
            
            return {
                "success": True,
                "improved_text": response.text.strip(),
                "original_text": current_text
            }
            
        except Exception as e:
            logger.error(f"AI improvement error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "improved_text": current_text
            }
    
    def _build_bullet_prompt(
        self, 
        position: str, 
        company: str, 
        current_description: str,
        seniority_level: str,
        industry: Optional[str]
    ) -> str:
        """Build optimized prompt for bullet point generation"""
        
        level_guidance = {
            "entry": "Focus on learning, contributions, and growth. Use verbs like: Assisted, Supported, Contributed, Learned, Developed.",
            "mid": "Focus on ownership, impact, and results. Use verbs like: Led, Managed, Developed, Implemented, Optimized, Increased.",
            "senior": "Focus on strategy, leadership, and business impact. Use verbs like: Spearheaded, Architected, Drove, Transformed, Established, Scaled."
        }
        
        guidance = level_guidance.get(seniority_level, level_guidance["mid"])
        
        industry_context = f"\nIndustry: {industry}" if industry else ""
        current_context = f"\n\nCurrent description to improve:\n{current_description}" if current_description else ""
        
        return f"""Generate 5 professional, ATS-friendly resume bullet points for this role:

Position: {position}
Company: {company}
Seniority Level: {seniority_level}{industry_context}{current_context}

{guidance}

Requirements:
1. Start each bullet with a strong action verb
2. Include quantifiable metrics (numbers, percentages, timeframes) where realistic
3. Follow the STAR method: Action + Result
4. Keep each bullet under 150 characters
5. Make them specific and impactful
6. Ensure ATS compatibility (no special characters, simple formatting)
7. Vary the action verbs used

Format: Return ONLY the bullet points, one per line, starting with "• "
Do not include explanations, headers, or additional text.

Example format:
• Led cross-functional team of 8 engineers to deliver product feature, increasing user engagement by 35%
• Developed automated testing framework reducing QA time by 40% and improving code quality
• Optimized database queries improving application performance by 50% and reducing server costs by $20K annually"""

        return prompt
    
    def _parse_bullets(self, text: str) -> List[str]:
        """Parse AI response into clean bullet points"""
        lines = text.strip().split('\n')
        bullets = []
        
        for line in lines:
            line = line.strip()
            # Remove bullet markers and clean up
            if line:
                # Remove common bullet markers
                for marker in ['•', '-', '*', '–', '—']:
                    if line.startswith(marker):
                        line = line[1:].strip()
                        break
                
                # Remove numbering
                if line and line[0].isdigit() and '.' in line[:3]:
                    line = line.split('.', 1)[1].strip()
                
                if line and len(line) > 20:  # Minimum length check
                    bullets.append(line)
        
        return bullets[:5]  # Return max 5 bullets
    
    def generate_summary(
        self,
        position: str,
        years_experience: int,
        skills: List[str],
        industry: Optional[str] = None
    ) -> Dict:
        """Generate professional summary"""
        if not self.enabled:
            return {
                "success": False,
                "error": "AI summary generation is not available",
                "summary": ""
            }
        
        try:
            skills_text = ", ".join(skills[:8]) if skills else "various technical skills"
            industry_text = f" in {industry}" if industry else ""
            
            prompt = f"""Generate a compelling professional summary for a resume:

Position: {position}
Years of Experience: {years_experience}
Key Skills: {skills_text}
Industry: {industry_text}

Requirements:
- 2-3 sentences maximum
- Highlight key strengths and value proposition
- Include years of experience
- Mention 2-3 most relevant skills
- Make it impactful and ATS-friendly
- Use third person (no "I" or "my")

Return ONLY the summary text, no explanations or labels."""

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.7,
                )
            )
            
            return {
                "success": True,
                "summary": response.text.strip()
            }
            
        except Exception as e:
            logger.error(f"AI summary generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "summary": ""
            }
