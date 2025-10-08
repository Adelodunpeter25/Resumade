from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.core.auth import get_password_hash, get_current_user
from app.models import User
from app.schemas import User as UserSchema, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new user account (Admin endpoint)
    
    - **email**: Valid email address (must be unique)
    - **full_name**: User's full name
    - **password**: Password (minimum 6 characters, securely hashed)
    
    Note: This endpoint creates users without authentication.
    For regular signup, use /api/auth/signup instead.
    """
    logger.info(f"Creating user account for: {user.email}")
    
    # Check if user exists
    if db.query(User).filter(User.email == user.email).first():
        logger.warning(f"User creation failed - email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User created successfully with ID: {db_user.id}")
    return db_user

@router.get("/", response_model=List[UserSchema])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Get all users (Admin endpoint)
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (max 100)
    
    Requires authentication. Returns list of all users in the system.
    """
    logger.info(f"Fetching users list requested by: {current_user.email}")
    return db.query(User).offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific user by ID
    
    - **user_id**: Unique user identifier
    
    Requires authentication. Returns user details if found.
    """
    logger.info(f"Fetching user {user_id} requested by: {current_user.email}")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing user
    
    - **user_id**: Unique user identifier
    - **email**: New email address (optional)
    - **full_name**: New full name (optional)
    - **is_active**: Account active status (optional)
    
    Only provided fields will be updated. Requires authentication.
    """
    logger.info(f"Updating user {user_id} requested by: {current_user.email}")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"User {user_id} updated successfully")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Delete a user account
    
    - **user_id**: Unique user identifier
    
    Permanently removes the user and all associated data.
    Requires authentication.
    """
    logger.info(f"Deleting user {user_id} requested by: {current_user.email}")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    logger.info(f"User {user_id} deleted successfully")
    return {"message": "User deleted successfully"}
