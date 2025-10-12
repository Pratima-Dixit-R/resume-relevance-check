import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib
import secrets
import os

DATABASE_URL = "sqlite:///./evaluations.db"  # Update with your database URL

# Handle database migration - remove old database if schema has changed
if os.path.exists("./evaluations.db"):
    # In a production environment, you would implement proper migrations
    # For development, we'll recreate the database when schema changes
    pass

Base = declarative_base()

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(String, index=True)
    job_id = Column(String, index=True)
    relevance_score = Column(Integer)
    missing_elements = Column(Text)
    verdict = Column(String)
    user_id = Column(Integer, index=True)  # Link evaluation to user
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def set_password(self, password: str):
        """Hash and set password"""
        self.salt = secrets.token_hex(16)
        self.hashed_password = hashlib.sha256((password + self.salt).encode()).hexdigest()
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        return hashlib.sha256((password + self.salt).encode()).hexdigest() == self.hashed_password

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_evaluation(db, resume_id, job_id, relevance_score, missing_elements, verdict, user_id=None):
    db_evaluation = Evaluation(
        resume_id=resume_id,
        job_id=job_id,
        relevance_score=relevance_score,
        missing_elements=missing_elements,
        verdict=verdict,
        user_id=user_id
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

def get_evaluations(db, skip=0, limit=10, user_id=None):
    query = db.query(Evaluation)
    if user_id:
        query = query.filter(Evaluation.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_evaluation_by_id(db, evaluation_id):
    return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

def store_evaluation_results(evaluation_result, user_id=None):
    """
    Store evaluation results in the database.
    
    Parameters:
    evaluation_result (dict): Dictionary containing evaluation results
    user_id (str): Optional user ID to link evaluation to user
    
    Returns:
    Evaluation: The stored evaluation record
    """
    db = SessionLocal()
    try:
        db_evaluation = Evaluation(
            resume_id=evaluation_result.get('resume_id', 'unknown'),
            job_id=evaluation_result.get('job_id', 'unknown'),
            relevance_score=int(evaluation_result.get('final_score', 0)),
            missing_elements=str(evaluation_result.get('missing_elements', '')),
            verdict=evaluation_result.get('verdict', 'Unknown'),
            user_id=user_id
        )
        db.add(db_evaluation)
        db.commit()
        db.refresh(db_evaluation)
        return db_evaluation
    except Exception as e:
        db.rollback()
        print(f"Error storing evaluation results: {e}")
        return None
    finally:
        db.close()

def create_user(db, username: str, email: str, password: str):
    """Create a new user"""
    user = User(username=username, email=email)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db, username: str):
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()