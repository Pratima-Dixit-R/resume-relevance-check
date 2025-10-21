"""
Advanced Resume Relevance Checker - Streamlit Cloud Version
This is an enhanced version with sample data integration and advanced analysis features.
"""

import streamlit as st
import tempfile
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
from pathlib import Path
import glob
import random
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🤖 Advanced Resume AI Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced responsive CSS with mobile app-like features
st.markdown("""
<style>
    /* Mobile app-like styling */
    body {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        overscroll-behavior: none;
    }
    
    /* Responsive design for all devices */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem !important;
        }
        .stButton>button {
            width: 100% !important;
            margin-bottom: 10px !important;
            padding: 15px !important;
            font-size: 1.1rem !important;
        }
        .stSidebar {
            width: 100% !important;
        }
        .stDataFrame {
            font-size: 0.8rem !important;
        }
        /* Mobile-specific styling */
        .stApp {
            padding: 10px !important;
        }
        .block-container {
            padding: 10px !important;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem !important;
        }
        .metric-card {
            padding: 0.5rem !important;
        }
        .stMetric {
            font-size: 0.9rem !important;
        }
        /* Compact mobile view */
        .stExpander {
            margin-bottom: 5px !important;
        }
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        -webkit-text-stroke: 0.5px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4ECDC4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .ai-status {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 2px solid #ffffff;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    .sample-data-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .auth-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Cross-browser compatibility */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Smooth animations for app-like feel */
    .stButton>button {
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'sample_data_loaded' not in st.session_state:
    st.session_state.sample_data_loaded = False

def get_sample_data_paths():
    """Get paths to sample resume and job description files."""
    base_path = Path(__file__).parent
    
    # Sample resumes
    resume_paths = {
        "Sample Resume Collection": list(glob.glob(str(base_path / "data" / "data" / "sample_resumes" / "Resumes" / "*.pdf"))),
        "Additional Resume Samples": list(glob.glob(str(base_path / "sample_resumes" / "*.txt")))
    }
    
    # Sample job descriptions
    jd_paths = {
        "Sample Job Descriptions": list(glob.glob(str(base_path / "data" / "sample_jds" / "JD" / "*.pdf"))),
        "Additional JD Samples": list(glob.glob(str(base_path / "sample_jds" / "*.txt")))
    }
    
    return resume_paths, jd_paths

def load_sample_file(file_path):
    """Load a sample file and return its content."""
    try:
        if file_path.endswith('.pdf'):
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file {file_path}: {e}")
        return None

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file (simplified version)"""
    try:
        # For PDF files
        if uploaded_file.name.endswith('.pdf'):
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        # For text files
        elif uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8')
        # For DOCX files
        elif uploaded_file.name.endswith('.docx'):
            from docx import Document
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                doc = Document(tmp_file.name)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                os.unlink(tmp_file.name)
                return text
        else:
            # Try to read as text
            return uploaded_file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

def calculate_hard_match(resume_data, jd_data):
    """Calculate hard match score based on keyword matching"""
    try:
        resume_text = resume_data.get('raw_text', '').lower()
        jd_text = jd_data.get('raw_text', '').lower()
        
        if not resume_text or not jd_text:
            return 0.0, []
        
        # Simple keyword matching approach
        # Extract potential keywords from JD (simplified)
        jd_words = set(jd_text.split())
        resume_words = set(resume_text.split())
        
        # Calculate overlap
        common_words = jd_words.intersection(resume_words)
        missing_words = jd_words - resume_words
        total_jd_words = len(jd_words)
        
        if total_jd_words == 0:
            return 0.0, []
            
        score = (len(common_words) / total_jd_words) * 100
        return min(score, 100.0), list(missing_words)
        
    except Exception as e:
        logger.error(f"Hard match calculation failed: {e}")
        return 0.0, []

def calculate_semantic_match(resume_data, jd_data):
    """Calculate semantic similarity using TF-IDF as fallback"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        resume_text = resume_data.get('raw_text', '')
        jd_text = jd_data.get('raw_text', '')
        
        if not resume_text or not jd_text:
            return 0.0
        
        # Clean texts
        def _clean_text(text):
            import re
            if not text:
                return ""
            # Remove extra whitespace and normalize
            text = re.sub(r'\s+', ' ', text.strip())
            # Remove special characters but keep important punctuation
            text = re.sub(r'[^\w\s\.,!?;:()-]', ' ', text)
            return text.lower()
        
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
        
        return max(0.0, min(100.0, float(similarity) * 100))
        
    except Exception as e:
        logger.error(f"Semantic matching failed: {e}")
        return 0.0

def extract_key_sections(text):
    """Extract key sections from resume or JD text"""
    sections = {
        'experience': [],
        'skills': [],
        'education': [],
        'projects': []
    }
    
    # Simple section extraction based on common headers
    lines = text.split('\n')
    current_section = None
    
    experience_keywords = ['experience', 'work', 'employment', 'professional']
    skills_keywords = ['skills', 'technologies', 'tools', 'competencies']
    education_keywords = ['education', 'academic', 'university', 'degree']
    projects_keywords = ['projects', 'portfolio', 'work samples']
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Detect section headers
        if any(keyword in line_lower for keyword in experience_keywords):
            current_section = 'experience'
        elif any(keyword in line_lower for keyword in skills_keywords):
            current_section = 'skills'
        elif any(keyword in line_lower for keyword in education_keywords):
            current_section = 'education'
        elif any(keyword in line_lower for keyword in projects_keywords):
            current_section = 'projects'
        
        # Add content to current section
        if current_section and line.strip() and not any(keyword in line_lower for keyword in 
            experience_keywords + skills_keywords + education_keywords + projects_keywords):
            sections[current_section].append(line.strip())
    
    return sections

def calculate_section_scores(resume_sections, jd_sections):
    """Calculate scores for each section"""
    section_scores = {}
    
    for section in ['experience', 'skills', 'education', 'projects']:
        resume_text = ' '.join(resume_sections.get(section, []))
        jd_text = ' '.join(jd_sections.get(section, []))
        
        if not jd_text:
            section_scores[section] = 100.0  # No requirements, full score
            continue
        
        if not resume_text:
            section_scores[section] = 0.0  # No content, no score
            continue
        
        # Calculate similarity for this section
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 1))
            tfidf_matrix = vectorizer.fit_transform([resume_text.lower(), jd_text.lower()])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            section_scores[section] = max(0.0, min(100.0, float(similarity) * 100))
        except:
            section_scores[section] = 0.0
    
    return section_scores

def get_detailed_verdict(hard_match_score, semantic_match_score, missing_keywords=None):
    """Generate detailed verdict based on scores"""
    combined_score = (hard_match_score + semantic_match_score) / 2
    
    if combined_score >= 80:
        verdict = "High"
        explanation = "✅ Excellent match! Your resume aligns well with the job requirements. Strongly recommended to apply."
        recommendation = "Your resume is well-aligned with this position. Consider highlighting your most relevant achievements."
    elif combined_score >= 60:
        verdict = "Medium"
        explanation = "🟡 Good match with some gaps. Consider tailoring your resume more closely to the job description."
        recommendation = "Focus on strengthening areas where keywords are missing and emphasize transferable skills."
    else:
        verdict = "Low"
        explanation = "🔴 Limited match. Significant gaps identified. Consider gaining more relevant experience or skills."
        recommendation = "Consider gaining additional relevant experience or skills. Tailor your resume to better match the job requirements."
    
    # Generate keyword gap analysis
    keyword_analysis = ""
    if missing_keywords and len(missing_keywords) > 0:
        top_missing = missing_keywords[:10]  # Top 10 missing keywords
        keyword_analysis = f"**Key Missing Keywords:** {', '.join(top_missing)}"
    
    return {
        'combined_score': combined_score,
        'verdict': verdict,
        'explanation': explanation,
        'recommendation': recommendation,
        'keyword_analysis': keyword_analysis
    }

def check_ai_status():
    """Check AI backend status"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        status_info = ["✅ TF-IDF Vectorizer available", "✅ Cosine Similarity available"]
        
        st.markdown(f'''
        <div class="ai-status">
            🟢 <strong>AI Status:</strong> Active | {" | ".join(status_info)}
        </div>
        ''', unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"❌ AI Status Error: {e}")
        return False

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 Advanced Resume AI Analyzer</h1>', unsafe_allow_html=True)
    
    # Check AI status
    ai_available = check_ai_status()
    
    # Sidebar
    st.sidebar.header("🚀 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📋 Upload & Analyze", 
        "📂 Sample Data",
        "📊 Analytics",
        "📋 View Results"
    ])
    
    # AI settings
    st.sidebar.header("🤖 AI Settings")
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"], index=1)
    
    # Advanced AI settings
    with st.sidebar.expander("🔬 Advanced Analysis"):
        st.markdown("### Deep Analysis Settings")
        enable_keyword_analysis = st.checkbox("Enable Keyword Gap Analysis", value=True)
        enable_skill_matching = st.checkbox("Enable Skill Matching", value=True)
        enable_experience_scoring = st.checkbox("Enable Experience Scoring", value=True)
        min_keyword_match = st.slider("Minimum Keyword Match Threshold", 0, 100, 70)
    
    if page == "📋 Upload & Analyze":
        upload_and_analyze_page(analysis_depth)
    elif page == "📂 Sample Data":
        sample_data_page()
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "📋 View Results":
        view_results_page()

