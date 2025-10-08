from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.auth import verify_password, get_password_hash, create_access_token, get_current_user
from app.models import User
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new user account
    
    - **email**: Valid email address (must be unique)
    - **full_name**: User's full name
    - **password**: Password (any length, securely hashed)
    
    Returns JWT access token for immediate authentication.
    """
    logger.info(f"Signup attempt for email: {user.email}")
    
    # Check if user exists
    if db.query(User).filter(User.email == user.email).first():
        logger.warning(f"Signup failed - email already exists: {user.email}")
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
    
    logger.info(f"User created successfully: {user.email}")
    
    # Create token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
):
    """
    Authenticate user and get access token
    
    - **email**: Registered email address
    - **password**: User's password
    
    Returns JWT access token for API authentication.
    """
    logger.info(f"Login attempt for email: {login_data.email}")
    
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        logger.warning(f"Login failed for email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    logger.info(f"Login successful for email: {login_data.email}")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header.
    """
    logger.info(f"User info requested for: {current_user.email}")
    return current_user
