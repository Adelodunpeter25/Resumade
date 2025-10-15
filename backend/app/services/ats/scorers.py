"""Section scoring functions"""
from typing import Dict
from .keywords import ATS_KEYWORDS, normalize_text
from .validators import detect_quantifiable_achievements

def score_personal_info(personal_info: dict) -> Dict:
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

def score_experience(experience: list) -> Dict:
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
    normalized = normalize_text(all_text)
    action_verb_count = sum(1 for verb in ATS_KEYWORDS["action_verbs"] 
                           if verb in normalized)
    
    if action_verb_count >= 3:
        score += 8
    elif action_verb_count > 0:
        score += 4
        feedback.append("Use more action verbs (Developed, Led, Managed, Implemented)")
    else:
        feedback.append("Start bullet points with action verbs (Developed, Led, Managed)")
    
    # Check for quantifiable achievements
    achievement_count = sum(detect_quantifiable_achievements(
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

def score_education(education: list) -> Dict:
    """Score education section"""
    score = 0
    max_score = 15
    feedback = []
    
    if not education:
        feedback.append("Add education information")
        return {"score": 0, "max_score": max_score, "feedback": feedback}
    
    score += 10
    
    complete = all(edu.get("institution") and edu.get("degree") 
                 and edu.get("field_of_study") for edu in education)
    if complete:
        score += 5
    else:
        feedback.append("Complete education entries (institution, degree, field of study)")
    
    return {"score": score, "max_score": max_score, "feedback": feedback}

def score_skills(skills: list, job_description: str = None) -> Dict:
    """Score skills section"""
    from .keywords import extract_keywords_from_job_description, normalize_text
    
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
        jd_keywords = extract_keywords_from_job_description(job_description)
        skill_names = [normalize_text(s.get("name", "")) for s in skills]
        matches = sum(1 for kw in jd_keywords if any(kw in skill for skill in skill_names))
        
        if matches < 3:
            feedback.append(f"Add skills from job description: {', '.join(jd_keywords[:5])}")
    
    return {"score": score, "max_score": max_score, "feedback": feedback}

def score_certifications(certifications: list) -> Dict:
    """Score certifications section"""
    score = 5 if certifications else 0
    return {"score": score, "max_score": 5, "feedback": []}

def score_projects(projects: list) -> Dict:
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
