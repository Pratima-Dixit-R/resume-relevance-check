import ollama
import numpy as np
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_semantic_match(resume_data, jd_data, use_ollama=True):
    """
    Calculate semantic similarity between resume and job description using Ollama.
    
    Parameters:
    resume_data (dict or str): Resume data or text
    jd_data (dict or str): Job description data or text
    use_ollama (bool): Whether to use Ollama for semantic analysis
    
    Returns:
    float: A score between 0 and 100 representing semantic similarity
    """
    # Extract text from data
    if isinstance(resume_data, dict):
        resume_text = resume_data.get('raw_text', '')
    else:
        resume_text = str(resume_data)
    
    if isinstance(jd_data, dict):
        jd_text = jd_data.get('raw_text', '')
    else:
        jd_text = str(jd_data)
    
    if not resume_text or not jd_text:
        return 0.0
    
    try:
        if use_ollama:
            # Use Ollama for advanced semantic analysis
            similarity_score = _calculate_ollama_similarity(resume_text, jd_text)
        else:
            # Fallback to TF-IDF based similarity
            similarity_score = _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Scale the similarity score to a range of 0 to 100
        relevance_score = np.clip(similarity_score * 100, 0, 100)
        
        return float(relevance_score)
    
    except Exception as e:
        logger.error(f"Error calculating semantic match: {e}")
        # Fallback to TF-IDF if Ollama fails
        try:
            similarity_score = _calculate_tfidf_similarity(resume_text, jd_text)
            return float(np.clip(similarity_score * 100, 0, 100))
        except Exception as e2:
            logger.error(f"Fallback semantic matching also failed: {e2}")
            return 0.0

def _calculate_ollama_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate similarity using Ollama LLM for advanced semantic understanding.
    
    Args:
        resume_text: Resume text content
        jd_text: Job description text content
        
    Returns:
        Similarity score between 0 and 1
    """
    try:
        # Check if Ollama is available
        if not _check_ollama_availability():
            logger.warning("Ollama not available, falling back to TF-IDF")
            return _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Create a prompt for semantic similarity analysis
        prompt = f"""
Analyze the semantic similarity between this resume and job description. 
Provide a similarity score from 0.0 to 1.0 based on:
- Skills alignment
- Experience relevance 
- Domain expertise match
- Responsibility overlap

RESUME:
{resume_text[:2000]}...

JOB DESCRIPTION:
{jd_text[:2000]}...

