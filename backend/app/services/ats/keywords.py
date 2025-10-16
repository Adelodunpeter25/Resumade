"""Keyword extraction and matching utilities"""
import re
from typing import List
from difflib import SequenceMatcher
from app.core.constants import ATSConstants, CacheConstants
from app.core.cache import cached

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

@cached(CacheConstants.KEYWORD_CACHE_TTL)
def normalize_text(text: str) -> str:
    """Normalize text for better matching"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@cached(CacheConstants.KEYWORD_CACHE_TTL)
def extract_keywords_from_job_description(job_description: str) -> List[str]:
    """Extract key terms from job description"""
    if not job_description:
        return []
    
    normalized = normalize_text(job_description)
    words = normalized.split()
    
    common_words = {"the", "and", "for", "with", "this", "that", "from", "have", "will", "your"}
    keywords = [w for w in words if len(w) > 3 and w not in common_words]
    
    return list(set(keywords))[:ATSConstants.MAX_JD_KEYWORDS]

def fuzzy_match(text: str, keyword: str, threshold: float = ATSConstants.FUZZY_MATCH_THRESHOLD) -> bool:
    """Fuzzy string matching for keyword detection"""
    text = text.lower().strip()
    keyword = keyword.lower().strip()
    
    if keyword in text:
        return True
    
    ratio = SequenceMatcher(None, text, keyword).ratio()
    return ratio >= threshold

def get_keyword_suggestions(resume_data: dict, job_description: str = None) -> List[str]:
    """Suggest keywords to improve ATS compatibility"""
    suggestions = []
    
    current_skills = [normalize_text(s.get("name", "")) 
                     for s in resume_data.get("skills", [])]
    
    if job_description:
        jd_keywords = extract_keywords_from_job_description(job_description)
        for kw in jd_keywords[:10]:
            if not any(fuzzy_match(skill, kw) for skill in current_skills):
                suggestions.append(kw)
    
    for category, keywords in ATS_KEYWORDS.items():
        if category == "technical":
            for main_kw, variants in keywords.items():
                if not any(any(fuzzy_match(skill, var) for var in variants) 
                         for skill in current_skills):
                    suggestions.append(main_kw)
                    if len(suggestions) >= 15:
                        break
    
    return suggestions[:15]