def sample_data_page():
    """Sample data page with quick start options"""
    st.markdown("### 🗂️ Quick Start with Sample Data")
    
    resume_paths, jd_paths = get_sample_data_paths()
    
    # Sample Data Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 Sample Resumes Available:**")
        
        # Show available sample resumes
        total_resumes = sum(len(files) for files in resume_paths.values())
        st.info(f"📊 {total_resumes} sample resumes ready for analysis")
        
        # Display sample resume options
        for category, files in resume_paths.items():
            if files:
                st.markdown(f"**{category}:**")
                for file_path in files[:3]:  # Show first 3 files
                    file_name = os.path.basename(file_path)
                    if st.button(f"📄 {file_name}", key=f"resume_{file_path}"):
                        resume_text = load_sample_file(file_path)
                        if resume_text:
                            st.session_state.resume_text = resume_text
                            st.session_state.resume_processed = True
                            st.session_state.sample_data_loaded = True
                            st.success(f"✅ Loaded: {file_name}")
                            
                            with st.expander("🔍 Preview"):
                                st.text_area("Content", resume_text[:500] + "...", height=150, key=f"preview_resume_{file_path}")
        
        if st.button("🚀 Load Random Sample Resume", type="primary"):
            # Get random resume from all available samples
            all_resumes = []
            for category, files in resume_paths.items():
                all_resumes.extend(files)
            
            if all_resumes:
                selected_resume = random.choice(all_resumes)
                resume_text = load_sample_file(selected_resume)
                
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.session_state.resume_processed = True
                    st.session_state.sample_data_loaded = True
                    st.success(f"✅ Loaded: {os.path.basename(selected_resume)}")
                    
                    with st.expander("🔍 Preview"):
                        st.text_area("Content", resume_text[:500] + "...", height=150, key="random_resume_preview")
    
    with col2:
        st.markdown("**💼 Sample Job Descriptions Available:**")
        
        # Show available sample JDs
        total_jds = sum(len(files) for files in jd_paths.values())
        st.info(f"📊 {total_jds} sample job descriptions ready for analysis")
        
        # Display sample JD options
        for category, files in jd_paths.items():
            if files:
                st.markdown(f"**{category}:**")
                for file_path in files[:3]:  # Show first 3 files
                    file_name = os.path.basename(file_path)
                    if st.button(f"💼 {file_name}", key=f"jd_{file_path}"):
                        jd_text = load_sample_file(file_path)
                        if jd_text:
                            st.session_state.jd_text = jd_text
                            st.session_state.jd_processed = True
                            st.session_state.sample_data_loaded = True
                            st.success(f"✅ Loaded: {file_name}")
                            
                            with st.expander("🔍 Preview"):
                                st.text_area("Content", jd_text[:500] + "...", height=150, key=f"preview_jd_{file_path}")
        
        if st.button("🚀 Load Random Sample JD", type="primary"):
            # Get random JD from all available samples
            all_jds = []
            for category, files in jd_paths.items():
                all_jds.extend(files)
            
            if all_jds:
                selected_jd = random.choice(all_jds)
                jd_text = load_sample_file(selected_jd)
                
                if jd_text:
                    st.session_state.jd_text = jd_text
                    st.session_state.jd_processed = True
                    st.session_state.sample_data_loaded = True
                    st.success(f"✅ Loaded: {os.path.basename(selected_jd)}")
                    
                    with st.expander("🔍 Preview"):
                        st.text_area("Content", jd_text[:500] + "...", height=150, key="random_jd_preview")

