import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List, Optional, Tuple
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AI Backend Imports with error handling
try:
    import ollama
    OLLAMA_AVAILABLE = True
    logger.info("Ollama backend available")
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama not available")

try:
    from sentence_transformers import SentenceTransformer
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger.info("Sentence Transformers backend available")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Sentence Transformers not available")

try:
    import spacy
    SPACY_AVAILABLE = True
    logger.info("spaCy backend available")
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("spaCy not available")

# Global model cache
_sentence_model = None
_spacy_model = None

def get_available_ollama_models() -> List[str]:
    """Get list of available Ollama models."""
    if not OLLAMA_AVAILABLE:
        return []
    
    try:
        models = ollama.list()
        return [model['name'] for model in models.get('models', [])]
    except Exception as e:
        logger.error(f"Error fetching Ollama models: {e}")
        return []

def _check_ollama_availability() -> bool:
    """Check if Ollama is available and has models."""
    if not OLLAMA_AVAILABLE:
        return False
    
    try:
        models = get_available_ollama_models()
        return len(models) > 0
    except Exception as e:
        logger.error(f"Ollama availability check failed: {e}")
        return False

def _get_sentence_transformer_model():
    """Get or initialize Sentence Transformer model."""
    global _sentence_model
    if _sentence_model is None and TRANSFORMERS_AVAILABLE:
        try:
            # Use a lightweight, fast model for production
            _sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence Transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Sentence Transformer model: {e}")
            _sentence_model = None
    return _sentence_model

def _get_spacy_model():
    """Get or initialize spaCy model."""
    global _spacy_model
    if _spacy_model is None and SPACY_AVAILABLE:
        try:
            _spacy_model = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            try:
                # Fallback to smaller model
                _spacy_model = spacy.load("en_core_web_sm")
            except:
                _spacy_model = None
    return _spacy_model

def _clean_text(text: str) -> str:
    """Clean and preprocess text."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s\.,!?;:()-]', ' ', text)
    
    return text.lower()

def _calculate_ollama_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate similarity using Ollama LLM."""
    try:
        if not _check_ollama_availability():
            logger.warning("Ollama not available, falling back to TF-IDF")
            return _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Get available models and use the first one
        models = get_available_ollama_models()
        model_name = models[0] if models else 'llama3.2'
        
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
        
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                'temperature': 0.1,
                'num_predict': 10
            }
        )
        
        # Extract numerical score from response
        score_text = response.get('response', '0.0').strip()
        
        # Try to extract a number from the response
        import re
        numbers = re.findall(r'\d+\.\d+|\d+', score_text)
        
        if numbers:
            score = float(numbers[0])
            # Ensure score is between 0 and 1
            if score > 1.0:
                score = score / 100.0  # Convert percentage to decimal
            return max(0.0, min(1.0, score))
        
        logger.warning(f"Could not parse Ollama response: {score_text}")
        return _calculate_tfidf_similarity(resume_text, jd_text)
        
    except Exception as e:
        logger.error(f"Ollama similarity calculation failed: {e}")
        return _calculate_tfidf_similarity(resume_text, jd_text)

def _calculate_transformer_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate similarity using Sentence Transformers."""
    try:
        model = _get_sentence_transformer_model()
        if model is None:
            return _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Encode texts
        resume_embedding = model.encode([_clean_text(resume_text)])
        jd_embedding = model.encode([_clean_text(jd_text)])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
        
        return max(0.0, min(1.0, float(similarity)))
        
    except Exception as e:
        logger.error(f"Transformer similarity calculation failed: {e}")
        return _calculate_tfidf_similarity(resume_text, jd_text)

def _calculate_spacy_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate similarity using spaCy."""
    try:
        nlp = _get_spacy_model()
        if nlp is None:
            return _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Process texts
        resume_doc = nlp(_clean_text(resume_text))
        jd_doc = nlp(_clean_text(jd_text))
        
        # Calculate similarity
        similarity = resume_doc.similarity(jd_doc)
        
        return max(0.0, min(1.0, float(similarity)))
        
    except Exception as e:
        logger.error(f"spaCy similarity calculation failed: {e}")
        return _calculate_tfidf_similarity(resume_text, jd_text)

