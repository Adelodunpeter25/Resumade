"""Application constants and configuration values"""

class ScoringConfig:
    """ATS Scoring configuration"""
    # Personal Info
    PERSONAL_INFO_MAX_SCORE = 20
    PERSONAL_INFO_NAME_SCORE = 5
    PERSONAL_INFO_EMAIL_SCORE = 5
    PERSONAL_INFO_PHONE_SCORE = 5
    PERSONAL_INFO_LOCATION_SCORE = 3
    PERSONAL_INFO_SUMMARY_SCORE = 2
    PERSONAL_INFO_SUMMARY_MIN_LENGTH = 50
    
    # Experience
    EXPERIENCE_MAX_SCORE = 35
    EXPERIENCE_BASE_SCORE = 10
    EXPERIENCE_COMPLETE_ENTRY_SCORE = 3
    EXPERIENCE_ACTION_VERBS_FULL_SCORE = 8
    EXPERIENCE_ACTION_VERBS_PARTIAL_SCORE = 4
    EXPERIENCE_ACHIEVEMENTS_FULL_SCORE = 8
    EXPERIENCE_ACHIEVEMENTS_PARTIAL_SCORE = 4
    EXPERIENCE_MIN_ACTION_VERBS = 3
    EXPERIENCE_MIN_ACHIEVEMENTS = 3
    
    # Education
    EDUCATION_MAX_SCORE = 15
    EDUCATION_BASE_SCORE = 10
    EDUCATION_COMPLETE_SCORE = 5
    
    # Skills
    SKILLS_MAX_SCORE = 20
    SKILLS_MINIMAL_COUNT = 5
    SKILLS_RECOMMENDED_COUNT = 8
    SKILLS_OPTIMAL_COUNT = 12
    SKILLS_MINIMAL_SCORE = 8
    SKILLS_GOOD_SCORE = 15
    SKILLS_FULL_SCORE = 20
    SKILLS_JD_MATCH_THRESHOLD = 3
    
    # Certifications & Projects
    CERTIFICATIONS_MAX_SCORE = 5
    PROJECTS_MAX_SCORE = 5
    PROJECTS_BASE_SCORE = 3
    PROJECTS_TECH_SCORE = 2
    
    # General
    MAX_TOTAL_SCORE = 100
    MAX_FEEDBACK_ITEMS = 10
    FUZZY_MATCH_THRESHOLD = 0.85
    FORMATTING_PENALTY = 5
    JD_MATCH_BONUS_PER_KEYWORD = 0.5
    JD_MATCH_MAX_BONUS = 5
    JD_MATCH_MIN_PERCENTAGE = 0.3
    MAX_ACHIEVEMENT_COUNT = 5
    MAX_KEYWORD_SUGGESTIONS = 15
    MAX_JD_KEYWORDS = 20

class ValidationConfig:
    """Input validation limits"""
    MAX_RESUME_TITLE_LENGTH = 200
    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 2
    MAX_EMAIL_LENGTH = 255
    MAX_PHONE_LENGTH = 20
    MAX_LOCATION_LENGTH = 200
    MAX_SUMMARY_LENGTH = 2000
    MAX_DESCRIPTION_LENGTH = 5000
    MAX_EXPERIENCE_ITEMS = 20
    MAX_EDUCATION_ITEMS = 10
    MAX_SKILLS_ITEMS = 50
    MAX_CERTIFICATIONS_ITEMS = 20
    MAX_PROJECTS_ITEMS = 15
    MAX_ACHIEVEMENTS_PER_EXPERIENCE = 10
    MAX_TECHNOLOGIES_PER_PROJECT = 20
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128

class RateLimitConfig:
    """Rate limiting configuration"""
    GUEST_RESUME_CREATE_PER_HOUR = 5
    AUTH_RESUME_CREATE_PER_HOUR = 50
    EXPORT_PER_HOUR = 20
    SCORE_CHECK_PER_HOUR = 30

class DatabaseConfig:
    """Database connection configuration"""
    POOL_SIZE = 20
    MAX_OVERFLOW = 40
    POOL_PRE_PING = True
    POOL_RECYCLE = 3600
    ECHO_SQL = False
    STATEMENT_TIMEOUT = 30000  # 30 seconds in milliseconds

class ResponseMessages:
    """Standardized response messages"""
    RESUME_CREATED = "Resume created successfully"
    RESUME_UPDATED = "Resume updated successfully"
    RESUME_DELETED = "Resume deleted successfully"
    RESUME_NOT_FOUND = "Resume not found"
    UNAUTHORIZED = "Not authorized to access this resource"
    INVALID_INPUT = "Invalid input data"
    RATE_LIMIT_EXCEEDED = "Rate limit exceeded. Please try again later"
    EXPORT_FAILED = "Failed to export resume"
    USER_CREATED = "User account created successfully"
    LOGIN_SUCCESS = "Login successful"
    INVALID_CREDENTIALS = "Invalid email or password"

class ATSConstants:
    """ATS scoring and processing constants"""
    MAX_SKILLS = 25
    MIN_SKILLS_RECOMMENDED = 8
    MAX_FEEDBACK_ITEMS = 10
    FUZZY_MATCH_THRESHOLD = 0.85
    JD_MATCH_THRESHOLD = 0.3
    MAX_JD_KEYWORDS = 20
    LRU_CACHE_SIZE = 256
    JD_KEYWORDS_CACHE_SIZE = 128
    
    ROLE_WEIGHTS = {
        "entry": {
            "personal_info": 0.20,
            "experience": 0.25,
            "education": 0.25,
            "skills": 0.20,
            "certifications": 0.05,
            "projects": 0.05
        },
        "mid": {
            "personal_info": 0.15,
            "experience": 0.35,
            "education": 0.15,
            "skills": 0.25,
            "certifications": 0.05,
            "projects": 0.05
        },
        "senior": {
            "personal_info": 0.10,
            "experience": 0.45,
            "education": 0.10,
            "skills": 0.25,
            "certifications": 0.05,
            "projects": 0.05
        }
    }

class FileConstants:
    """File upload and processing constants"""
    MAX_PDF_SIZE_MB = 10
    MAX_PDF_SIZE_BYTES = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['.pdf']

class CacheConstants:
    """Caching configuration"""
    TEMPLATE_CACHE_TTL = 3600  # 1 hour
    TEMPLATE_CACHE_SIZE = 100
    TEMPLATE_LIST_CACHE_TTL = 86400  # 24 hours
