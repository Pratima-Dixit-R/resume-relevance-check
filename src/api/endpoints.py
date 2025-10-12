import sys
import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import List, Optional

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Import after path modification
import jwt

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from typing import List, Optional
from src.parsing.resume_parser import ResumeParser
from src.parsing.jd_parser import JDParser
from src.scoring.hard_match import calculate_hard_match
from src.scoring.semantic_match import calculate_semantic_match
from src.scoring.verdict import get_verdict
from src.storage.database import store_evaluation_results, get_evaluations, SessionLocal, create_user, get_user_by_username
from src.api.auth import authenticate_user, create_access_token, get_current_active_user, TokenData
from src.api.models import UserCreate, UserLogin, Token, User, Evaluation
from datetime import datetime
from datetime import timedelta

router = APIRouter()

# Authentication routes
@router.post("/auth/register", response_model=User)
async def register_user(user: UserCreate):
    """Register a new user"""
    db = SessionLocal()
    try:
        # Check if user already exists
        db_user = get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Create new user
        new_user = create_user(db, user.username, user.email, user.password)
        return new_user
    finally:
        db.close()

@router.post("/auth/login", response_model=Token)
async def login_for_access_token(user_credentials: UserLogin):
    """Login and get access token"""
    user = authenticate_user(user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

# Protected evaluation routes
@router.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)):
    filename: Optional[str] = file.filename
    if not filename or not filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are accepted.")
    
    resume_parser = ResumeParser()
    resume_text = await resume_parser.parse(file)
    
    return {"message": "Resume uploaded successfully", "resume_text": resume_text}

@router.post("/upload_jd/")
async def upload_jd(file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)):
    filename: Optional[str] = file.filename
    if not filename or not filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are accepted.")
    
    jd_parser = JDParser()
    jd_text = await jd_parser.parse(file)
    
    return {"message": "Job description uploaded successfully", "jd_text": jd_text}

@router.post("/evaluate/")
async def evaluate_resume(resume_text: str, jd_text: str, current_user: User = Depends(get_current_active_user)):
    # Parse the text data for better structure
    resume_data = {"raw_text": resume_text, "skills": []}
    jd_data = {"raw_text": jd_text, "required_skills": {"required": [], "preferred": []}}
    
    hard_match_score = calculate_hard_match(resume_data, jd_data)
    semantic_match_score = calculate_semantic_match(resume_data, jd_data)
    final_score = (hard_match_score + semantic_match_score) / 2
    verdict = get_verdict(final_score)
    
    evaluation_result = {
        "hard_match_score": hard_match_score,
        "semantic_match_score": semantic_match_score,
        "final_score": final_score,
        "verdict": verdict
    }
    
    store_evaluation_results(evaluation_result, user_id=current_user.id)
    
    return evaluation_result

@router.get("/evaluations/", response_model=List[Evaluation])
async def get_evaluation_results(current_user: User = Depends(get_current_active_user)):
    """Get user's evaluation results"""
    try:
        from src.storage.database import SessionLocal, Evaluation as DBEvaluation
        db = SessionLocal()
        evaluations = db.query(DBEvaluation).filter(DBEvaluation.user_id == current_user.id).order_by(DBEvaluation.id.desc()).limit(10).all()
        db.close()
        
        results = []
        for eval in evaluations:
            results.append({
                "id": eval.id,
                "resume_id": eval.resume_id,
                "job_id": eval.job_id,
                "relevance_score": eval.relevance_score,
                "missing_elements": eval.missing_elements,
                "verdict": eval.verdict,
                "user_id": eval.user_id,
                "created_at": eval.created_at.isoformat() if eval.created_at is not None else None
            })
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))