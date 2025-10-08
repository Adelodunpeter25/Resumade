from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class InvoiceItemBase(BaseModel):
    description: str
    quantity: Decimal = Field(gt=0, decimal_places=2)
    unit_price: Decimal = Field(ge=0, decimal_places=2)
    notes: Optional[str] = None

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemUpdate(BaseModel):
    description: Optional[str] = None
    quantity: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    unit_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    notes: Optional[str] = None

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int
    total_price: Decimal

    class Config:
        from_attributes = True
