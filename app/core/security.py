# app/core/security.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def create_access_token(data: dict) -> str:
    """Generates a JWT access token."""
    return create_jwt_token(data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict) -> str:
    """Generates a JWT refresh token."""
    return create_jwt_token(data, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
