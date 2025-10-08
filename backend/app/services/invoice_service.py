from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.models import Invoice, InvoiceItem

class InvoiceService:
    
    @staticmethod
    def generate_invoice_number() -> str:
        """Generate unique invoice number"""
        return f"INV-{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def calculate_item_total(quantity: Decimal, unit_price: Decimal) -> Decimal:
        """Calculate total for a single item"""
        return quantity * unit_price
    
    @staticmethod
    def calculate_subtotal(items: List[InvoiceItem]) -> Decimal:
        """Calculate subtotal from invoice items"""
        return sum(item.total_price for item in items)
    
    @staticmethod
    def calculate_tax(subtotal: Decimal, tax_rate: Decimal = Decimal("0.1")) -> Decimal:
        """Calculate tax amount (default 10%)"""
        return subtotal * tax_rate
    
    @staticmethod
    def calculate_total(subtotal: Decimal, tax_amount: Decimal) -> Decimal:
        """Calculate final total"""
        return subtotal + tax_amount
    
    @staticmethod
    def calculate_invoice_totals(items: List[InvoiceItem], tax_rate: Decimal = Decimal("0.1")) -> dict:
        """Calculate all invoice totals"""
        subtotal = InvoiceService.calculate_subtotal(items)
        tax_amount = InvoiceService.calculate_tax(subtotal, tax_rate)
        total_amount = InvoiceService.calculate_total(subtotal, tax_amount)
        
        return {
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_amount": total_amount
        }
    
    @staticmethod
    def is_overdue(invoice: Invoice) -> bool:
        """Check if invoice is overdue"""
        if not invoice.due_date or invoice.status == "paid":
            return False
        return datetime.now() > invoice.due_date
    
    @staticmethod
    def days_overdue(invoice: Invoice) -> int:
        """Calculate days overdue"""
        if not InvoiceService.is_overdue(invoice):
            return 0
        return (datetime.now() - invoice.due_date).days
    
    @staticmethod
    def get_overdue_invoices(db: Session, user_id: int) -> List[Invoice]:
        """Get all overdue invoices for a user"""
        invoices = db.query(Invoice).filter(
            Invoice.user_id == user_id,
            Invoice.status != "paid",
            Invoice.due_date < datetime.now()
        ).all()
        return invoices
    
    @staticmethod
    def mark_as_paid(invoice: Invoice, db: Session) -> Invoice:
        """Mark invoice as paid"""
        invoice.status = "paid"
        db.commit()
        db.refresh(invoice)
        return invoice
    
    @staticmethod
    def set_due_date(invoice: Invoice, days_from_now: int = 30) -> datetime:
        """Set due date (default 30 days from now)"""
        return datetime.now() + timedelta(days=days_from_now)
