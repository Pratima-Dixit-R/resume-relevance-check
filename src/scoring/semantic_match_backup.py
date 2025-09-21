import logging
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List, Optional, Tuple
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AI Backend Imports - Hugging Face Primary (NO Ollama)
try:
    from transformers import pipeline
    HUGGINGFACE_LLM_AVAILABLE = True
    logger.info("✅ Hugging Face LLM backend available")
except ImportError:
    pipeline = None
    HUGGINGFACE_LLM_AVAILABLE = False
    logger.warning("❌ Hugging Face LLM not available")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    logger.info("✅ Sentence Transformers backend available")
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("❌ Sentence Transformers not available")

try:
    import spacy
    SPACY_AVAILABLE = True
    logger.info("✅ spaCy backend available")
except ImportError:
    spacy = None
    SPACY_AVAILABLE = False
    logger.warning("❌ spaCy not available")

# LangChain imports for enhanced AI capabilities
try:
    from langchain_huggingface import HuggingFacePipeline
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_HF_AVAILABLE = True
    logger.info("✅ LangChain with Hugging Face backend available")
except ImportError:
    try:
        from langchain_community.llms import HuggingFacePipeline
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        LANGCHAIN_HF_AVAILABLE = True
        logger.info("✅ LangChain with Hugging Face backend available (community)")
    except ImportError:
        HuggingFacePipeline = None
        PromptTemplate = None
        LLMChain = None
        LANGCHAIN_HF_AVAILABLE = False
        logger.warning("❌ LangChain with Hugging Face not available")

# Global model cache - NO Ollama references
_sentence_model = None
_spacy_model = None
_hf_pipeline = None

def _get_huggingface_pipeline():
    """Get or initialize optimized Hugging Face pipeline for resume analysis."""
    global _hf_pipeline
    
    if _hf_pipeline is None and HUGGINGFACE_LLM_AVAILABLE and pipeline is not None:
        try:
            # Use DistilGPT-2 for fast, efficient text generation
            model_name = "distilgpt2"
            _hf_pipeline = pipeline(
                "text-generation",
                model=model_name,
                max_length=128,
                do_sample=True,
                temperature=0.3,
                pad_token_id=50256
            )
            logger.info(f"✅ Hugging Face pipeline loaded: {model_name}")
                
        except Exception as e:
            logger.error(f"❌ Failed to load Hugging Face pipeline: {e}")
            _hf_pipeline = None
            
    return _hf_pipeline

def _get_sentence_transformer_model():
    """Get or initialize Sentence Transformer model."""
    global _sentence_model
    if _sentence_model is None and SENTENCE_TRANSFORMERS_AVAILABLE:
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

def _calculate_huggingface_llama_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate similarity using Hugging Face Llama 3 model."""
    try:
        pipeline_model = _get_llama_model()
        if pipeline_model is None:
            logger.warning("Hugging Face LLM not available, falling back to Sentence Transformers")
            return _calculate_transformer_similarity(resume_text, jd_text)
        
        # Create a focused prompt for resume-job matching
        prompt = f"""Analyze the match between this resume and job description. Rate similarity from 0.0 to 1.0.

Resume: {resume_text[:800]}...

Job Description: {jd_text[:800]}...

