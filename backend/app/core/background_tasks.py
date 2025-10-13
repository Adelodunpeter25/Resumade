from fastapi import BackgroundTasks
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class BackgroundTaskManager:
    """Manage background tasks for async operations"""
    
    @staticmethod
    def add_task(background_tasks: BackgroundTasks, func: Callable, *args, **kwargs):
        """Add a background task"""
        try:
            background_tasks.add_task(func, *args, **kwargs)
            logger.info(f"Background task added: {func.__name__}")
        except Exception as e:
            logger.error(f"Failed to add background task: {str(e)}")
    
    @staticmethod
    async def generate_pdf_async(resume_id: int, template: str):
        """Generate PDF in background"""
        from app.services import PDFService
        from app.core.database import SessionLocal
        from app.models import Resume
        
        try:
            db = SessionLocal()
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            if resume:
                pdf_service = PDFService()
                pdf_content = pdf_service.generate_pdf(resume, template)
                logger.info(f"PDF generated for resume {resume_id}")
                return pdf_content
        except Exception as e:
            logger.error(f"Background PDF generation failed: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    async def update_analytics_async(resume_id: int, metric: str):
        """Update analytics in background"""
        from app.core.database import SessionLocal
        from app.models import Resume
        
        try:
            db = SessionLocal()
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            if resume:
                if metric == "views":
                    resume.views += 1
                elif metric == "downloads":
                    resume.downloads += 1
                db.commit()
                logger.info(f"Analytics updated for resume {resume_id}: {metric}")
        except Exception as e:
            logger.error(f"Background analytics update failed: {str(e)}")
        finally:
            db.close()
