"""
Streamlit App for Resume AI Analyzer
This is the main file for Streamlit Cloud deployment.
"""

import streamlit as st
import tempfile
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
from pathlib import Path
import glob
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🤖 Resume AI Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced responsive CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
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
    }
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

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
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
    """Calculate semantic similarity using TF-IDF"""
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
    st.markdown('<h1 class="main-header">🤖 Resume AI Analyzer</h1>', unsafe_allow_html=True)
    
    # Check AI status
    ai_available = check_ai_status()
    
    # Sidebar
    st.sidebar.header("🚀 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📋 Upload & Analyze", 
        "📊 Analytics",
        "📋 View Results"
    ])
    
    # AI settings
    st.sidebar.header("🤖 AI Settings")
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"], index=1)
    
    if page == "📋 Upload & Analyze":
        upload_and_analyze_page(analysis_depth)
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "📋 View Results":
        view_results_page()

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
        
        # Calculate scores
        status_text.text('🧮 Calculating scores...')
        progress_bar.progress(60)
        
        hard_match_score, missing_keywords = calculate_hard_match(resume_data, jd_data)
        semantic_match_score = calculate_semantic_match(resume_data, jd_data)
        
        progress_bar.progress(80)
        status_text.text('🏆 Generating verdict...')
        
        verdict_info = get_detailed_verdict(hard_match_score, semantic_match_score, missing_keywords)
        
        progress_bar.progress(100)
        status_text.text('✅ Analysis complete!')
        
        # Display results
        display_results(hard_match_score, semantic_match_score, verdict_info)
        
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
        progress_bar.empty()
        status_text.empty()

def display_results(hard_match_score, semantic_match_score, verdict_info):
    """Display analysis results"""
    st.success("✅ Analysis completed successfully!")
    
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
    
    # Visualization
    st.markdown("### 📊 Score Breakdown")
    
    scores = [hard_match_score, semantic_match_score, verdict_info['combined_score']]
    labels = ['Hard Match', 'Semantic Match', 'Final Score']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[
        go.Bar(x=labels, y=scores, marker_color=colors,
               text=[f"{score:.1f}%" for score in scores],
               textposition='auto')
    ])
    
    fig.update_layout(
        title="Resume Relevance Analysis",
        yaxis_title="Score (%)",
        yaxis_range=[0, 100],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def analytics_page():
    """Analytics page"""
    st.header("📊 Analytics & Insights")
    
    if st.session_state.analysis_history:
        df = pd.DataFrame(st.session_state.analysis_history)
        
        # Convert scores to numeric
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
        
        # Detailed history table
        st.subheader("📋 Analysis History")
        st.dataframe(df[['timestamp', 'final_score', 'verdict', 'data_source']], use_container_width=True)
        
    else:
        st.info("📊 No analysis history available.")

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