Similarity score (0.0-1.0):"""
        
        # Generate response
        response = pipeline_model(
            prompt,
            max_new_tokens=10,
            num_return_sequences=1,
            temperature=0.1,
            do_sample=True
        )
        
        # Extract score from response
        generated_text = response[0]['generated_text']
        score_text = generated_text.replace(prompt, "").strip()
        
        # Extract numerical score
        import re
        score_match = re.search(r'(0\.[0-9]+|1\.0|0|1)', score_text)
        if score_match:
            score = float(score_match.group(1))
            return min(max(score, 0.0), 1.0)
        else:
            logger.warning(f"Could not parse Hugging Face score: {score_text}")
            return _calculate_transformer_similarity(resume_text, jd_text)
            
    except Exception as e:
        logger.error(f"Hugging Face LLM similarity calculation failed: {e}")
        return _calculate_transformer_similarity(resume_text, jd_text)

def _calculate_langchain_huggingface_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate semantic similarity using LangChain with Hugging Face integration.
    Provides enhanced prompt engineering and response parsing.
    """
    try:
        pipeline_model = _get_llama_model()
        if pipeline_model is None or not LANGCHAIN_HF_AVAILABLE:
            return _calculate_huggingface_llama_similarity(resume_text, jd_text)
        
        # Initialize LangChain Hugging Face LLM
        llm = HuggingFacePipeline(pipeline=pipeline_model)
        
        # Create enhanced prompt template
        prompt_template = PromptTemplate(
            input_variables=["resume", "job_description"],
            template="""
You are an expert HR analyst specializing in resume-job description matching for Innomatics Research Labs.

Analyze the semantic similarity between this resume and job description with focus on:

1. TECHNICAL SKILLS ALIGNMENT (40% weight):
   - Programming languages, frameworks, tools
   - Domain-specific technologies
   - Certifications and qualifications

2. EXPERIENCE RELEVANCE (30% weight):
   - Years of experience in relevant domains
   - Project complexity and scope
   - Leadership and team management

3. DOMAIN EXPERTISE (20% weight):
   - Industry knowledge
   - Research background
   - Academic qualifications

4. ROLE RESPONSIBILITIES (10% weight):
   - Job function alignment
   - Career progression match
   - Cultural fit indicators

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Provide ONLY a numerical similarity score between 0.0 and 1.0 (e.g., 0.75).
No explanation, no text, just the number.
"""
        )
        
        # Create LLM chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        # Process with limited text to avoid token limits
        resume_excerpt = resume_text[:1000]
        jd_excerpt = jd_text[:1000]
        
        # Execute chain
        result = chain.run(
            resume=resume_excerpt,
            job_description=jd_excerpt
        )
        
        # Parse result
        import re
        score_match = re.search(r'(0\.[0-9]+|1\.0|0|1)', result.strip())
        if score_match:
            score = float(score_match.group(1))
            return min(max(score, 0.0), 1.0)
        else:
            logger.warning(f"Could not parse LangChain Hugging Face score: {result}")
            return 0.5
            
    except Exception as e:
        logger.error(f"Error in LangChain Hugging Face similarity calculation: {e}")
        # Fallback to direct Hugging Face
        return _calculate_huggingface_llama_similarity(resume_text, jd_text)

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

def calculate_semantic_match(resume_data: Dict[str, Any], jd_data: Dict[str, Any], use_huggingface: bool = True) -> float:
    """Calculate semantic similarity between resume and job description using Hugging Face."""
    try:
        resume_text = resume_data.get('raw_text', '')
        jd_text = jd_data.get('raw_text', '')
        
        if not resume_text or not jd_text:
            logger.warning("Empty text provided for semantic matching")
            return 0.0
        
        # Try different backends in order of preference (Hugging Face first)
        if use_huggingface and HUGGINGFACE_LLM_AVAILABLE:
            score = _calculate_huggingface_llama_similarity(resume_text, jd_text)
            logger.info(f"Hugging Face LLM semantic similarity: {score:.3f}")
            return score * 100
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            score = _calculate_transformer_similarity(resume_text, jd_text)
            logger.info(f"Sentence Transformer semantic similarity: {score:.3f}")
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
        
        # Try all available backends (prioritize Hugging Face LLM)
        if LANGCHAIN_HF_AVAILABLE and HUGGINGFACE_LLM_AVAILABLE:
            backend_scores['langchain_huggingface'] = _calculate_langchain_huggingface_similarity(resume_text, jd_text)
        elif HUGGINGFACE_LLM_AVAILABLE:
            backend_scores['huggingface_llm'] = _calculate_huggingface_llama_similarity(resume_text, jd_text)
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            backend_scores['sentence_transformers'] = _calculate_transformer_similarity(resume_text, jd_text)
        
        if SPACY_AVAILABLE:
            backend_scores['spacy'] = _calculate_spacy_similarity(resume_text, jd_text)
        
        # Always include TF-IDF as baseline
        backend_scores['tfidf'] = _calculate_tfidf_similarity(resume_text, jd_text)
        
        # Calculate weighted average (prefer Hugging Face LLM, then other AI models over TF-IDF)
        weights = {
            'langchain_huggingface': 0.5,
            'huggingface_llm': 0.4,
            'sentence_transformers': 0.3,
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
        if 'langchain_huggingface' in backend_scores:
            analysis_parts.append(f"Enhanced AI Analysis (LangChain+Hugging Face): {backend_scores['langchain_huggingface']:.1%}")
        elif 'huggingface_llm' in backend_scores:
            analysis_parts.append(f"AI Analysis (Hugging Face LLM): {backend_scores['huggingface_llm']:.1%}")
        if 'sentence_transformers' in backend_scores:
            analysis_parts.append(f"Neural Embeddings: {backend_scores['sentence_transformers']:.1%}")
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