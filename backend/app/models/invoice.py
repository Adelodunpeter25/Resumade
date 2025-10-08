from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # NULLABLE user_id: allows guest invoices (user_id=None) and logged-in user invoices
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))
    subtotal = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), default=0)
    status = Column(String, default="draft")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer", back_populates="invoices")
    # user relationship is nullable - None for guest invoices
    user = relationship("User")
    items = relationship("InvoiceItem", back_populates="invoice")
