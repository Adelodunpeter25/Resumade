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
    
    # Formatting issues to detect
    PROBLEMATIC_CHARS = r'[★☆♥♦●○◆◇■□▪▫]'
    
    @staticmethod
    def fuzzy_match(text: str, keyword: str, threshold: float = 0.85) -> bool:
        """Fuzzy string matching for keyword detection"""
        text = text.lower().strip()
        keyword = keyword.lower().strip()
        
        # Exact match
        if keyword in text:
            return True
        
        # Fuzzy match using sequence matcher
        ratio = SequenceMatcher(None, text, keyword).ratio()
        return ratio >= threshold
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for better matching"""
        if not text:
            return ""
        # Lowercase, remove extra spaces, remove punctuation
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
        
        # Filter for meaningful keywords (length > 3, not common words)
        common_words = {"the", "and", "for", "with", "this", "that", "from", "have", "will", "your"}
        keywords = [w for w in words if len(w) > 3 and w not in common_words]
        
        # Return unique keywords
        return list(set(keywords))[:20]
    
    @staticmethod
    def detect_quantifiable_achievements(text: str) -> int:
        """Detect quantified achievements in text"""
        if not text:
            return 0
        
        patterns = [
            r'\d+%',  # percentages
            r'\$\d+',  # dollar amounts
            r'\d+[kKmM]',  # thousands/millions
            r'increased by \d+',
            r'reduced by \d+',
            r'improved by \d+',
            r'saved \d+',
            r'\d+ users',
            r'\d+ customers'
        ]
        
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        
        return min(count, 5)  # Cap at 5
    
    @staticmethod
    def check_formatting_issues(resume_data: dict) -> Dict:
        """Check for ATS-unfriendly formatting"""
        issues = []
        
        personal_info = resume_data.get("personal_info", {})
        
        # Check for special characters
        name = personal_info.get("full_name", "")
        if re.search(ATSService.PROBLEMATIC_CHARS, name):
            issues.append("Remove special characters/emojis from name")
        
        # Check for proper email format
        email = personal_info.get("email", "")
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            issues.append("Email format may not be recognized")
        
        # Check for phone format
        phone = personal_info.get("phone", "")
        if phone and not re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', phone):
            issues.append("Use standard phone format (e.g., 123-456-7890)")
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues
        }
    
    @staticmethod
    def calculate_section_score(section_name: str, section_data: any, job_description: str = None) -> Dict:
        """Calculate score for individual section"""
        score = 0
        max_score = 0
        feedback = []
        
        if section_name == "personal_info":
            max_score = 20
            if section_data.get("full_name"):
                score += 5
            else:
                feedback.append("Add your full name")
            
            if section_data.get("email"):
                score += 5
            else:
                feedback.append("Add email address")
            
            if section_data.get("phone"):
                score += 5
            else:
                feedback.append("Add phone number")
            
            if section_data.get("location"):
                score += 3
            else:
                feedback.append("Add location (city, state)")
            
            if section_data.get("summary") and len(section_data["summary"]) > 50:
                score += 2
            else:
                feedback.append("Add professional summary (50+ characters)")
        
        elif section_name == "experience":
            max_score = 35
            if not section_data or len(section_data) == 0:
                feedback.append("Add work experience")
            else:
                score += 10  # Has experience
                
                # Check completeness
                complete_entries = sum(1 for exp in section_data 
                                     if exp.get("company") and exp.get("position") 
                                     and exp.get("start_date") and exp.get("description"))
                score += min(complete_entries * 3, 9)
                
                if complete_entries < len(section_data):
                    feedback.append("Complete all experience entries (company, position, dates, description)")
                
                # Check for action verbs
                all_text = " ".join([str(exp.get("description", "")) for exp in section_data])
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
                ) for exp in section_data)
                
                if achievement_count >= 3:
                    score += 8
                elif achievement_count > 0:
                    score += 4
                    feedback.append("Add more quantifiable achievements (e.g., 'Increased sales by 40%')")
                else:
                    feedback.append("Include measurable results (percentages, numbers, metrics)")
        
        elif section_name == "education":
            max_score = 15
            if not section_data or len(section_data) == 0:
                feedback.append("Add education information")
            else:
                score += 10
                
                # Check completeness
                complete = all(edu.get("institution") and edu.get("degree") 
                             and edu.get("field") for edu in section_data)
                if complete:
                    score += 5
                else:
                    feedback.append("Complete education entries (institution, degree, field of study)")
        
        elif section_name == "skills":
            max_score = 20
            skill_count = len(section_data) if section_data else 0
            
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
            
            # Check for technical keywords if job description provided
            if job_description and section_data:
                jd_keywords = ATSService.extract_keywords_from_job_description(job_description)
                skill_names = [ATSService.normalize_text(s.get("name", "")) for s in section_data]
                matches = sum(1 for kw in jd_keywords if any(kw in skill for skill in skill_names))
                
                if matches < 3:
                    feedback.append(f"Add skills from job description: {', '.join(jd_keywords[:5])}")
        
        elif section_name == "certifications":
            max_score = 5
            if section_data and len(section_data) > 0:
                score += 5
        
        elif section_name == "projects":
            max_score = 5
            if section_data and len(section_data) > 0:
                score += 3
                # Check for technical details
                has_tech = any(proj.get("technologies") for proj in section_data)
                if has_tech:
                    score += 2
                else:
                    feedback.append("Add technologies used in projects")
        
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score * 100), 1) if max_score > 0 else 0,
            "feedback": feedback
        }
    
    @staticmethod
    def calculate_ats_score(resume_data: dict, job_description: str = None, role_level: str = "mid") -> Dict:
        """
        Calculate comprehensive ATS score with dynamic weighting
        
        Args:
            resume_data: Resume data dictionary
            job_description: Optional job description for context-aware scoring
            role_level: Job level (entry, mid, senior) for dynamic weighting
        """
        
        # Dynamic weights based on role level
        weights = {
            "entry": {"personal_info": 0.20, "experience": 0.25, "education": 0.25, "skills": 0.20, "certifications": 0.05, "projects": 0.05},
            "mid": {"personal_info": 0.15, "experience": 0.35, "education": 0.15, "skills": 0.25, "certifications": 0.05, "projects": 0.05},
            "senior": {"personal_info": 0.10, "experience": 0.45, "education": 0.10, "skills": 0.25, "certifications": 0.05, "projects": 0.05}
        }
        
        weight_set = weights.get(role_level, weights["mid"])
        
        # Calculate section scores
        sections = {
            "personal_info": resume_data.get("personal_info", {}),
            "experience": resume_data.get("experience", []),
            "education": resume_data.get("education", []),
            "skills": resume_data.get("skills", []),
            "certifications": resume_data.get("certifications", []),
            "projects": resume_data.get("projects", [])
        }
        
        section_scores = {}
        total_weighted_score = 0
        all_feedback = []
        
        for section_name, section_data in sections.items():
            section_result = ATSService.calculate_section_score(section_name, section_data, job_description)
            section_scores[section_name] = section_result
            
            # Apply weight
            weighted_score = (section_result["score"] / section_result["max_score"]) * weight_set[section_name] * 100
            total_weighted_score += weighted_score
            
            # Collect feedback
            if section_result["feedback"]:
                all_feedback.extend([f"{section_name.replace('_', ' ').title()}: {fb}" for fb in section_result["feedback"]])
        
        # Check formatting
        formatting = ATSService.check_formatting_issues(resume_data)
        if formatting["has_issues"]:
            all_feedback.extend(formatting["issues"])
            total_weighted_score -= 5  # Penalty for formatting issues
        
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
            "feedback": all_feedback[:10],  # Top 10 feedback items
            "section_breakdown": {
                name: {
                    "score": result["score"],
                    "max_score": result["max_score"],
                    "percentage": result["percentage"]
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
        
        # Extract current skills
        current_skills = [ATSService.normalize_text(s.get("name", "")) 
                         for s in resume_data.get("skills", [])]
        
        # If job description provided, prioritize those keywords
        if job_description:
            jd_keywords = ATSService.extract_keywords_from_job_description(job_description)
            for kw in jd_keywords[:10]:
                if not any(ATSService.fuzzy_match(skill, kw) for skill in current_skills):
                    suggestions.append(kw)
        
        # Add common technical keywords not in resume
        for category, keywords in ATSService.ATS_KEYWORDS.items():
            if category == "technical":
                for main_kw, variants in keywords.items():
                    if not any(any(ATSService.fuzzy_match(skill, var) for var in variants) 
                             for skill in current_skills):
                        suggestions.append(main_kw)
                        if len(suggestions) >= 15:
                            break
        
        return suggestions[:15]