def upload_and_analyze_page(analysis_depth):
    """Upload and analysis page"""
    st.markdown("### 📁 Upload Your Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📁 Job Description")
        jd_file = st.file_uploader("Choose a job description file", type=["pdf", "docx", "txt"], key="jd")
        
        if jd_file is not None:
            st.info(f"File: {jd_file.name} ({jd_file.size} bytes)")
            if st.button("🔄 Process Job Description", type="secondary"):
                with st.spinner("Processing job description..."):
                    jd_text = extract_text_from_file(jd_file)
                    if jd_text:
                        st.session_state.jd_text = jd_text
                        st.session_state.jd_processed = True
                        st.session_state.sample_data_loaded = False
                        st.success("✅ Job Description processed!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", jd_text[:500] + "...", height=150)
    
    with col2:
        st.header("📄 Resume")
        resume_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"], key="resume")
        
        if resume_file is not None:
            st.info(f"File: {resume_file.name} ({resume_file.size} bytes)")
            if st.button("🔄 Process Resume", type="secondary"):
                with st.spinner("Processing resume..."):
                    resume_text = extract_text_from_file(resume_file)
                    if resume_text:
                        st.session_state.resume_text = resume_text
                        st.session_state.resume_processed = True
                        st.session_state.sample_data_loaded = False
                        st.success("✅ Resume processed!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", resume_text[:500] + "...", height=150)
    
    # Analysis section
    if getattr(st.session_state, 'jd_processed', False) and getattr(st.session_state, 'resume_processed', False):
        st.markdown("---")
        st.header("🤖 AI-Powered Analysis")
        
        # Show data source
        if st.session_state.sample_data_loaded:
            st.info("ℹ️ Using sample data for analysis")
        else:
            st.info("ℹ️ Using uploaded data for analysis")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 Start AI Analysis", type="primary"):
                perform_analysis(analysis_depth)
    else:
        st.info("📝 Please upload and process both resume and job description to start analysis.")

