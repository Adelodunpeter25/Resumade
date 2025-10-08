from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
import logging

from app.core.database import get_db
from app.core.auth import get_current_user  # REQUIRES LOGIN
from app.models import User
from app.services import PaymentService, CustomerService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)

@router.get("/revenue-summary")
def get_revenue_summary(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
) -> Dict:
    """
    Get comprehensive revenue summary for the authenticated user
    
    **REQUIRES LOGIN** - Analytics are only available to logged-in users
    
    Returns:
    - **total_invoiced**: Total amount of all invoices created by the user
    - **total_paid**: Total amount of paid invoices by the user
    - **total_outstanding**: Total amount of unpaid invoices by the user
    
    Only includes invoices owned by the authenticated user (excludes guest invoices).
    Useful for understanding overall business performance and cash flow.
    """
    logger.info(f"Generating revenue summary for user: {current_user.email}")
    return PaymentService.get_revenue_summary(db, current_user.id)

@router.get("/aging-report")
def get_aging_report(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
) -> Dict:
    """
    Generate accounts receivable aging report
    
    **REQUIRES LOGIN** - Analytics are only available to logged-in users
    
    Returns outstanding invoices categorized by age:
    - **current**: Invoices not yet due
    - **overdue_1_30**: 1-30 days overdue
    - **overdue_31_60**: 31-60 days overdue  
    - **overdue_60_plus**: More than 60 days overdue
    - **total_outstanding**: Sum of all outstanding amounts
    
    Only includes invoices owned by the authenticated user (excludes guest invoices).
    Essential for managing cash flow and identifying collection issues.
    """
    logger.info(f"Generating aging report for user: {current_user.email}")
    return PaymentService.get_aging_report(db, current_user.id)

@router.get("/customer/{customer_id}/stats")
def get_customer_stats(
    customer_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
) -> Dict:
    """
    Get detailed statistics for a specific customer
    
    **REQUIRES LOGIN** - Analytics are only available to logged-in users
    
    - **customer_id**: Unique customer identifier
    
    Returns:
    - **total_invoiced**: Total amount invoiced to this customer by the user
    - **outstanding_balance**: Current amount owed by customer to the user
    - **invoice_count**: Total number of invoices for customer by the user
    - **overdue_count**: Number of overdue invoices for customer by the user
    
    Only includes data for invoices owned by the authenticated user.
    Helps assess customer relationship and payment patterns.
    """
    logger.info(f"Generating stats for customer {customer_id} by user: {current_user.email}")
    return CustomerService.get_customer_stats(db, customer_id)
