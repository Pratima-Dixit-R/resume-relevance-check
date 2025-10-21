"""
Professional Resume Analyzer - Advanced AI Analysis
This app provides professional-grade resume analysis similar to LinkedIn, Naukri.com and other top platforms.
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
import json
import base64
import logging
from io import BytesIO
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration with professional styling
st.set_page_config(
    page_title="🎯 Professional Resume AI Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Professional header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #1a2a6c, #2a5298, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1.5rem 0 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Professional card styling */
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    /* Professional status indicator */
    .ai-status {
        background: linear-gradient(135deg, #2c3e50, #4a6491);
        color: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        font-weight: 600;
        text-align: center;
        font-size: 1.1rem;
        border: 2px solid #3498db;
    }
    
    /* Professional button styling */
    .stButton>button {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2980b9, #2573a7);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Professional tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Responsive design for all devices */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem !important;
        }
        
        .metric-card {
            margin-bottom: 1rem;
        }
        
        .stButton>button {
            width: 100% !important;
            margin-bottom: 10px !important;
            padding: 15px !important;
            font-size: 1.1rem !important;
        }
    }
    
    /* Chart container styling */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    /* Report styling */
    .analysis-report {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    /* Section header styling */
    .section-header {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

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

def extract_key_sections(text):
    """Extract key sections from resume or JD text"""
    sections = {
        'experience': [],
        'skills': [],
        'education': [],
        'projects': [],
        'certifications': [],
        'summary': []
    }
    
    # Simple section extraction based on common headers
    lines = text.split('\n')
    current_section = None
    
    experience_keywords = ['experience', 'work', 'employment', 'professional']
    skills_keywords = ['skills', 'technologies', 'tools', 'competencies', 'expertise']
    education_keywords = ['education', 'academic', 'university', 'degree', 'qualification']
    projects_keywords = ['projects', 'portfolio', 'work samples', 'achievements']
    certifications_keywords = ['certifications', 'certificates', 'credentials']
    summary_keywords = ['summary', 'objective', 'profile', 'about']
    
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
        elif any(keyword in line_lower for keyword in certifications_keywords):
            current_section = 'certifications'
        elif any(keyword in line_lower for keyword in summary_keywords):
            current_section = 'summary'
        
        # Add content to current section
        if current_section and line.strip() and not any(keyword in line_lower for keyword in 
            experience_keywords + skills_keywords + education_keywords + projects_keywords + 
            certifications_keywords + summary_keywords):
            sections[current_section].append(line.strip())
    
    return sections

def calculate_section_scores(resume_sections, jd_sections):
    """Calculate scores for each section"""
    section_scores = {}
    
    for section in ['experience', 'skills', 'education', 'projects', 'certifications', 'summary']:
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
            
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=500)
            tfidf_matrix = vectorizer.fit_transform([resume_text.lower(), jd_text.lower()])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            section_scores[section] = max(0.0, min(100.0, float(similarity) * 100))
        except:
            section_scores[section] = 0.0
    
    return section_scores

def calculate_hard_match(resume_data, jd_data):
    """Calculate hard match score based on keyword matching"""
    try:
        resume_text = resume_data.get('raw_text', '').lower()
        jd_text = jd_data.get('raw_text', '').lower()
        
        if not resume_text or not jd_text:
            return 0.0, []
        
        # Extract keywords from JD
        import re
        # Simple keyword extraction - in a real app, you might use NLP techniques
        jd_words = set(re.findall(r'\b\w+\b', jd_text))
        resume_words = set(re.findall(r'\b\w+\b', resume_text))
        
        # Calculate overlap
        common_words = jd_words.intersection(resume_words)
        missing_words = list(jd_words - resume_words)
        total_jd_words = len(jd_words)
        
        if total_jd_words == 0:
            return 0.0, []
            
        score = (len(common_words) / total_jd_words) * 100
        return min(score, 100.0), missing_words[:20]  # Top 20 missing words
        
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
            ngram_range=(1, 3),
            max_features=2000,
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return max(0.0, min(100.0, float(similarity) * 100))
        
    except Exception as e:
        logger.error(f"Semantic matching failed: {e}")
        return 0.0

def calculate_skill_match(resume_text, jd_text):
    """Calculate skill-specific matching score"""
    try:
        # Extract potential skills (simplified approach)
        import re
        
        # Common skill-related words
        skill_indicators = ['skill', 'experience', 'proficiency', 'expertise', 'knowledge', 
                           'ability', 'competency', 'qualification', 'certification']
        
        # Find skill sections
        resume_lines = resume_text.lower().split('\n')
        jd_lines = jd_text.lower().split('\n')
        
        resume_skills = []
        jd_skills = []
        
        for line in resume_lines:
            if any(indicator in line for indicator in skill_indicators) or len(line.split()) < 10:
                # Extract potential skills (words with capitalization or technical terms)
                skills = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b|\b\w+[.-]\w+\b', 
                                  resume_text)
                resume_skills.extend(skills)
        
        for line in jd_lines:
            if any(indicator in line for indicator in skill_indicators) or len(line.split()) < 10:
                skills = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b|\b\w+[.-]\w+\b', 
                                  jd_text)
                jd_skills.extend(skills)
        
        if not jd_skills:
            return 100.0  # No skills specified
        
        # Calculate overlap
        resume_skills_set = set([s.lower() for s in resume_skills])
        jd_skills_set = set([s.lower() for s in jd_skills])
        
        common_skills = resume_skills_set.intersection(jd_skills_set)
        missing_skills = jd_skills_set - resume_skills_set
        
        score = (len(common_skills) / len(jd_skills_set)) * 100 if jd_skills_set else 0
        return min(score, 100.0), list(missing_skills)
        
    except Exception as e:
        logger.error(f"Skill matching failed: {e}")
        return 0.0, []

def get_detailed_verdict(hard_match_score, semantic_match_score, skill_match_score, missing_keywords=None):
    """Generate detailed verdict based on scores"""
    # Weighted average
    combined_score = (hard_match_score * 0.3 + semantic_match_score * 0.5 + skill_match_score * 0.2)
    
    if combined_score >= 85:
        verdict = "Excellent"
        explanation = "🏆 Outstanding match! Your resume aligns exceptionally well with the job requirements. You're highly recommended to apply."
        recommendation = "Your resume is exceptionally well-aligned with this position. Consider highlighting your most relevant achievements in your cover letter."
    elif combined_score >= 70:
        verdict = "Strong"
        explanation = "✅ Strong match with minor gaps. Your resume shows good alignment with the job requirements."
        recommendation = "Focus on emphasizing your key achievements and consider tailoring your summary to match the job description more closely."
    elif combined_score >= 55:
        verdict = "Good"
        explanation = "🟡 Good match with some gaps. Consider tailoring your resume more closely to the job description."
        recommendation = "Strengthen areas where keywords are missing and emphasize transferable skills. Consider adding more quantifiable achievements."
    elif combined_score >= 40:
        verdict = "Fair"
        explanation = "⚠️ Fair match with significant gaps. Consider gaining more relevant experience or skills."
        recommendation = "Focus on building relevant skills and experiences. Tailor your resume to better match the job requirements with more specific examples."
    else:
        verdict = "Poor"
        explanation = "🔴 Limited match. Significant gaps identified. Consider gaining more relevant experience or skills."
        recommendation = "Consider gaining additional relevant experience or skills. Completely tailor your resume to better match the job requirements with concrete examples."
    
    # Generate keyword gap analysis
    keyword_analysis = ""
    if missing_keywords and len(missing_keywords) > 0:
        top_missing = missing_keywords[:15]  # Top 15 missing keywords
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
        status_info = ["✅ TF-IDF Vectorizer", "✅ Cosine Similarity", "✅ NLP Processing"]
        
        st.markdown(f'''
        <div class="ai-status">
            🟢 <strong>AI Analysis Engine:</strong> Active | {" | ".join(status_info)}
        </div>
        ''', unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"❌ AI Status Error: {e}")
        return False

def create_download_link(data, filename, download_type="json"):
    """Create a download link for analysis results"""
    if download_type == "json":
        json_data = json.dumps(data, indent=2)
        b64 = base64.b64encode(json_data.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="{filename}">📥 Download Analysis Report (JSON)</a>'
    elif download_type == "csv":
        df = pd.DataFrame([data] if isinstance(data, dict) else data)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download Analysis Report (CSV)</a>'
    else:
        href = ""
    return href

def main():
    # Main header
    st.markdown('<h1 class="main-header">🎯 Professional Resume AI Analyzer</h1>', unsafe_allow_html=True)
    
    # Check AI status
    ai_available = check_ai_status()
    
    # Sidebar
    st.sidebar.header("🚀 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📄 Upload & Analyze", 
        "📊 Detailed Analytics",
        "📈 Advanced Visualizations",
        "📋 View Reports",
        "💾 Export & Share"
    ])
    
    # AI settings
    st.sidebar.header("🤖 AI Analysis Settings")
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Quick Scan", "Comprehensive", "Deep Dive"], index=1)
    
    # Analysis focus
    st.sidebar.header("🔍 Analysis Focus")
    focus_areas = st.sidebar.multiselect(
        "Select Focus Areas",
        ["Keyword Matching", "Semantic Analysis", "Skill Matching", "Section Analysis"],
        ["Keyword Matching", "Semantic Analysis", "Skill Matching"]
    )
    
    if page == "📄 Upload & Analyze":
        upload_and_analyze_page(analysis_depth, focus_areas)
    elif page == "📊 Detailed Analytics":
        detailed_analytics_page()
    elif page == "📈 Advanced Visualizations":
        advanced_visualizations_page()
    elif page == "📋 View Reports":
        view_reports_page()
    elif page == "💾 Export & Share":
        export_share_page()

def upload_and_analyze_page(analysis_depth, focus_areas):
    """Upload and analysis page"""
    st.markdown("### 📁 Upload Your Documents for Professional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📁 Job Description")
        jd_file = st.file_uploader("Choose a job description file", type=["pdf", "docx", "txt"], key="jd")
        
        if jd_file is not None:
            st.info(f"📎 File: {jd_file.name} ({jd_file.size} bytes)")
            if st.button("🔄 Process Job Description", type="secondary", key="process_jd"):
                with st.spinner("🔬 Analyzing job description..."):
                    jd_text = extract_text_from_file(jd_file)
                    if jd_text:
                        st.session_state.jd_text = jd_text
                        st.session_state.jd_processed = True
                        st.success("✅ Job Description processed successfully!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", jd_text[:500] + "...", height=150, key="jd_preview")
    
    with col2:
        st.header("📄 Resume")
        resume_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"], key="resume")
        
        if resume_file is not None:
            st.info(f"📎 File: {resume_file.name} ({resume_file.size} bytes)")
            if st.button("🔄 Process Resume", type="secondary", key="process_resume"):
                with st.spinner("🔬 Analyzing resume..."):
                    resume_text = extract_text_from_file(resume_file)
                    if resume_text:
                        st.session_state.resume_text = resume_text
                        st.session_state.resume_processed = True
                        st.success("✅ Resume processed successfully!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", resume_text[:500] + "...", height=150, key="resume_preview")
    
    # Analysis section
    if getattr(st.session_state, 'jd_processed', False) and getattr(st.session_state, 'resume_processed', False):
        st.markdown("---")
        st.header("🤖 Professional AI-Powered Analysis")
        
        st.info(f"📊 Analysis Configuration: {analysis_depth} | Focus Areas: {', '.join(focus_areas)}")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 Start Professional Analysis", type="primary", use_container_width=True):
                perform_professional_analysis(analysis_depth, focus_areas)
    else:
        st.info("📝 Please upload and process both resume and job description to start professional analysis.")

def perform_professional_analysis(analysis_depth, focus_areas):
    """Perform professional analysis"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize
        status_text.text('🔄 Initializing professional analysis engine...')
        progress_bar.progress(5)
        
        # Prepare data
        status_text.text('📊 Preparing data for analysis...')
        progress_bar.progress(15)
        
        resume_data = {"raw_text": st.session_state.resume_text}
        jd_data = {"raw_text": st.session_state.jd_text}
        
        # Initialize section variables
        resume_sections = {}
        jd_sections = {}
        section_scores = {}
        
        # Extract sections for comprehensive analysis
        if "Section Analysis" in focus_areas and analysis_depth in ["Comprehensive", "Deep Dive"]:
            status_text.text('🔍 Extracting document sections...')
            progress_bar.progress(25)
            resume_sections = extract_key_sections(st.session_state.resume_text)
            jd_sections = extract_key_sections(st.session_state.jd_text)
        
        # Calculate scores
        status_text.text('🧮 Performing multi-dimensional analysis...')
        progress_bar.progress(40)
        
        hard_match_score, missing_keywords = 0.0, []
        semantic_match_score = 0.0
        skill_match_score, missing_skills = 0.0, []
        
        if "Keyword Matching" in focus_areas:
            hard_match_score, missing_keywords = calculate_hard_match(resume_data, jd_data)
        
        if "Semantic Analysis" in focus_areas:
            semantic_match_score = calculate_semantic_match(resume_data, jd_data)
        
        if "Skill Matching" in focus_areas:
            skill_match_score, missing_skills = calculate_skill_match(
                st.session_state.resume_text, st.session_state.jd_text)
        
        # Section scores for comprehensive analysis
        if "Section Analysis" in focus_areas and analysis_depth in ["Comprehensive", "Deep Dive"]:
            status_text.text('📑 Analyzing document sections...')
            progress_bar.progress(60)
            section_scores = calculate_section_scores(resume_sections, jd_sections)
        
        progress_bar.progress(75)
        status_text.text('🏆 Generating professional verdict...')
        
        verdict_info = get_detailed_verdict(
            hard_match_score, semantic_match_score, skill_match_score, missing_keywords)
        
        # Add section scores to verdict for comprehensive analysis
        if "Section Analysis" in focus_areas and section_scores:
            verdict_info['section_scores'] = section_scores
        
        # Add skill analysis
        if "Skill Matching" in focus_areas:
            verdict_info['skill_match_score'] = skill_match_score
            verdict_info['missing_skills'] = missing_skills[:10]  # Top 10 missing skills
        
        progress_bar.progress(90)
        status_text.text('💾 Saving professional analysis results...')
        
        # Store results
        analysis_result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hard_match': hard_match_score,
            'semantic_match': semantic_match_score,
            'skill_match': skill_match_score,
            'final_score': verdict_info['combined_score'],
            'verdict': verdict_info['verdict'],
            'analysis_depth': analysis_depth,
            'focus_areas': focus_areas,
            'explanation': verdict_info['explanation'],
            'recommendation': verdict_info['recommendation'],
            'keyword_analysis': verdict_info.get('keyword_analysis', ''),
            'missing_skills': verdict_info.get('missing_skills', []),
            'section_scores': section_scores if section_scores else {},
            'jd_preview': st.session_state.jd_text[:200] + "..." if st.session_state.jd_text else "",
            'resume_preview': st.session_state.resume_text[:200] + "..." if st.session_state.resume_text else ""
        }
        
        st.session_state.analysis_results.append(analysis_result)
        st.session_state.current_analysis = analysis_result
        
        progress_bar.progress(100)
        status_text.text('✅ Professional analysis completed successfully!')
        
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        display_professional_results(analysis_result)
        
    except Exception as e:
        st.error(f"🚨 Analysis error: {e}")
        import traceback
        st.text(traceback.format_exc())
        progress_bar.empty()
        status_text.empty()