def perform_analysis(analysis_depth):
    """Perform analysis"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize
        status_text.text('🔄 Initializing analysis...')
        progress_bar.progress(20)
        
        # Prepare data
        status_text.text('📊 Preparing data...')
        progress_bar.progress(40)
        
        resume_data = {"raw_text": st.session_state.resume_text}
        jd_data = {"raw_text": st.session_state.jd_text}
        
        # Initialize section variables
        resume_sections = {}
        jd_sections = {}
        section_scores = {}
        
        # Extract sections for deep analysis
        if analysis_depth == "Deep":
            status_text.text('🔍 Extracting sections...')
            resume_sections = extract_key_sections(st.session_state.resume_text)
            jd_sections = extract_key_sections(st.session_state.jd_text)
        
        # Calculate scores
        status_text.text('🧮 Calculating scores...')
        progress_bar.progress(60)
        
        hard_match_score, missing_keywords = calculate_hard_match(resume_data, jd_data)
        semantic_match_score = calculate_semantic_match(resume_data, jd_data)
        
        # Section scores for deep analysis
        if analysis_depth == "Deep":
            status_text.text('📑 Analyzing sections...')
            section_scores = calculate_section_scores(resume_sections, jd_sections)
        
        progress_bar.progress(80)
        status_text.text('🏆 Generating verdict...')
        
        verdict_info = get_detailed_verdict(hard_match_score, semantic_match_score, missing_keywords)
        
        # Add section scores to verdict for deep analysis
        if analysis_depth == "Deep" and section_scores:
            verdict_info['section_scores'] = section_scores
        
        progress_bar.progress(100)
        status_text.text('✅ Analysis complete!')
        
        # Display results
        display_enhanced_results(hard_match_score, semantic_match_score, verdict_info, "")
        
        # Store in history
        st.session_state.analysis_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hard_match': hard_match_score,
            'semantic_match': semantic_match_score,
            'final_score': verdict_info['combined_score'],
            'verdict': verdict_info['verdict'],
            'analysis_depth': analysis_depth,
            'data_source': 'Sample Data' if st.session_state.sample_data_loaded else 'Uploaded Data'
        })
        
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"🚨 Analysis error: {e}")
        import traceback
        st.text(traceback.format_exc())
        progress_bar.empty()
        status_text.empty()

def display_enhanced_results(hard_match_score, semantic_match_score, verdict_info, detailed_analysis):
    """Display enhanced analysis results with advanced visualizations"""
    st.success("✅ Analysis completed successfully!")
    
    # Main metrics in a highlighted section
    st.markdown("### 📊 Key Metrics")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏅 Hard Match", f"{hard_match_score:.1f}%")
    
    with col2:
        st.metric("🤖 Semantic Match", f"{semantic_match_score:.1f}%")
    
    with col3:
        st.metric("🎯 Final Score", f"{verdict_info['combined_score']:.1f}%")
    
    with col4:
        verdict_emoji = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
        st.metric("🏆 Verdict", f"{verdict_emoji.get(verdict_info['verdict'], '🔵')} {verdict_info['verdict']}")
    
    # Detailed explanation
    st.markdown("### 📝 Analysis Summary")
    st.info(verdict_info['explanation'])
    
    # Recommendations
    if 'recommendation' in verdict_info and verdict_info['recommendation']:
        st.markdown("### 💡 Recommendations")
        st.success(verdict_info['recommendation'])
    
    # Keyword gap analysis
    if 'keyword_analysis' in verdict_info and verdict_info['keyword_analysis']:
        st.markdown("### 🔍 Keyword Gap Analysis")
        st.warning(verdict_info['keyword_analysis'])
    
    # Section scores for deep analysis
    if 'section_scores' in verdict_info and verdict_info['section_scores']:
        st.markdown("### 📑 Section Analysis")
        section_data = verdict_info['section_scores']
        section_df = pd.DataFrame({
            'Section': list(section_data.keys()),
            'Score': [f"{score:.1f}%" for score in section_data.values()]
        })
        st.table(section_df)
    
    # Advanced visualizations
    st.markdown("### 📈 Detailed Analysis")
    
    # Create comparison chart
    fig_comparison = go.Figure()
    
    scores = [hard_match_score, semantic_match_score, verdict_info['combined_score']]
    labels = ['Hard Match', 'Semantic Match', 'Final Score']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig_comparison.add_trace(go.Bar(
        x=labels, 
        y=scores, 
        marker_color=colors,
        text=[f"{score:.1f}%" for score in scores],
        textposition='auto'
    ))
    
    fig_comparison.update_layout(
        title="Score Comparison",
        yaxis_title="Score (%)",
        yaxis_range=[0, 100],
        height=400
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Radar chart for comprehensive view
    st.markdown("### 📡 Comprehensive Analysis")
    
    categories = ['Hard Match', 'Semantic Match']
    values = [hard_match_score, semantic_match_score]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Resume Match',
        line_color='#45B7D1'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Match Profile Radar",
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Detailed breakdown
    if detailed_analysis:
        st.markdown("### 🔍 Detailed Breakdown")
        st.text(detailed_analysis)

def analytics_page():
    """Analytics page with advanced data analysis"""
    st.header("📊 Analytics & Insights")
    
    if st.session_state.analysis_history:
        df = pd.DataFrame(st.session_state.analysis_history)
        
        # Convert scores to numeric if they're not already
        df['hard_match'] = pd.to_numeric(df['hard_match'], errors='coerce')
        df['semantic_match'] = pd.to_numeric(df['semantic_match'], errors='coerce')
        df['final_score'] = pd.to_numeric(df['final_score'], errors='coerce')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            st.metric("Average Score", f"{df['final_score'].mean():.1f}%")
        with col3:
            st.metric("Best Score", f"{df['final_score'].max():.1f}%")
        with col4:
            st.metric("Worst Score", f"{df['final_score'].min():.1f}%")
        
        # Score distribution chart
        st.subheader("📈 Score Distribution")
        
        fig_hist = go.Figure(data=[go.Histogram(x=df['final_score'], nbinsx=20)])
        fig_hist.update_layout(
            title="Distribution of Analysis Scores",
            xaxis_title="Score (%)",
            yaxis_title="Frequency",
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Trend analysis
        st.subheader("📈 Score Trend Over Time")
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df_sorted = df.sort_values('timestamp')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_sorted['timestamp'],
            y=df_sorted['final_score'],
            mode='lines+markers',
            name='Score Trend',
            line=dict(color='#45B7D1'),
            marker=dict(size=8)
        ))
        
        fig_trend.update_layout(
            title="Score Trend Over Time",
            xaxis_title="Date",
            yaxis_title="Score (%)",
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Data source distribution
        st.subheader("📊 Data Source Distribution")
        
        source_counts = df['data_source'].value_counts()
        
        fig_source = go.Figure(data=[go.Pie(
            labels=source_counts.index,
            values=source_counts.values,
            marker_colors=['#FF6B6B', '#4ECDC4']
        )])
        
        fig_source.update_layout(
            title="Distribution of Data Sources",
            height=400
        )
        st.plotly_chart(fig_source, use_container_width=True)
        
        # Verdict distribution
        st.subheader("📊 Verdict Distribution")
        
        verdict_counts = df['verdict'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=verdict_counts.index,
            values=verdict_counts.values,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )])
        
        fig_pie.update_layout(
            title="Distribution of Verdicts",
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed history table
        st.subheader("📋 Analysis History")
        st.dataframe(df[['timestamp', 'final_score', 'verdict', 'data_source', 'analysis_depth']], use_container_width=True)
        
        # Performance insights
        st.subheader("💡 Performance Insights")
        
        avg_score = df['final_score'].mean()
        if avg_score >= 80:
            st.success("🏆 Excellent performance! Your resumes consistently match job descriptions well.")
        elif avg_score >= 50:
            st.info("👍 Good performance with room for improvement. Focus on strengthening key skills.")
        else:
            st.warning("⚠️ Consider reviewing your resume content to better align with job requirements.")
            
        # Improvement suggestions
        st.markdown("### 📝 Improvement Suggestions")
        st.markdown("""
        1. **Skill Alignment**: Ensure your resume highlights skills mentioned in job descriptions
        2. **Keyword Optimization**: Use industry-specific terminology from the job posting
        3. **Experience Relevance**: Tailor your experience descriptions to match job requirements
        4. **Format Consistency**: Maintain a clean, professional format that's easy to parse
        """)
        
    else:
        st.info("📊 No analysis history available. Run your first analysis to see insights!")

def view_results_page():
    """View results page"""
    st.header("📋 Recent Results")
    
    if st.session_state.analysis_history:
        for i, result in enumerate(reversed(st.session_state.analysis_history)):
            with st.expander(f"Analysis {len(st.session_state.analysis_history)-i}: {result['verdict']} ({result['final_score']:.1f}%) - {result['data_source']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Timestamp:** {result['timestamp']}")
                    st.write(f"**Hard Match:** {result['hard_match']:.1f}%")
                    st.write(f"**Semantic Match:** {result['semantic_match']:.1f}%")
                with col2:
                    st.write(f"**Analysis Depth:** {result['analysis_depth']}")
                    st.write(f"**Data Source:** {result['data_source']}")
                    st.write(f"**Verdict:** {result['verdict']}")
    else:
        st.info("📋 No results available.")

if __name__ == "__main__":
    main()