def _calculate_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate similarity using TF-IDF (fallback method)."""
    try:
        # Clean texts
        resume_clean = _clean_text(resume_text)
        jd_clean = _clean_text(jd_text)
        
        if not resume_clean or not jd_clean:
            return 0.0
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000,
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return max(0.0, min(1.0, float(similarity)))
        
    except Exception as e:
        logger.error(f"TF-IDF similarity calculation failed: {e}")
        return 0.0

def calculate_semantic_match(resume_data: Dict[str, Any], jd_data: Dict[str, Any], use_ollama: bool = True) -> float:
    """Calculate semantic similarity between resume and job description."""
    try:
        resume_text = resume_data.get('raw_text', '')
        jd_text = jd_data.get('raw_text', '')
        
        if not resume_text or not jd_text:
            logger.warning("Empty text provided for semantic matching")
            return 0.0
        
        # Try different backends in order of preference
        if use_ollama and OLLAMA_AVAILABLE:
            score = _calculate_ollama_similarity(resume_text, jd_text)
            logger.info(f"Ollama semantic similarity: {score:.3f}")
            return score * 100
        
        if TRANSFORMERS_AVAILABLE:
            score = _calculate_transformer_similarity(resume_text, jd_text)
            logger.info(f"Transformer semantic similarity: {score:.3f}")
            return score * 100
        
        if SPACY_AVAILABLE:
            score = _calculate_spacy_similarity(resume_text, jd_text)
            logger.info(f"spaCy semantic similarity: {score:.3f}")
            return score * 100
        
        # Fallback to TF-IDF
        score = _calculate_tfidf_similarity(resume_text, jd_text)
        logger.info(f"TF-IDF semantic similarity: {score:.3f}")
        return score * 100
        
    except Exception as e:
        logger.error(f"Semantic matching failed: {e}")
        return 0.0

def calculate_detailed_semantic_match(resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate detailed semantic analysis using multiple backends."""
    try:
        resume_text = resume_data.get('raw_text', '')
        jd_text = jd_data.get('raw_text', '')
        
        if not resume_text or not jd_text:
            return {
                'weighted_score': 0.0,
                'detailed_analysis': 'No text provided for analysis',
                'backend_scores': {}
            }
        
        backend_scores = {}
        
        # Try all available backends
        if OLLAMA_AVAILABLE and _check_ollama_availability():
            backend_scores['ollama'] = _calculate_ollama_similarity(resume_text, jd_text)
        
        if TRANSFORMERS_AVAILABLE:
            backend_scores['transformers'] = _calculate_transformer_similarity(resume_text, jd_text)
        
        if SPACY_AVAILABLE:
            backend_scores['spacy'] = _calculate_spacy_similarity(resume_text, jd_text)
        
        # Always include TF-IDF as baseline
        backend_scores['tfidf'] = _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Calculate weighted average (prefer AI models over TF-IDF)
        weights = {
            'ollama': 0.4,
            'transformers': 0.3,
            'spacy': 0.2,
            'tfidf': 0.1
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for backend, score in backend_scores.items():
            weight = weights.get(backend, 0.1)
            weighted_score += score * weight
            total_weight += weight
        
        if total_weight > 0:
            weighted_score = weighted_score / total_weight
        
        # Generate detailed analysis
        analysis_parts = []
        if 'ollama' in backend_scores:
            analysis_parts.append(f"AI Analysis (Ollama): {backend_scores['ollama']:.1%}")
        if 'transformers' in backend_scores:
            analysis_parts.append(f"Neural Embeddings: {backend_scores['transformers']:.1%}")
        if 'spacy' in backend_scores:
            analysis_parts.append(f"NLP Analysis: {backend_scores['spacy']:.1%}")
        analysis_parts.append(f"Statistical Analysis: {backend_scores['tfidf']:.1%}")
        
        detailed_analysis = "\n".join(analysis_parts)
        
        return {
            'weighted_score': max(0.0, min(100.0, weighted_score * 100)),  # Convert to percentage
            'detailed_analysis': detailed_analysis,
            'backend_scores': {k: v * 100 for k, v in backend_scores.items()}  # Convert to percentages
        }
        
    except Exception as e:
        logger.error(f"Detailed semantic analysis failed: {e}")
        return {
            'weighted_score': 0.0,
            'detailed_analysis': f'Analysis failed: {str(e)}',
            'backend_scores': {}
        }