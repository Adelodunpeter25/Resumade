from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
import logging

from app.models import User, Customer, Invoice, InvoiceItem
from app.endpoints import users_router, customers_router, invoices_router, auth_router, analytics_router
from app.core.exceptions import (
    QuickInvoiceException, 
    quickinvoice_exception_handler,
    integrity_error_handler,
    general_exception_handler
)
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuickInvoice API",
    version="1.0.0",
    description="A comprehensive invoice management system with authentication, CRUD operations, and business analytics.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add exception handlers
app.add_exception_handler(QuickInvoiceException, quickinvoice_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers - tags are already defined in each router
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(customers_router, prefix="/api")
app.include_router(invoices_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("QuickInvoice API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("QuickInvoice API shutting down...")

# Base route, add 'HEAD' method for uptime robot monitoring
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    """Root endpoint - API status check"""
    return {"message": "QuickInvoice API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "database": "connected"}
