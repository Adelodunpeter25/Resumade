from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
import logging

from app.models import User, Resume
from app.endpoints import users_router, resumes_router, auth_router
from app.core.exceptions import (
    QuickInvoiceException, 
    quickinvoice_exception_handler,
    integrity_error_handler,
    general_exception_handler
)
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resumade API",
    version="1.0.0",
    description="Professional resume builder with multiple templates and PDF generation.",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_exception_handler(QuickInvoiceException, quickinvoice_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(resumes_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("Resumade API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Resumade API shutting down...")

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    """Root endpoint - API status check"""
    return {"message": "Resumade API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "database": "connected"}
