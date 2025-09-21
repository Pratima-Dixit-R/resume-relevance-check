from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./evaluations.db"  # Update with your database URL

Base = declarative_base()

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(String, index=True)
    job_id = Column(String, index=True)
    relevance_score = Column(Integer)
    missing_elements = Column(Text)
    verdict = Column(String)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_evaluation(db, resume_id, job_id, relevance_score, missing_elements, verdict):
    db_evaluation = Evaluation(
        resume_id=resume_id,
        job_id=job_id,
        relevance_score=relevance_score,
        missing_elements=missing_elements,
        verdict=verdict
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

def get_evaluations(db, skip=0, limit=10):
    return db.query(Evaluation).offset(skip).limit(limit).all()

def get_evaluation_by_id(db, evaluation_id):
    return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

def store_evaluation_results(evaluation_result):
    """
    Store evaluation results in the database.
    
    Parameters:
    evaluation_result (dict): Dictionary containing evaluation results
    
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
            verdict=evaluation_result.get('verdict', 'Unknown')
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