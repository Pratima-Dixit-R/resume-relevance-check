from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from src.parsing.resume_parser import ResumeParser
from src.parsing.jd_parser import JDParser
from src.scoring.hard_match import calculate_hard_match
from src.scoring.semantic_match import calculate_semantic_match
from src.scoring.verdict import get_verdict
from src.storage.database import store_evaluation_results

router = APIRouter()

@router.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are accepted.")
    
    resume_parser = ResumeParser()
    resume_text = await resume_parser.parse(file)
    
    return {"message": "Resume uploaded successfully", "resume_text": resume_text}

@router.post("/upload_jd/")
async def upload_jd(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are accepted.")
    
    jd_parser = JDParser()
    jd_text = await jd_parser.parse(file)
    
    return {"message": "Job description uploaded successfully", "jd_text": jd_text}

@router.post("/evaluate/")
async def evaluate_resume(resume_text: str, jd_text: str):
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
    
    store_evaluation_results(evaluation_result)
    
    return evaluation_result

@router.get("/evaluations/")
async def get_evaluation_results():
    """Get recent evaluation results"""
    try:
        from src.storage.database import SessionLocal, Evaluation
        db = SessionLocal()
        evaluations = db.query(Evaluation).order_by(Evaluation.id.desc()).limit(10).all()
        db.close()
        
        results = []
        for eval in evaluations:
            results.append({
                "id": eval.id,
                "relevance_score": eval.relevance_score,
                "verdict": eval.verdict,
                "missing_elements": eval.missing_elements
            })
        
        return {"evaluations": results}
    except Exception as e:
        return {"error": str(e), "evaluations": []}

