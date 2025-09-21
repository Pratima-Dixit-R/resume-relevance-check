import numpy as np
from typing import List, Union, Optional
import logging
from functools import lru_cache

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available. Using fallback embeddings.")

class EmbeddingManager:
    """Advanced embedding manager using Sentence Transformers for better semantic understanding"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the embedding manager with a pre-trained model
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self._model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self._model = SentenceTransformer(self.model_name)
                logging.info(f"Loaded sentence transformer model: {self.model_name}")
            except Exception as e:
                logging.error(f"Failed to load model {self.model_name}: {e}")
                self._model = None
        else:
            logging.warning("Sentence transformers not available, using TF-IDF fallback")
    
    @lru_cache(maxsize=128)
    def create_embeddings(self, text: str) -> np.ndarray:
        """Create embeddings from input text
        
        Args:
            text: Input text to create embeddings for
            
        Returns:
            numpy array containing the embeddings
        """
        if not text or not text.strip():
            return np.zeros(384)  # Default embedding size for MiniLM
        
        if self._model is not None:
            try:
                # Use sentence transformers for high-quality embeddings
                embeddings = self._model.encode(text.strip(), normalize_embeddings=True)
                return embeddings
            except Exception as e:
                logging.error(f"Error creating embeddings: {e}")
                return self._fallback_embeddings(text)
        else:
            return self._fallback_embeddings(text)
    
    def _fallback_embeddings(self, text: str) -> np.ndarray:
        """Fallback method using simple text features when transformers are unavailable"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        try:
            # Simple TF-IDF based embeddings as fallback
            vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text])
            return tfidf_matrix.toarray()[0]
        except Exception:
            # Ultimate fallback - zeros
            return np.zeros(384)
    
    def create_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for multiple texts efficiently
        
        Args:
            texts: List of texts to create embeddings for
            
        Returns:
            numpy array with shape (n_texts, embedding_dim)
        """
        if self._model is not None:
            try:
                embeddings = self._model.encode(texts, normalize_embeddings=True)
                return embeddings
            except Exception as e:
                logging.error(f"Error creating batch embeddings: {e}")
                return np.array([self._fallback_embeddings(text) for text in texts])
        else:
            return np.array([self._fallback_embeddings(text) for text in texts])
    
    def compare_embeddings(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compare two embeddings and return similarity score
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        try:
            # Ensure embeddings are 2D for sklearn
            if embedding1.ndim == 1:
                embedding1 = embedding1.reshape(1, -1)
            if embedding2.ndim == 1:
                embedding2 = embedding2.reshape(1, -1)
            
            similarity = cosine_similarity(embedding1, embedding2)[0][0]
            return float(np.clip(similarity, 0, 1))
        except Exception as e:
            logging.error(f"Error comparing embeddings: {e}")
            return 0.0
    
    def normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """Normalize embeddings for consistent comparison
        
        Args:
            embeddings: Input embeddings to normalize
            
        Returns:
            Normalized embeddings
        """
        try:
            from sklearn.preprocessing import normalize
            return normalize(embeddings, norm='l2')
        except Exception as e:
            logging.error(f"Error normalizing embeddings: {e}")
            return embeddings
    
    def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """Get semantic similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            emb1 = self.create_embeddings(text1)
            emb2 = self.create_embeddings(text2)
            return self.compare_embeddings(emb1, emb2)
        except Exception as e:
            logging.error(f"Error calculating semantic similarity: {e}")
            return 0.0

# Global embedding manager instance
_embedding_manager = None

def get_embedding_manager() -> EmbeddingManager:
    """Get or create global embedding manager instance"""
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = EmbeddingManager()
    return _embedding_manager

# Convenience functions for backward compatibility
def create_embeddings(text: str) -> np.ndarray:
    """Create embeddings from input text"""
    return get_embedding_manager().create_embeddings(text)

def compare_embeddings(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Compare two embeddings and return similarity score"""
    return get_embedding_manager().compare_embeddings(embedding1, embedding2)

def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    """Normalize embeddings for consistent comparison"""
    return get_embedding_manager().normalize_embeddings(embeddings)

# Export all functions
__all__ = [
    'EmbeddingManager', 'get_embedding_manager', 
    'create_embeddings', 'compare_embeddings', 'normalize_embeddings'
]