from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from .invoice_item import InvoiceItem, InvoiceItemCreate

class InvoiceBase(BaseModel):
    customer_id: int
    due_date: Optional[datetime] = None
    status: str = "draft"
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate] = []

class InvoiceUpdate(BaseModel):
    customer_id: Optional[int] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Invoice(InvoiceBase):
    id: int
    invoice_number: str
    user_id: int
    issue_date: datetime
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    created_at: datetime
    items: List[InvoiceItem] = []

    class Config:
        from_attributes = True
