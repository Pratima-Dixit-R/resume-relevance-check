from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_semantic_match(resume_data, jd_data):
    """
    Calculate semantic similarity between resume and job description.
    
    Parameters:
    resume_data (dict or str): Resume data or text
    jd_data (dict or str): Job description data or text
    
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
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 2)
    )
    
    try:
        # Fit and transform both texts
        texts = [resume_text, jd_text]
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        similarity_score = similarity_matrix[0][0]
        
        # Scale the similarity score to a range of 0 to 100
        relevance_score = np.clip(similarity_score * 100, 0, 100)
        
        return float(relevance_score)
    
    except Exception as e:
        print(f"Error calculating semantic match: {e}")
        return 0.0