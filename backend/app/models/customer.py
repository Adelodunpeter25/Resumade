from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    
    # NULLABLE user_id: allows guest customers (user_id=None) and logged-in user customers
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # user relationship is nullable - None for guest customers
    user = relationship("User")
    invoices = relationship("Invoice", back_populates="customer")
