import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import secrets

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path modification
import jwt

from src.storage.database import get_user_by_id, get_db, get_user_by_username

# JWT configuration
SECRET_KEY = "resume_relevance_checker_secret_key_2025"  # In production, use a more secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class TokenData:
    def __init__(self, username: str = "", user_id: int = 0):
        self.username: str = username
        self.user_id: int = user_id

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """Verify a password against its hash"""
    return hashlib.sha256((plain_password + salt).encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> tuple:
    """Generate a salt and hash for a password"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return pwd_hash, salt

def authenticate_user(username: str, password: str):
    """Authenticate a user"""
    db = next(get_db())
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, str(user.hashed_password), str(user.salt)):
        return False
    return user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", "")
        user_id: int = payload.get("user_id", 0)
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id)
    except jwt.PyJWTError:
        raise credentials_exception
    
    db = next(get_db())
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user"""
    return current_user