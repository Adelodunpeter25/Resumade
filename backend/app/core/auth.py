from datetime import datetime, timedelta
from typing import Optional
import hashlib
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import User

# Two different security instances for required vs optional auth
security = HTTPBearer()  # Required auth (raises error if no token)
security_optional = HTTPBearer(
    auto_error=False
)  # Optional auth (returns None if no token)


def _prepare_password(password: str) -> bytes:
    """Hash password with SHA256 first to handle long passwords"""
    return hashlib.sha256(password.encode("utf-8")).digest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    prepared_password = _prepare_password(plain_password)
    return bcrypt.checkpw(prepared_password, hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    prepared_password = _prepare_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prepared_password, salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    REQUIRED AUTHENTICATION: Get current authenticated user or raise 401 error
    Use this for endpoints that require login (analytics, user management, invoice history, etc.)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = verify_token(credentials.credentials)
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security_optional),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    OPTIONAL AUTHENTICATION: Get current user if logged in, None if guest
    Use this for endpoints that work for both guests and logged-in users (create invoice, view invoice, etc.)

    Returns:
    - User object if valid token provided and user exists
    - None if no token provided (guest user)
    - None if invalid token provided (treat as guest)
    """
    if not credentials:
        return None  # Guest user - no token provided

    try:
        email = verify_token(credentials.credentials)
        if email is None:
            return None  # Invalid token, treat as guest

        user = db.query(User).filter(User.email == email).first()
        return user  # Could be None if user not found, but token was valid
    except Exception:
        return None  # Any error, treat as guest
