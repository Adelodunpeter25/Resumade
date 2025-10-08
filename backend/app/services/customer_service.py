from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Customer, Invoice

class CustomerService:
    
    @staticmethod
    def get_customer_total_invoiced(db: Session, customer_id: int) -> Decimal:
        """Get total amount invoiced for a customer"""
        result = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.customer_id == customer_id
        ).scalar()
        return result or Decimal("0.00")
    
    @staticmethod
    def get_customer_outstanding_balance(db: Session, customer_id: int) -> Decimal:
        """Get outstanding balance for a customer (unpaid invoices)"""
        result = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.customer_id == customer_id,
            Invoice.status != "paid"
        ).scalar()
        return result or Decimal("0.00")
    
    @staticmethod
    def get_customer_invoice_count(db: Session, customer_id: int) -> int:
        """Get total number of invoices for a customer"""
        return db.query(Invoice).filter(Invoice.customer_id == customer_id).count()
    
    @staticmethod
    def get_customer_overdue_invoices(db: Session, customer_id: int) -> List[Invoice]:
        """Get overdue invoices for a customer"""
        from datetime import datetime
        return db.query(Invoice).filter(
            Invoice.customer_id == customer_id,
            Invoice.status != "paid",
            Invoice.due_date < datetime.now()
        ).all()
    
    @staticmethod
    def get_customer_stats(db: Session, customer_id: int) -> dict:
        """Get comprehensive customer statistics"""
        return {
            "total_invoiced": CustomerService.get_customer_total_invoiced(db, customer_id),
            "outstanding_balance": CustomerService.get_customer_outstanding_balance(db, customer_id),
            "invoice_count": CustomerService.get_customer_invoice_count(db, customer_id),
            "overdue_count": len(CustomerService.get_customer_overdue_invoices(db, customer_id))
        }
    
    @staticmethod
    def validate_customer_data(name: str, email: str) -> List[str]:
        """Validate customer data and return list of errors"""
        errors = []
        
        if not name or len(name.strip()) < 2:
            errors.append("Customer name must be at least 2 characters")
        
        if not email or "@" not in email:
            errors.append("Valid email address is required")
        
        return errors
