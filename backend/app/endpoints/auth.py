from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import logging
import secrets

from app.core.database import get_db
from app.core.auth import verify_password, get_password_hash, create_access_token, get_current_user
from app.core.validation import InputValidator
from app.core.constants import ResponseMessages, ValidationConfig
from app.models import User
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.response import APIResponse, ErrorResponse, ErrorDetail
from app.services.oauth_service import GoogleOAuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

# Store OAuth states temporarily (use Redis in production)
oauth_states = {}

@router.post("/signup", response_model=APIResponse[Token], status_code=status.HTTP_201_CREATED)
def signup(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """Create a new user account with email and password"""
    logger.info(f"Signup attempt for email: {user.email}")
    
    # Validate email
    if not InputValidator.validate_email(user.email):
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                message=ResponseMessages.INVALID_INPUT,
                errors=[ErrorDetail(field="email", message="Invalid email format")]
            ).dict()
        )
    
    # Validate password length
    if len(user.password) < ValidationConfig.MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                message=ResponseMessages.INVALID_INPUT,
                errors=[ErrorDetail(field="password", message=f"Password must be at least {ValidationConfig.MIN_PASSWORD_LENGTH} characters")]
            ).dict()
        )
    
    # Sanitize inputs
    email = user.email.strip().lower()
    full_name = InputValidator.sanitize_text(user.full_name, ValidationConfig.MAX_NAME_LENGTH)
    
    # Check if user exists
    if db.query(User).filter(User.email == email).first():
        logger.warning(f"Signup failed - email already exists: {email}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                message="Email already registered",
                errors=[ErrorDetail(field="email", message="This email is already in use")]
            ).dict()
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    db_user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    
    logger.info(f"User created successfully: {email}")
    
    # Create token
    access_token = create_access_token(data={"sub": email})
    
    return APIResponse(
        success=True,
        message=ResponseMessages.USER_CREATED,
        data=Token(access_token=access_token, token_type="bearer")
    )

@router.post("/login", response_model=APIResponse[Token])
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    logger.info(f"Login attempt for email: {credentials.email}")
    
    email = credentials.email.strip().lower()
    
    # Find user
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not user.hashed_password:
        logger.warning(f"Login failed - user not found: {email}")
        raise HTTPException(
            status_code=401,
            detail=ErrorResponse(
                message=ResponseMessages.INVALID_CREDENTIALS
            ).dict()
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        logger.warning(f"Login failed - invalid password: {email}")
        raise HTTPException(
            status_code=401,
            detail=ErrorResponse(
                message=ResponseMessages.INVALID_CREDENTIALS
            ).dict()
        )
    
    # Create token
    access_token = create_access_token(data={"sub": email})
    
    logger.info(f"Login successful: {email}")
    
    return APIResponse(
        success=True,
        message=ResponseMessages.LOGIN_SUCCESS,
        data=Token(access_token=access_token, token_type="bearer")
    )

@router.get("/google")
def google_auth():
    """Initiate Google OAuth flow"""
    state = secrets.token_urlsafe(32)
    oauth_states[state] = True  # Store state
    
    auth_url = GoogleOAuthService.get_authorization_url(state)
    return {"auth_url": auth_url}

@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback"""
    # Verify state
    if state not in oauth_states:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    del oauth_states[state]
    
    # Exchange code for token
    token_data = await GoogleOAuthService.exchange_code_for_token(code)
    if not token_data:
        raise HTTPException(status_code=400, detail="Failed to exchange code for token")
    
    # Get user info
    user_info = await GoogleOAuthService.get_user_info(token_data["access_token"])
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info")
    
    email = user_info["email"].lower()
    google_id = user_info["id"]
    full_name = user_info.get("name", email.split("@")[0])
    
    # Find or create user
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        user = User(
            email=email,
            full_name=full_name,
            oauth_provider="google",
            oauth_id=google_id,
            hashed_password=None
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"New user created via Google OAuth: {email}")
    elif not user.oauth_provider:
        # Link existing account
        user.oauth_provider = "google"
        user.oauth_id = google_id
        db.commit()
        logger.info(f"Linked Google OAuth to existing account: {email}")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": email})
    
    # Redirect to frontend with token
    frontend_url = f"{settings.frontend_url}/auth/callback?token={access_token}"
    return RedirectResponse(url=frontend_url)

@router.get("/me", response_model=APIResponse[UserSchema])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return APIResponse(
        success=True,
        message="User information retrieved",
        data=current_user
    )

@router.post("/login", response_model=APIResponse[Token])
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    logger.info(f"Login attempt for email: {credentials.email}")
    
    email = credentials.email.strip().lower()
    
    # Find user
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not user.hashed_password:
        logger.warning(f"Login failed - user not found: {email}")
        raise HTTPException(
            status_code=401,
            detail=ErrorResponse(
                message=ResponseMessages.INVALID_CREDENTIALS
            ).dict()
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        logger.warning(f"Login failed - invalid password: {email}")
        raise HTTPException(
            status_code=401,
            detail=ErrorResponse(
                message=ResponseMessages.INVALID_CREDENTIALS
            ).dict()
        )
    
    # Create token
    access_token = create_access_token(data={"sub": email})
    
    logger.info(f"Login successful: {email}")
    
    return APIResponse(
        success=True,
        message=ResponseMessages.LOGIN_SUCCESS,
        data=Token(access_token=access_token, token_type="bearer")
    )
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