def display_professional_results(analysis_result):
    """Display professional analysis results with enhanced visualizations"""
    st.success("✅ Professional analysis completed successfully!")
    
    # Store current analysis in session state
    st.session_state.current_analysis = analysis_result
    
    # Main metrics in professional cards
    st.markdown("### 📊 Professional Match Scores")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 Overall Match", f"{analysis_result['final_score']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🔤 Keyword Match", f"{analysis_result['hard_match']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🧠 Semantic Match", f"{analysis_result['semantic_match']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🛠️ Skill Match", f"{analysis_result['skill_match']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Verdict with professional styling
    st.markdown("### 📝 Professional Assessment")
    verdict_colors = {"Excellent": "🟢", "Strong": "🔵", "Good": "🟡", "Fair": "🟠", "Poor": "🔴"}
    st.info(f"{verdict_colors.get(analysis_result['verdict'], '⚪')} **{analysis_result['verdict']}** - {analysis_result['explanation']}")
    
    # Detailed breakdown in tabs
    st.markdown("### 📋 Detailed Professional Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Recommendations", "Keyword Gap", "Skill Gap", "Full Report"])
    
    with tab1:
        st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
        st.success(analysis_result['recommendation'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if analysis_result.get('keyword_analysis'):
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.warning(analysis_result['keyword_analysis'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No keyword analysis available for this report.")
    
    with tab3:
        if analysis_result.get('missing_skills'):
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.markdown("**Missing Skills to Consider Adding:**")
            for skill in analysis_result['missing_skills']:
                st.markdown(f"- {skill}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No skill gap analysis available for this report.")
    
    with tab4:
        st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
        st.json(analysis_result)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Professional visualizations
    st.markdown("### 📈 Professional Data Visualizations")
    
    # Create professional comparison chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### Match Score Comparison")
    
    scores = [analysis_result['hard_match'], analysis_result['semantic_match'], 
              analysis_result['skill_match'], analysis_result['final_score']]
    labels = ['Keyword Match', 'Semantic Match', 'Skill Match', 'Overall Score']
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
    
    fig_comparison = go.Figure(data=[
        go.Bar(
            x=labels, 
            y=scores, 
            marker_color=colors,
            text=[f"{score:.1f}%" for score in scores],
            textposition='outside',
            textfont_size=14,
            width=0.6
        )
    ])
    
    fig_comparison.update_layout(
        title="Professional Match Score Analysis",
        yaxis_title="Score (%)",
        yaxis_range=[0, 100],
        height=500,
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True, theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Radar chart for comprehensive view
    if analysis_result.get('section_scores'):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Section Score Radar Analysis")
        
        section_scores = analysis_result['section_scores']
        categories = list(section_scores.keys())
        values = list(section_scores.values())
        
        # Close the radar chart
        categories.append(categories[0])
        values.append(values[0])
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Section Scores',
            line_color='#3498db',
            fillcolor='rgba(52, 152, 219, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont_size=10
                ),
                angularaxis=dict(
                    tickfont_size=11
                )
            ),
            showlegend=False,
            title="Professional Section Score Radar",
            height=500,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)

def detailed_analytics_page():
    """Detailed analytics page with comprehensive data analysis"""
    st.header("📊 Professional Detailed Analytics")
    
    if st.session_state.analysis_results:
        df = pd.DataFrame(st.session_state.analysis_results)
        
        # Convert scores to numeric
        score_columns = ['hard_match', 'semantic_match', 'skill_match', 'final_score']
        for col in score_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Professional metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            st.metric("Avg Overall Score", f"{df['final_score'].mean():.1f}%")
        with col3:
            st.metric("Best Score", f"{df['final_score'].max():.1f}%")
        with col4:
            st.metric("Worst Score", f"{df['final_score'].min():.1f}%")
        with col5:
            st.metric("Success Rate", f"{(df['final_score'] >= 70).sum() / len(df) * 100:.1f}%")
        
        # Professional score distribution chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional Score Distribution")
        
        fig_hist = go.Figure()
        
        # Add histograms for different score types
        score_types = ['final_score', 'hard_match', 'semantic_match', 'skill_match']
        colors = ['#9b59b6', '#3498db', '#2ecc71', '#e74c3c']
        names = ['Overall Score', 'Keyword Match', 'Semantic Match', 'Skill Match']
        
        for i, (score_type, color, name) in enumerate(zip(score_types, colors, names)):
            fig_hist.add_trace(go.Histogram(
                x=df[score_type],
                name=name,
                marker_color=color,
                opacity=0.7,
                nbinsx=25
            ))
        
        fig_hist.update_layout(
            title="Professional Score Distribution Analysis",
            xaxis_title="Score (%)",
            yaxis_title="Frequency",
            height=500,
            font=dict(size=12),
            barmode='overlay'
        )
        
        st.plotly_chart(fig_hist, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Trend analysis
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional Score Trend Analysis")
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df_sorted = df.sort_values('timestamp')
        
        fig_trend = go.Figure()
        
        # Add trend lines for different scores
        trend_data = [
            ('final_score', '#9b59b6', 'Overall Score'),
            ('hard_match', '#3498db', 'Keyword Match'),
            ('semantic_match', '#2ecc71', 'Semantic Match'),
            ('skill_match', '#e74c3c', 'Skill Match')
        ]
        
        for score_col, color, name in trend_data:
            fig_trend.add_trace(go.Scatter(
                x=df_sorted['timestamp'],
                y=df_sorted[score_col],
                mode='lines+markers',
                name=name,
                line=dict(color=color, width=3),
                marker=dict(size=8)
            ))
        
        fig_trend.update_layout(
            title="Professional Score Trend Over Time",
            xaxis_title="Date",
            yaxis_title="Score (%)",
            height=500,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Verdict distribution
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional Verdict Distribution")
        
        verdict_counts = df['verdict'].value_counts()
        verdict_colors = ['#27ae60', '#2980b9', '#f39c12', '#e67e22', '#e74c3c']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=verdict_counts.index,
            values=verdict_counts.values,
            marker_colors=verdict_colors,
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig_pie.update_layout(
            title="Professional Verdict Distribution",
            height=500,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed history table
        st.markdown("### 📋 Professional Analysis History")
        display_df = df[['timestamp', 'final_score', 'verdict', 'analysis_depth']].copy()
        display_df['final_score'] = display_df['final_score'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Performance insights
        st.markdown("### 💡 Professional Performance Insights")
        
        avg_score = df['final_score'].mean()
        if avg_score >= 85:
            st.success("🏆 Exceptional performance! Your resumes consistently exceed job description requirements.")
        elif avg_score >= 70:
            st.info("👍 Strong performance with good alignment to job descriptions.")
        elif avg_score >= 55:
            st.warning("⚠️ Moderate performance with room for improvement in resume alignment.")
        else:
            st.error("🔴 Performance needs significant improvement in resume-job alignment.")
            
        # Professional improvement suggestions
        st.markdown("### 📝 Professional Improvement Recommendations")
        st.markdown("""
        1. **🎯 Strategic Alignment**: Align your resume keywords with job descriptions using industry-specific terminology
        2. **📊 Quantifiable Achievements**: Include measurable results and metrics in your experience sections
        3. **🛠️ Skill Optimization**: Highlight technical skills and certifications relevant to the position
        4. **📄 Format Enhancement**: Use a clean, professional format that passes Applicant Tracking Systems (ATS)
        5. **🔍 Customization**: Tailor each resume to specific job requirements rather than using generic templates
        """)
        
    else:
        st.info("📊 No analysis history available. Run your first professional analysis to see insights!")

def advanced_visualizations_page():
    """Advanced visualizations page with professional charts"""
    st.header("📈 Professional Advanced Visualizations")
    
    if st.session_state.analysis_results:
        df = pd.DataFrame(st.session_state.analysis_results)
        
        # Convert scores to numeric
        score_columns = ['hard_match', 'semantic_match', 'skill_match', 'final_score']
        for col in score_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Correlation heatmap
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional Score Correlation Analysis")
        
        correlation_data = df[score_columns].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=correlation_data.values,
            x=correlation_data.columns,
            y=correlation_data.columns,
            colorscale='RdBu',
            text=correlation_data.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig_corr.update_layout(
            title="Professional Score Correlation Matrix",
            height=500,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_corr, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Box plot for score distribution
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional Score Distribution Box Plot")
        
        fig_box = go.Figure()
        
        score_types = ['final_score', 'hard_match', 'semantic_match', 'skill_match']
        colors = ['#9b59b6', '#3498db', '#2ecc71', '#e74c3c']
        names = ['Overall Score', 'Keyword Match', 'Semantic Match', 'Skill Match']
        
        for i, (score_type, color, name) in enumerate(zip(score_types, colors, names)):
            fig_box.add_trace(go.Box(
                y=df[score_type],
                name=name,
                marker_color=color,
                boxmean=True
            ))
        
        fig_box.update_layout(
            title="Professional Score Distribution Analysis",
            yaxis_title="Score (%)",
            height=500,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_box, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3D scatter plot
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional 3D Score Analysis")
        
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=df['hard_match'],
            y=df['semantic_match'],
            z=df['skill_match'],
            mode='markers',
            marker=dict(
                size=8,
                color=df['final_score'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Overall Score")
            ),
            text=df['timestamp'],
            hovertemplate='<b>Timestamp:</b> %{text}<br>' +
                         '<b>Keyword:</b> %{x:.1f}%<br>' +
                         '<b>Semantic:</b> %{y:.1f}%<br>' +
                         '<b>Skill:</b> %{z:.1f}%<br>' +
                         '<b>Overall:</b> %{marker.color:.1f}%'
        )])
        
        fig_3d.update_layout(
            title="Professional 3D Score Analysis",
            scene=dict(
                xaxis_title='Keyword Match (%)',
                yaxis_title='Semantic Match (%)',
                zaxis_title='Skill Match (%)'
            ),
            height=600,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_3d, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Focus area analysis
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Professional Focus Area Analysis")
        
        # Count focus areas
        all_focus_areas = []
        for focus_list in df['focus_areas']:
            if isinstance(focus_list, list):
                all_focus_areas.extend(focus_list)
        
        if all_focus_areas:
            focus_counts = pd.Series(all_focus_areas).value_counts()
            
            fig_focus = go.Figure(data=[go.Bar(
                x=focus_counts.index,
                y=focus_counts.values,
                marker_color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
                text=focus_counts.values,
                textposition='outside'
            )])
            
            fig_focus.update_layout(
                title="Professional Focus Area Frequency",
                xaxis_title="Focus Area",
                yaxis_title="Frequency",
                height=400,
                font=dict(size=12)
            )
            
            st.plotly_chart(fig_focus, use_container_width=True, theme="streamlit")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("📈 No analysis data available. Run your first professional analysis to see advanced visualizations!")

def view_reports_page():
    """View detailed reports page"""
    st.header("📋 Professional Detailed Analysis Reports")
    
    if st.session_state.analysis_results:
        # Create a selectbox to choose which analysis to view
        report_options = [f"Analysis {i+1}: {result['verdict']} ({result['final_score']:.1f}%) - {result['timestamp']}" 
                         for i, result in enumerate(st.session_state.analysis_results)]
        
        selected_report = st.selectbox("Select a professional report to view:", report_options)
        selected_index = report_options.index(selected_report)
        selected_result = st.session_state.analysis_results[selected_index]
        
        # Display the selected report
        st.markdown("### 📊 Selected Professional Analysis Report")
        
        # Main metrics in professional cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🎯 Overall Match", f"{selected_result['final_score']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🔤 Keyword Match", f"{selected_result['hard_match']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🧠 Semantic Match", f"{selected_result['semantic_match']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🛠️ Skill Match", f"{selected_result['skill_match']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Verdict
        verdict_colors = {"Excellent": "🟢", "Strong": "🔵", "Good": "🟡", "Fair": "🟠", "Poor": "🔴"}
        st.info(f"{verdict_colors.get(selected_result['verdict'], '⚪')} **{selected_result['verdict']}** - {selected_result['explanation']}")
        
        # Detailed information in professional tabs
        st.markdown("### 📋 Professional Report Details")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summary", "Recommendations", "Gaps Analysis", "Section Scores", "Raw Data"])
        
        with tab1:
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.markdown("#### Executive Summary")
            st.info(selected_result['explanation'])
            st.markdown("#### Analysis Configuration")
            st.markdown(f"- **Depth**: {selected_result['analysis_depth']}")
            st.markdown(f"- **Focus Areas**: {', '.join(selected_result['focus_areas'])}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.markdown("#### Professional Recommendations")
            st.success(selected_result['recommendation'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.markdown("#### Gap Analysis")
            if selected_result.get('keyword_analysis'):
                st.markdown("##### Missing Keywords")
                st.warning(selected_result['keyword_analysis'])
            if selected_result.get('missing_skills'):
                st.markdown("##### Missing Skills")
                for skill in selected_result['missing_skills']:
                    st.markdown(f"- {skill}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.markdown("#### Section Score Analysis")
            if selected_result.get('section_scores'):
                section_data = selected_result['section_scores']
                section_df = pd.DataFrame({
                    'Section': list(section_data.keys()),
                    'Score': [f"{score:.1f}%" for score in section_data.values()]
                })
                st.table(section_df)
            else:
                st.info("No section analysis available for this report.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab5:
            st.markdown('<div class="analysis-report">', unsafe_allow_html=True)
            st.markdown("#### Raw Analysis Data")
            st.json(selected_result)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Professional visualization
        st.markdown("### 📈 Professional Visual Analysis")
        
        # Create professional comparison chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Match Score Comparison")
        
        scores = [selected_result['hard_match'], selected_result['semantic_match'], 
                  selected_result['skill_match'], selected_result['final_score']]
        labels = ['Keyword Match', 'Semantic Match', 'Skill Match', 'Overall Score']
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
        
        fig_comparison = go.Figure(data=[
            go.Bar(
                x=labels, 
                y=scores, 
                marker_color=colors,
                text=[f"{score:.1f}%" for score in scores],
                textposition='outside',
                textfont_size=14,
                width=0.6
            )
        ])
        
        fig_comparison.update_layout(
            title="Professional Match Score Analysis",
            yaxis_title="Score (%)",
            yaxis_range=[0, 100],
            height=500,
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True, theme="streamlit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Radar chart for section scores
        if selected_result.get('section_scores'):
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Section Score Radar Analysis")
            
            section_scores = selected_result['section_scores']
            categories = list(section_scores.keys())
            values = list(section_scores.values())
            
            # Close the radar chart
            categories.append(categories[0])
            values.append(values[0])
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Section Scores',
                line_color='#3498db',
                fillcolor='rgba(52, 152, 219, 0.3)'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont_size=10
                    ),
                    angularaxis=dict(
                        tickfont_size=11
                    )
                ),
                showlegend=False,
                title="Professional Section Score Radar",
                height=500,
                font=dict(size=12)
            )
            
            st.plotly_chart(fig_radar, use_container_width=True, theme="streamlit")
            st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("📋 No professional analysis reports available. Run your first analysis to generate reports!")

def export_share_page():
    """Export and share page"""
    st.header("💾 Professional Export & Share Options")
    
    if st.session_state.analysis_results:
        st.markdown("### 📥 Professional Export Options")
        
        # Export current analysis
        if st.session_state.current_analysis:
            st.markdown("#### 📄 Export Current Analysis")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_json = json.dumps(st.session_state.current_analysis, indent=2)
                st.download_button(
                    label="📥 Download JSON Report",
                    data=current_json,
                    file_name=f"professional_resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                df_current = pd.DataFrame([st.session_state.current_analysis])
                csv_current = df_current.to_csv(index=False)
                st.download_button(
                    label="📊 Download CSV Report",
                    data=csv_current,
                    file_name=f"professional_resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                # Create a simple text report
                report_text = f"""Professional Resume Analysis Report
==============================
Generated: {st.session_state.current_analysis['timestamp']}
Overall Match Score: {st.session_state.current_analysis['final_score']:.1f}%
Verdict: {st.session_state.current_analysis['verdict']}

Key Findings:
{st.session_state.current_analysis['explanation']}

Recommendations:
{st.session_state.current_analysis['recommendation']}
"""
                st.download_button(
                    label="📄 Download Text Report",
                    data=report_text,
                    file_name=f"professional_resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Export all analyses
        st.markdown("#### 📦 Export All Professional Analyses")
        col1, col2 = st.columns(2)
        
        with col1:
            all_json = json.dumps(st.session_state.analysis_results, indent=2)
            st.download_button(
                label="📥 Download All JSON Reports",
                data=all_json,
                file_name=f"all_professional_resume_analyses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            df_all = pd.DataFrame(st.session_state.analysis_results)
            csv_all = df_all.to_csv(index=False)
            st.download_button(
                label="📊 Download All CSV Reports",
                data=csv_all,
                file_name=f"all_professional_resume_analyses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Share options
        st.markdown("### 🌐 Professional Sharing Options")
        
        st.markdown("#### 🔗 Share Analysis Link")
        st.info("To share your analysis, you can:")
        st.markdown("""
        1. **Download and Email**: Download the report and email it to colleagues
        2. **Cloud Storage**: Upload to Google Drive, Dropbox, or OneDrive and share the link
        3. **Print to PDF**: Use your browser's print function to save as PDF
        """)
        
        # Display current analysis if available
        if st.session_state.current_analysis:
            st.markdown("### 📋 Current Analysis Preview")
            with st.expander("🔍 View Current Analysis Details"):
                st.json(st.session_state.current_analysis)
        
        # Display all analyses summary
        st.markdown("### 📋 All Analyses Summary")
        with st.expander("📊 View All Analyses Summary"):
            df_summary = pd.DataFrame(st.session_state.analysis_results)
            display_summary = df_summary[['timestamp', 'final_score', 'verdict', 'analysis_depth']].copy()
            display_summary['final_score'] = display_summary['final_score'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_summary, use_container_width=True)
            
    else:
        st.info("💾 No professional analysis data available to export. Run a professional analysis first!")

if __name__ == "__main__":
    main()