"""Main ATS service orchestrating scoring and analysis"""

from typing import Dict
from app.core.constants import ATSConstants, CacheConstants
from app.core.cache import cached
from .keywords import (
    normalize_text,
    extract_keywords_from_job_description,
    get_keyword_suggestions,
)
from .validators import check_formatting_issues
from .gemini_service import GeminiService
from .scorers import (
    score_personal_info,
    score_experience,
    score_education,
    score_skills,
    score_certifications,
    score_projects,
)

# Initialize Gemini service
_gemini_service = GeminiService()


class ATSService:
    """Enhanced ATS compatibility checking and resume scoring"""

    @staticmethod
    @cached(CacheConstants.ATS_SCORE_CACHE_TTL)
    def calculate_ats_score(
        resume_data: dict, job_description: str = None, role_level: str = "mid"
    ) -> Dict:
        """Calculate comprehensive ATS score with dynamic weighting"""

        # Get weights based on role level
        weight_set = ATSConstants.ROLE_WEIGHTS.get(
            role_level, ATSConstants.ROLE_WEIGHTS["mid"]
        )

        # Score each section
        section_scores = {
            "personal_info": score_personal_info(resume_data.get("personal_info", {})),
            "experience": score_experience(resume_data.get("experience", [])),
            "education": score_education(resume_data.get("education", [])),
            "skills": score_skills(resume_data.get("skills", []), job_description),
            "certifications": score_certifications(
                resume_data.get("certifications", [])
            ),
            "projects": score_projects(resume_data.get("projects", [])),
        }

        # Calculate weighted score
        total_weighted_score = 0
        all_feedback = []

        for section_name, section_result in section_scores.items():
            weighted_score = (
                (section_result["score"] / section_result["max_score"])
                * weight_set[section_name]
                * 100
            )
            total_weighted_score += weighted_score

            if section_result["feedback"]:
                all_feedback.extend(
                    [
                        f"{section_name.replace('_', ' ').title()}: {fb}"
                        for fb in section_result["feedback"]
                    ]
                )

        # Limit feedback items
        all_feedback = all_feedback[: ATSConstants.MAX_FEEDBACK_ITEMS]

        # Check formatting
        formatting = check_formatting_issues(resume_data)
        if formatting["has_issues"]:
            all_feedback.extend(formatting["issues"])
            total_weighted_score -= 5

        # Format feedback as bullet points
        all_feedback = [
            f"• {fb}" if not fb.startswith("•") else fb for fb in all_feedback
        ]

        # Job description matching bonus
        if job_description:
            jd_keywords = extract_keywords_from_job_description(job_description)
            resume_text = normalize_text(str(resume_data))
            matches = sum(1 for kw in jd_keywords if kw in resume_text)
            match_bonus = min(matches * 0.5, 5)
            total_weighted_score += match_bonus

            if matches < len(jd_keywords) * ATSConstants.JD_MATCH_THRESHOLD:
                all_feedback.append(
                    f"• Tailor resume to job description - include keywords: {', '.join(jd_keywords[:5])}"
                )

        final_score = max(0, min(100, total_weighted_score))

        # Get AI-enhanced feedback
        ai_feedback = _gemini_service.enhance_feedback(
            resume_data, final_score, all_feedback
        )

        return {
            "score": round(final_score, 1),
            "max_score": 100,
            "percentage": round(final_score, 1),
            "grade": ATSService._get_grade(final_score),
            "feedback": all_feedback,
            "ai_feedback": ai_feedback.get("enhanced_feedback"),
            "ai_suggestions": ai_feedback.get("ai_suggestions", []),
            "section_breakdown": {
                name: {
                    "score": result["score"],
                    "max_score": result["max_score"],
                    "percentage": round(
                        (result["score"] / result["max_score"] * 100), 1
                    )
                    if result["max_score"] > 0
                    else 0,
                }
                for name, result in section_scores.items()
            },
            "formatting_check": formatting,
        }

    @staticmethod
    def _get_grade(score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    @staticmethod
    def get_keyword_suggestions(resume_data: dict, job_description: str = None) -> list:
        """Suggest keywords to improve ATS compatibility"""
        return get_keyword_suggestions(resume_data, job_description)
