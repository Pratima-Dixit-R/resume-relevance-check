import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from functools import lru_cache
import time

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import get_user_by_id, get_db, get_user_by_username, get_user_by_email

# JWT configuration with stronger security
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "resume_relevance_checker_secret_key_2025_stronger_than_linkedin")
ALGORITHM = "HS512"  # Using HS512 instead of HS256 for stronger encryption
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Rate limiting
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_TIME = 900  # 15 minutes

security = HTTPBearer()

class TokenData:
    def __init__(self, username: str = "", user_id: int = 0):
        self.username: str = username
        self.user_id: int = user_id

# Rate limiting storage (in production, use Redis or database)
login_attempts = {}

def is_rate_limited(username: str) -> bool:
    """Check if user is rate limited"""
    now = time.time()
    attempts = login_attempts.get(username, [])
    
    # Remove attempts older than lockout time
    attempts = [attempt for attempt in attempts if now - attempt < LOGIN_LOCKOUT_TIME]
    login_attempts[username] = attempts
    
    return len(attempts) >= MAX_LOGIN_ATTEMPTS

def record_login_attempt(username: str):
    """Record a login attempt"""
    now = time.time()
    if username not in login_attempts:
        login_attempts[username] = []
    login_attempts[username].append(now)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token with enhanced security"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt (LinkedIn-level security)"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generate a hash for a password using bcrypt (LinkedIn-level security)"""
    salt = bcrypt.gensalt(rounds=14)  # Using 14 rounds for stronger security
    pwd_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return pwd_hash.decode('utf-8')

def authenticate_user(username: str, password: str):
    """Authenticate a user with rate limiting"""
    # Check rate limiting
    if is_rate_limited(username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )
    
    db = next(get_db())
    # Try to find user by username first
    user = get_user_by_username(db, username)
    # If not found, try to find by email
    if not user:
        user = get_user_by_email(db, username)
    
    if not user:
        record_login_attempt(username)
        return False
    
    if not verify_password(password, str(user.hashed_password)):
        record_login_attempt(username)
        return False
    
    # Reset login attempts on successful login
    if username in login_attempts:
        del login_attempts[username]
    
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
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
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