import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
import logging

from app.endpoints import (
    users_router,
    resumes_router,
    auth_router,
    admin_router,
    ai_content_router,
)
from app.endpoints.analytics import router as analytics_router
from app.core.exceptions import (
    ResumadeException,
    resumade_exception_handler,
    integrity_error_handler,
    general_exception_handler,
)
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resumade API",
    version="1.0.0",
    description="Professional resume builder with multiple templates and PDF generation.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://resumade.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ResumadeException, resumade_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(resumes_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(ai_content_router, prefix="/api")
app.include_router(analytics_router)


async def preload_heavy_imports():
    """Pre-load heavy imports in background after startup"""
    logger.info("Pre-loading heavy dependencies in background...")

    # Pre-load WeasyPrint
    try:
        logger.info("WeasyPrint loaded")
    except Exception as e:
        logger.warning(f"WeasyPrint load failed: {e}")

    # Pre-load Gemini AI
    try:
        import google.generativeai as genai
        from app.core.config import settings

        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            genai.GenerativeModel("gemini-2.0-flash")
            logger.info("Gemini AI loaded")
    except Exception as e:
        logger.warning(f"Gemini AI load failed: {e}")

    # Pre-load PDF parsing
    try:
        logger.info("PyPDF2 loaded")
    except Exception as e:
        logger.warning(f"PyPDF2 load failed: {e}")

    # Pre-load DOCX
    try:
        logger.info("python-docx loaded")
    except Exception as e:
        logger.warning(f"python-docx load failed: {e}")

    logger.info("Heavy dependencies pre-loaded")


@app.on_event("startup")
async def startup_event():
    logger.info("Resumade API starting up...")
    # Start background task to load heavy imports
    asyncio.create_task(preload_heavy_imports())


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Resumade API shutting down...")


@app.api_route("/", methods=["GET", "HEAD"])
def root():
    """Root endpoint - API status check"""
    return {"message": "Resumade API", "status": "running"}


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "database": "connected"}
