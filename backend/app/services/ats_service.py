import re
from typing import Dict, List, Optional
from difflib import SequenceMatcher

class ATSService:
    """Enhanced ATS compatibility checking and resume scoring"""
    
    # Expanded keyword database with synonyms
    ATS_KEYWORDS = {
        "technical": {
            "python": ["python", "py", "python3"],
            "javascript": ["javascript", "js", "node.js", "nodejs", "node"],
            "react": ["react", "reactjs", "react.js"],
            "java": ["java", "jdk"],
            "sql": ["sql", "mysql", "postgresql", "postgres"],
            "aws": ["aws", "amazon web services"],
            "docker": ["docker", "containerization"],
            "kubernetes": ["kubernetes", "k8s"],
        },
        "soft_skills": {
            "leadership": ["leadership", "led", "managed", "supervised", "directed"],
            "communication": ["communication", "presented", "collaborated"],
            "teamwork": ["teamwork", "team player", "collaboration"],
            "problem-solving": ["problem-solving", "troubleshooting", "debugging"],
            "analytical": ["analytical", "analysis", "data-driven"]
        },
        "action_verbs": [
            "developed", "managed", "led", "implemented", "designed", "created", 
            "improved", "increased", "reduced", "achieved", "delivered", "built",
            "launched", "optimized", "streamlined", "coordinated", "established"
        ]
    }
    
    PROBLEMATIC_CHARS = r'[★☆♥♦●○◆◇■□▪▫]'
    
    # ==================== UTILITY METHODS ====================
    
    @staticmethod
    def fuzzy_match(text: str, keyword: str, threshold: float = 0.85) -> bool:
        """Fuzzy string matching for keyword detection"""
        text = text.lower().strip()
        keyword = keyword.lower().strip()
        
        if keyword in text:
            return True
        
        ratio = SequenceMatcher(None, text, keyword).ratio()
        return ratio >= threshold
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for better matching"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def extract_keywords_from_job_description(job_description: str) -> List[str]:
        """Extract key terms from job description"""
        if not job_description:
            return []
        
        normalized = ATSService.normalize_text(job_description)
        words = normalized.split()
        
        common_words = {"the", "and", "for", "with", "this", "that", "from", "have", "will", "your"}
        keywords = [w for w in words if len(w) > 3 and w not in common_words]
        
        return list(set(keywords))[:20]
    
    @staticmethod
    def detect_quantifiable_achievements(text: str) -> int:
        """Detect quantified achievements in text"""
        if not text:
            return 0
        
        patterns = [
            r'\d+%', r'\$\d+', r'\d+[kKmM]', r'increased by \d+',
            r'reduced by \d+', r'improved by \d+', r'saved \d+',
            r'\d+ users', r'\d+ customers'
        ]
        
        count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
        return min(count, 5)
    
    # ==================== VALIDATION METHODS ====================
    
    @staticmethod
    def check_formatting_issues(resume_data: dict) -> Dict:
        """Check for ATS-unfriendly formatting"""
        issues = []
        personal_info = resume_data.get("personal_info", {})
        
        # Check name
        name = personal_info.get("full_name", "")
        if re.search(ATSService.PROBLEMATIC_CHARS, name):
            issues.append("Remove special characters/emojis from name")
        
        # Check email
        email = personal_info.get("email", "")
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            issues.append("Email format may not be recognized")
        
        # Check phone
        phone = personal_info.get("phone", "")
        if phone and not re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', phone):
            issues.append("Use standard phone format (e.g., 123-456-7890)")
        
        return {"has_issues": len(issues) > 0, "issues": issues}
    
    # ==================== SECTION SCORING METHODS ====================
    
    @staticmethod
    def _score_personal_info(personal_info: dict) -> Dict:
        """Score personal info section"""
        score = 0
        max_score = 20
        feedback = []
        
        if personal_info.get("full_name"):
            score += 5
        else:
            feedback.append("Add your full name")
        
        if personal_info.get("email"):
            score += 5
        else:
            feedback.append("Add email address")
        
        if personal_info.get("phone"):
            score += 5
        else:
            feedback.append("Add phone number")
        
        if personal_info.get("location"):
            score += 3
        else:
            feedback.append("Add location (city, state)")
        
        if personal_info.get("summary") and len(personal_info["summary"]) > 50:
            score += 2
        else:
            feedback.append("Add professional summary (50+ characters)")
        
        return {"score": score, "max_score": max_score, "feedback": feedback}
    
    @staticmethod
    def _score_experience(experience: list) -> Dict:
        """Score experience section"""
        score = 0
        max_score = 35
        feedback = []
        
        if not experience:
            feedback.append("Add work experience")
            return {"score": 0, "max_score": max_score, "feedback": feedback}
        
        score += 10  # Has experience
        
        # Check completeness
        complete_entries = sum(1 for exp in experience 
                             if exp.get("company") and exp.get("position") 
                             and exp.get("start_date") and exp.get("description"))
        score += min(complete_entries * 3, 9)
        
        if complete_entries < len(experience):
            feedback.append("Complete all experience entries (company, position, dates, description)")
        
        # Check for action verbs
        all_text = " ".join([str(exp.get("description", "")) for exp in experience])
        normalized = ATSService.normalize_text(all_text)
        action_verb_count = sum(1 for verb in ATSService.ATS_KEYWORDS["action_verbs"] 
                               if verb in normalized)
        
        if action_verb_count >= 3:
            score += 8
        elif action_verb_count > 0:
            score += 4
            feedback.append("Use more action verbs (Developed, Led, Managed, Implemented)")
        else:
            feedback.append("Start bullet points with action verbs (Developed, Led, Managed)")
        
        # Check for quantifiable achievements
        achievement_count = sum(ATSService.detect_quantifiable_achievements(
            str(exp.get("description", "")) + " ".join(exp.get("achievements", []))
        ) for exp in experience)
        
        if achievement_count >= 3:
            score += 8
        elif achievement_count > 0:
            score += 4
            feedback.append("Add more quantifiable achievements (e.g., 'Increased sales by 40%')")
        else:
            feedback.append("Include measurable results (percentages, numbers, metrics)")
        
        return {"score": score, "max_score": max_score, "feedback": feedback}
    
    @staticmethod
    def _score_education(education: list) -> Dict:
        """Score education section"""
        score = 0
        max_score = 15
        feedback = []
        
        if not education:
            feedback.append("Add education information")
            return {"score": 0, "max_score": max_score, "feedback": feedback}
        
        score += 10
        
        complete = all(edu.get("institution") and edu.get("degree") 
                     and edu.get("field") for edu in education)
        if complete:
            score += 5
        else:
            feedback.append("Complete education entries (institution, degree, field of study)")
        
        return {"score": score, "max_score": max_score, "feedback": feedback}
    
    @staticmethod
    def _score_skills(skills: list, job_description: str = None) -> Dict:
        """Score skills section"""
        score = 0
        max_score = 20
        feedback = []
        skill_count = len(skills) if skills else 0
        
        if skill_count == 0:
            feedback.append("Add relevant skills (aim for 8-12 skills)")
        elif skill_count < 5:
            score += 8
            feedback.append(f"Add more skills (current: {skill_count}, recommended: 8-12)")
        elif skill_count < 8:
            score += 15
            feedback.append("Consider adding 2-3 more relevant skills")
        else:
            score += 20
        
        # Check for job description match
        if job_description and skills:
            jd_keywords = ATSService.extract_keywords_from_job_description(job_description)
            skill_names = [ATSService.normalize_text(s.get("name", "")) for s in skills]
            matches = sum(1 for kw in jd_keywords if any(kw in skill for skill in skill_names))
            
            if matches < 3:
                feedback.append(f"Add skills from job description: {', '.join(jd_keywords[:5])}")
        
        return {"score": score, "max_score": max_score, "feedback": feedback}
    
    @staticmethod
    def _score_certifications(certifications: list) -> Dict:
        """Score certifications section"""
        score = 5 if certifications else 0
        return {"score": score, "max_score": 5, "feedback": []}
    
    @staticmethod
    def _score_projects(projects: list) -> Dict:
        """Score projects section"""
        score = 0
        max_score = 5
        feedback = []
        
        if not projects:
            return {"score": 0, "max_score": max_score, "feedback": feedback}
        
        score += 3
        has_tech = any(proj.get("technologies") for proj in projects)
        if has_tech:
            score += 2
        else:
            feedback.append("Add technologies used in projects")
        
        return {"score": score, "max_score": max_score, "feedback": feedback}
    
    # ==================== MAIN SCORING METHOD ====================
    
    @staticmethod
    def calculate_ats_score(resume_data: dict, job_description: str = None, role_level: str = "mid") -> Dict:
        """Calculate comprehensive ATS score with dynamic weighting"""
        
        # Dynamic weights based on role level
        weights = {
            "entry": {"personal_info": 0.20, "experience": 0.25, "education": 0.25, "skills": 0.20, "certifications": 0.05, "projects": 0.05},
            "mid": {"personal_info": 0.15, "experience": 0.35, "education": 0.15, "skills": 0.25, "certifications": 0.05, "projects": 0.05},
            "senior": {"personal_info": 0.10, "experience": 0.45, "education": 0.10, "skills": 0.25, "certifications": 0.05, "projects": 0.05}
        }
        
        weight_set = weights.get(role_level, weights["mid"])
        
        # Score each section
        section_scores = {
            "personal_info": ATSService._score_personal_info(resume_data.get("personal_info", {})),
            "experience": ATSService._score_experience(resume_data.get("experience", [])),
            "education": ATSService._score_education(resume_data.get("education", [])),
            "skills": ATSService._score_skills(resume_data.get("skills", []), job_description),
            "certifications": ATSService._score_certifications(resume_data.get("certifications", [])),
            "projects": ATSService._score_projects(resume_data.get("projects", []))
        }
        
        # Calculate weighted score
        total_weighted_score = 0
        all_feedback = []
        
        for section_name, section_result in section_scores.items():
            weighted_score = (section_result["score"] / section_result["max_score"]) * weight_set[section_name] * 100
            total_weighted_score += weighted_score
            
            if section_result["feedback"]:
                all_feedback.extend([f"{section_name.replace('_', ' ').title()}: {fb}" for fb in section_result["feedback"]])
        
        # Check formatting
        formatting = ATSService.check_formatting_issues(resume_data)
        if formatting["has_issues"]:
            all_feedback.extend(formatting["issues"])
            total_weighted_score -= 5
        
        # Job description matching bonus
        if job_description:
            jd_keywords = ATSService.extract_keywords_from_job_description(job_description)
            resume_text = ATSService.normalize_text(str(resume_data))
            matches = sum(1 for kw in jd_keywords if kw in resume_text)
            match_bonus = min(matches * 0.5, 5)
            total_weighted_score += match_bonus
            
            if matches < len(jd_keywords) * 0.3:
                all_feedback.append(f"Tailor resume to job description - include keywords: {', '.join(jd_keywords[:5])}")
        
        final_score = max(0, min(100, total_weighted_score))
        
        return {
            "score": round(final_score, 1),
            "max_score": 100,
            "percentage": round(final_score, 1),
            "grade": ATSService._get_grade(final_score),
            "feedback": all_feedback[:10],
            "section_breakdown": {
                name: {
                    "score": result["score"],
                    "max_score": result["max_score"],
                    "percentage": round((result["score"] / result["max_score"] * 100), 1) if result["max_score"] > 0 else 0
                }
                for name, result in section_scores.items()
            },
            "formatting_check": formatting
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
    def get_keyword_suggestions(resume_data: dict, job_description: str = None) -> List[str]:
        """Suggest keywords to improve ATS compatibility"""
        suggestions = []
        
        current_skills = [ATSService.normalize_text(s.get("name", "")) 
                         for s in resume_data.get("skills", [])]
        
        if job_description:
            jd_keywords = ATSService.extract_keywords_from_job_description(job_description)
            for kw in jd_keywords[:10]:
                if not any(ATSService.fuzzy_match(skill, kw) for skill in current_skills):
                    suggestions.append(kw)
        
        for category, keywords in ATSService.ATS_KEYWORDS.items():
            if category == "technical":
                for main_kw, variants in keywords.items():
                    if not any(any(ATSService.fuzzy_match(skill, var) for var in variants) 
                             for skill in current_skills):
                        suggestions.append(main_kw)
                        if len(suggestions) >= 15:
                            break
        
        return suggestions[:15]
