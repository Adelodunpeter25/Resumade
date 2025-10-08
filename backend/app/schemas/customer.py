from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class Customer(CustomerBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