Return only a numerical score between 0.0 and 1.0, nothing else.
"""
        
        # Use Ollama to analyze semantic similarity
        response = ollama.generate(
            model='llama3.2',  # Use a lightweight model for speed
            prompt=prompt,
            options={
                'temperature': 0.1,  # Low temperature for consistent scoring
                'num_predict': 10    # Short response expected
            }
        )
        
        # Extract numerical score from response
        score_text = response.get('response', '0.0').strip()
        
        # Parse the score
        try:
            score = float(score_text)
            # Ensure score is within valid range
            score = np.clip(score, 0.0, 1.0)
            logger.info(f"Ollama semantic similarity score: {score}")
            return score
        except ValueError:
            logger.warning(f"Could not parse Ollama score: {score_text}")
            # Fallback to analyzing response content
            return _parse_ollama_response(score_text)
    
    except Exception as e:
        logger.error(f"Error in Ollama similarity calculation: {e}")
        raise

def _check_ollama_availability() -> bool:
    """
    Check if Ollama is running and accessible.
    
    Returns:
        bool: True if Ollama is available, False otherwise
    """
    try:
        # Try to list available models
        models = ollama.list()
        return True
    except Exception as e:
        logger.warning(f"Ollama not available: {e}")
        return False

def _parse_ollama_response(response_text: str) -> float:
    """
    Parse Ollama response to extract similarity score.
    
    Args:
        response_text: Raw response from Ollama
        
    Returns:
        Parsed similarity score between 0 and 1
    """
    try:
        # Look for numerical patterns in the response
        import re
        
        # Find numbers that look like scores (0.0 to 1.0)
        matches = re.findall(r'\b0?\.[0-9]+\b|\b1\.0\b|\b0\b', response_text)
        
        if matches:
            score = float(matches[0])
            return np.clip(score, 0.0, 1.0)
        
        # Look for percentages and convert
        percent_matches = re.findall(r'\b([0-9]+)%', response_text)
        if percent_matches:
            score = float(percent_matches[0]) / 100.0
            return np.clip(score, 0.0, 1.0)
        
        # Default fallback
        logger.warning(f"Could not parse score from: {response_text}")
        return 0.5  # Neutral score
        
    except Exception as e:
        logger.error(f"Error parsing Ollama response: {e}")
        return 0.5

def _calculate_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """
    Fallback similarity calculation using TF-IDF vectors.
    
    Args:
        resume_text: Resume text content
        jd_text: Job description text content
        
    Returns:
        Similarity score between 0 and 1
    """
    try:
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2),
            lowercase=True
        )
        
        # Fit and transform both texts
        texts = [resume_text, jd_text]
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        similarity_score = similarity_matrix[0][0]
        
        return similarity_score
    
    except Exception as e:
        logger.error(f"Error in TF-IDF similarity calculation: {e}")
        raise

def calculate_detailed_semantic_match(resume_data, jd_data):
    """
    Calculate detailed semantic match with breakdown using Ollama for analysis.
    
    Returns:
    dict: Detailed breakdown of semantic similarities
    """
    try:
        # Extract text from data
        if isinstance(resume_data, dict):
            resume_text = resume_data.get('raw_text', '')
            resume_skills = resume_data.get('skills', [])
        else:
            resume_text = str(resume_data)
            resume_skills = []
        
        if isinstance(jd_data, dict):
            jd_text = jd_data.get('raw_text', '')
            jd_skills = jd_data.get('required_skills', {}).get('required', [])
        else:
            jd_text = str(jd_data)
            jd_skills = []
        
        # Overall semantic similarity using Ollama
        overall_similarity = calculate_semantic_match(resume_data, jd_data, use_ollama=True)
        
        # Skills-specific similarity
        skills_similarity = 0.0
        if resume_skills and jd_skills:
            resume_skills_text = ' '.join(resume_skills)
            jd_skills_text = ' '.join(jd_skills)
            skills_similarity = calculate_semantic_match(resume_skills_text, jd_skills_text, use_ollama=True) if resume_skills_text and jd_skills_text else 0.0
        
        # Get detailed analysis from Ollama
        detailed_analysis = _get_ollama_detailed_analysis(resume_text, jd_text)
        
        return {
            'overall_similarity': overall_similarity,
            'skills_similarity': skills_similarity,
            'detailed_analysis': detailed_analysis,
            'weighted_score': (overall_similarity * 0.7) + (skills_similarity * 0.3)
        }
    
    except Exception as e:
        logger.error(f"Error calculating detailed semantic match: {e}")
        return {
            'overall_similarity': 0.0,
            'skills_similarity': 0.0,
            'detailed_analysis': "Analysis failed",
            'weighted_score': 0.0
        }

def _get_ollama_detailed_analysis(resume_text: str, jd_text: str) -> str:
    """
    Get detailed analysis of resume-job match using Ollama.
    
    Args:
        resume_text: Resume text content
        jd_text: Job description text content
        
    Returns:
        Detailed analysis text
    """
    try:
        if not _check_ollama_availability():
            return "Detailed analysis unavailable - Ollama not accessible"
        
        prompt = f"""
Provide a brief analysis of how well this resume matches the job description. 
Focus on:
1. Key strengths and alignments
2. Potential gaps or missing skills
3. Overall fit assessment

RESUME:
{resume_text[:1500]}...

JOB DESCRIPTION:
{jd_text[:1500]}...

Keep the analysis concise (under 200 words).
"""
        
        response = ollama.generate(
            model='llama3.2',
            prompt=prompt,
            options={
                'temperature': 0.3,
                'num_predict': 200
            }
        )
        
        return response.get('response', 'Analysis unavailable')
    
    except Exception as e:
        logger.error(f"Error getting detailed analysis: {e}")
        return f"Analysis error: {str(e)}"

def get_available_ollama_models():
    """
    Get list of available Ollama models.
    
    Returns:
        list: Available model names
    """
    try:
        models = ollama.list()
        return [model['name'] for model in models.get('models', [])]
    except Exception as e:
        logger.error(f"Error getting Ollama models: {e}")
        return []