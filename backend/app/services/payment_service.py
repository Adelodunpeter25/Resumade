from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Invoice, User

class PaymentService:
    
    @staticmethod
    def calculate_late_fee(invoice: Invoice, daily_rate: Decimal = Decimal("0.01")) -> Decimal:
        """Calculate late fee based on days overdue (1% per day default)"""
        if not invoice.due_date or invoice.status == "paid":
            return Decimal("0.00")
        
        days_overdue = (datetime.now() - invoice.due_date).days
        if days_overdue <= 0:
            return Decimal("0.00")
        
        return invoice.total_amount * daily_rate * days_overdue
    
    @staticmethod
    def get_payment_status(invoice: Invoice) -> str:
        """Get detailed payment status"""
        if invoice.status == "paid":
            return "paid"
        
        if not invoice.due_date:
            return "no_due_date"
        
        days_until_due = (invoice.due_date - datetime.now()).days
        
        if days_until_due > 7:
            return "current"
        elif days_until_due > 0:
            return "due_soon"
        elif days_until_due == 0:
            return "due_today"
        else:
            return "overdue"
    
    @staticmethod
    def get_aging_report(db: Session, user_id: int) -> Dict[str, Decimal]:
        """Generate aging report for unpaid invoices"""
        now = datetime.now()
        
        # Current (not due yet)
        current = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.user_id == user_id,
            Invoice.status != "paid",
            Invoice.due_date > now
        ).scalar() or Decimal("0.00")
        
        # 1-30 days overdue
        days_30_ago = now - timedelta(days=30)
        overdue_30 = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.user_id == user_id,
            Invoice.status != "paid",
            Invoice.due_date <= now,
            Invoice.due_date > days_30_ago
        ).scalar() or Decimal("0.00")
        
        # 31-60 days overdue
        days_60_ago = now - timedelta(days=60)
        overdue_60 = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.user_id == user_id,
            Invoice.status != "paid",
            Invoice.due_date <= days_30_ago,
            Invoice.due_date > days_60_ago
        ).scalar() or Decimal("0.00")
        
        # 60+ days overdue
        overdue_60_plus = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.user_id == user_id,
            Invoice.status != "paid",
            Invoice.due_date <= days_60_ago
        ).scalar() or Decimal("0.00")
        
        return {
            "current": current,
            "overdue_1_30": overdue_30,
            "overdue_31_60": overdue_60,
            "overdue_60_plus": overdue_60_plus,
            "total_outstanding": current + overdue_30 + overdue_60 + overdue_60_plus
        }
    
    @staticmethod
    def get_revenue_summary(db: Session, user_id: int) -> Dict[str, Decimal]:
        """Get revenue summary for user"""
        # Total invoiced
        total_invoiced = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.user_id == user_id
        ).scalar() or Decimal("0.00")
        
        # Total paid
        total_paid = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.user_id == user_id,
            Invoice.status == "paid"
        ).scalar() or Decimal("0.00")
        
        # Total outstanding
        total_outstanding = total_invoiced - total_paid
        
        return {
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_outstanding": total_outstanding
        }
