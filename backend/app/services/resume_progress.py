from typing import Dict
from app.models.resume_progress import ResumeProgress
from app.models.resume import Resume

class ResumeProgressService:
    @staticmethod
    def calculate_section_scores(resume: Resume) -> Dict[str, float]:
        scores = {}
        
        # Personal Info score
        personal_info = resume.personal_info or {}
        required_fields = ['full_name', 'email', 'phone', 'location']
        optional_fields = ['linkedin', 'website', 'summary']
        personal_score = (
            sum(1 for f in required_fields if personal_info.get(f)) * 0.8 / len(required_fields) +
            sum(1 for f in optional_fields if personal_info.get(f)) * 0.2 / len(optional_fields)
        ) * 100
        scores['personal_info'] = personal_score

        # Experience score
        experience = resume.experience or []
        if experience:
            exp_scores = []
            for exp in experience:
                required_exp_fields = ['company', 'position', 'start_date', 'description']
                exp_score = sum(1 for f in required_exp_fields if exp.get(f)) / len(required_exp_fields)
                exp_scores.append(exp_score)
            scores['experience'] = sum(exp_scores) / len(exp_scores) * 100
        else:
            scores['experience'] = 0

        # Education score
        education = resume.education or []
        if education:
            edu_scores = []
            for edu in education:
                required_edu_fields = ['institution', 'degree', 'graduation_date']
                edu_score = sum(1 for f in required_edu_fields if edu.get(f)) / len(required_edu_fields)
                edu_scores.append(edu_score)
            scores['education'] = sum(edu_scores) / len(edu_scores) * 100
        else:
            scores['education'] = 0

        # Skills score
        skills = resume.skills or []
        scores['skills'] = min(len(skills) * 10, 100) if skills else 0

        # Projects score
        projects = resume.projects or []
        if projects:
            proj_scores = []
            for proj in projects:
                required_proj_fields = ['name', 'description']
                proj_score = sum(1 for f in required_proj_fields if proj.get(f)) / len(required_proj_fields)
                proj_scores.append(proj_score)
            scores['projects'] = sum(proj_scores) / len(proj_scores) * 100
        else:
            scores['projects'] = 0

        return scores

    @staticmethod
    def calculate_overall_progress(section_scores: Dict[str, float], weights: Dict[str, float]) -> float:
        total_weight = sum(weights.values())
        weighted_sum = sum(
            section_scores.get(section, 0) * weight
            for section, weight in weights.items()
        )
        return weighted_sum / total_weight

    @staticmethod
    async def update_progress(resume: Resume, db) -> ResumeProgress:
        section_scores = ResumeProgressService.calculate_section_scores(resume)
        
        progress = await db.query(ResumeProgress).filter(ResumeProgress.resume_id == resume.id).first()
        if not progress:
            progress = ResumeProgress(resume_id=resume.id)
            db.add(progress)

        progress.section_scores = section_scores
        progress.completion_percentage = ResumeProgressService.calculate_overall_progress(
            section_scores,
            progress.sections_weight
        )
        
        await db.commit()
        await db.refresh(progress)
        return progress
