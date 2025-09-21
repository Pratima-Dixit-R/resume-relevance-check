from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
from src.utils.embeddings import get_embedding_manager

def calculate_semantic_match(resume_data, jd_data, use_transformers=True):
    """
    Calculate semantic similarity between resume and job description using advanced embeddings.
    
    Parameters:
    resume_data (dict or str): Resume data or text
    jd_data (dict or str): Job description data or text
    use_transformers (bool): Whether to use transformer-based embeddings
    
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
        if use_transformers:
            # Use advanced transformer-based embeddings
            similarity_score = _calculate_transformer_similarity(resume_text, jd_text)
        else:
            # Fallback to TF-IDF based similarity
            similarity_score = _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Scale the similarity score to a range of 0 to 100
        relevance_score = np.clip(similarity_score * 100, 0, 100)
        
        return float(relevance_score)
    
    except Exception as e:
        logging.error(f"Error calculating semantic match: {e}")
        # Fallback to TF-IDF if transformers fail
        try:
            similarity_score = _calculate_tfidf_similarity(resume_text, jd_text)
            return float(np.clip(similarity_score * 100, 0, 100))
        except Exception as e2:
            logging.error(f"Fallback semantic matching also failed: {e2}")
            return 0.0

def _calculate_transformer_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate similarity using sentence transformers for better semantic understanding.
    
    Args:
        resume_text: Resume text content
        jd_text: Job description text content
        
    Returns:
        Similarity score between 0 and 1
    """
    try:
        embedding_manager = get_embedding_manager()
        
        # Get embeddings for both texts
        resume_embedding = embedding_manager.create_embeddings(resume_text)
        jd_embedding = embedding_manager.create_embeddings(jd_text)
        
        # Calculate cosine similarity
        similarity = embedding_manager.compare_embeddings(resume_embedding, jd_embedding)
        
        return similarity
    
    except Exception as e:
        logging.error(f"Error in transformer similarity calculation: {e}")
        raise

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
        logging.error(f"Error in TF-IDF similarity calculation: {e}")
        raise

def calculate_detailed_semantic_match(resume_data, jd_data):
    """
    Calculate detailed semantic match with breakdown of different aspects.
    
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
        
        # Overall semantic similarity
        overall_similarity = calculate_semantic_match(resume_data, jd_data)
        
        # Skills-specific similarity if available
        skills_similarity = 0.0
        if resume_skills and jd_skills:
            resume_skills_text = ' '.join(resume_skills)
            jd_skills_text = ' '.join(jd_skills)
            skills_similarity = calculate_semantic_match(resume_skills_text, jd_skills_text) if resume_skills_text and jd_skills_text else 0.0
        
        # Content sections similarity (if we can extract different sections)
        sections_similarity = _calculate_sections_similarity(resume_text, jd_text)
        
        return {
            'overall_similarity': overall_similarity,
            'skills_similarity': skills_similarity,
            'sections_similarity': sections_similarity,
            'weighted_score': (overall_similarity * 0.6) + (skills_similarity * 0.3) + (sections_similarity * 0.1)
        }
    
    except Exception as e:
        logging.error(f"Error calculating detailed semantic match: {e}")
        return {
            'overall_similarity': 0.0,
            'skills_similarity': 0.0,
            'sections_similarity': 0.0,
            'weighted_score': 0.0
        }

def _calculate_sections_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate similarity between different sections of resume and job description.
    
    This is a simplified version - in practice, you might want to implement
    more sophisticated section extraction and comparison.
    """
    try:
        # Simple approach: compare first and last parts of documents
        resume_parts = resume_text.split('\n\n')
        jd_parts = jd_text.split('\n\n')
        
        if len(resume_parts) < 2 or len(jd_parts) < 2:
            return 0.0
        
        # Compare intro sections
        intro_similarity = calculate_semantic_match(resume_parts[0], jd_parts[0])
        
        return intro_similarity / 100.0  # Convert back to 0-1 scale
    
    except Exception:
        return 0.0