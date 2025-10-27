from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address (must be unique)")
    full_name: str = Field(..., min_length=2, description="User's full name")


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        description="Password (minimum 6 characters, securely hashed)",
    )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address")
    full_name: Optional[str] = Field(None, min_length=2, description="New full name")
    is_active: Optional[bool] = Field(None, description="Account active status")


class User(UserBase):
    """User response model with all public fields"""

    id: int = Field(..., description="Unique user identifier")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True
