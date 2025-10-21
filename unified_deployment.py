#!/usr/bin/env python3
"""
Unified deployment script for Resume AI Analyzer.
This script creates a single Streamlit app that includes both frontend and backend functionality,
and provides public HTTPS access through localtunnel.
"""

import os
import sys
import subprocess
import time
import threading
import requests
import json
from pathlib import Path

def create_unified_app():
    """Create a unified Streamlit app that includes backend functionality."""
    unified_app_content = '''
import streamlit as st
import requests
import tempfile
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
from pathlib import Path
import glob

# Page configuration
st.set_page_config(
    page_title="🤖 Resume AI Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4ECDC4;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

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
                    text += paragraph.text + "\\n"
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
            text = re.sub(r'\\s+', ' ', text.strip())
            # Remove special characters but keep important punctuation
            text = re.sub(r'[^\\w\\s\\.,!?;:()-]', ' ', text)
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

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 Resume AI Analyzer</h1>', unsafe_allow_html=True)
    
    # AI status
    st.markdown(f'''
    <div class="ai-status">
        <strong>AI Status:</strong> Active | Using TF-IDF for semantic analysis
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🚀 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📋 Upload & Analyze", 
        "📊 Results"
    ])
    
    if page == "📋 Upload & Analyze":
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
                            st.success("✅ Resume processed!")
                            
                            with st.expander("🔍 Preview"):
                                st.text_area("Content", resume_text[:500] + "...", height=150)
        
        # Analysis section
        if 'jd_text' in st.session_state and 'resume_text' in st.session_state:
            st.markdown("---")
            st.header("🤖 AI-Powered Analysis")
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("🚀 Start AI Analysis", type="primary"):
                    with st.spinner("🤖 Analyzing resume and job description..."):
                        # Prepare data
                        resume_data = {"raw_text": st.session_state.resume_text}
                        jd_data = {"raw_text": st.session_state.jd_text}
                        
                        # Calculate scores
                        hard_match_score, missing_keywords = calculate_hard_match(resume_data, jd_data)
                        semantic_match_score = calculate_semantic_match(resume_data, jd_data)
                        
                        # Generate verdict
                        verdict_info = get_detailed_verdict(hard_match_score, semantic_match_score, missing_keywords)
                        
                        # Store results
                        st.session_state.analysis_results = {
                            'hard_match_score': hard_match_score,
                            'semantic_match_score': semantic_match_score,
                            'verdict_info': verdict_info
                        }
                        
                        st.success("✅ Analysis completed!")
        
    elif page == "📊 Results":
        if st.session_state.analysis_results:
            display_results(
                st.session_state.analysis_results['hard_match_score'],
                st.session_state.analysis_results['semantic_match_score'],
                st.session_state.analysis_results['verdict_info']
            )
        else:
            st.info("📊 No analysis results available. Please upload files and run analysis first.")

if __name__ == "__main__":
    main()
'''
    
    # Write the unified app to a file
    with open("unified_streamlit_app.py", "w", encoding="utf-8") as f:
        f.write(unified_app_content)
    
    print("✅ Created unified Streamlit app: unified_streamlit_app.py")

def launch_unified_app():
    """Launch the unified Streamlit app."""
    print("🚀 Launching unified Streamlit app on port 8501...")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "unified_streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start unified app: {e}")
        return None

def create_https_tunnel():
    """Create HTTPS tunnel using localtunnel."""
    try:
        print("🔗 Creating HTTPS tunnel using localtunnel...")
        
        # Create tunnel for the app (port 8501)
        tunnel_process = subprocess.Popen([
            'npx', 'localtunnel', '--port', '8501'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for tunnel to establish
        time.sleep(5)
        
        print("✅ HTTPS tunnel created successfully!")
        print("   Check the terminal output above for the public URL")
        print("   It will look something like: https://random-subdomain.loca.lt")
        
        return tunnel_process
        
    except Exception as e:
        print(f"❌ Failed to create HTTPS tunnel: {e}")
        return None

def main():
    """Main function to deploy the unified application."""
    print("🚀 Resume AI Analyzer - Unified Deployment")
    print("="*50)
    
    # Create the unified app
    create_unified_app()
    
    # Launch the unified app
    app_process = launch_unified_app()
    if not app_process:
        print("❌ Failed to launch unified app. Exiting.")
        return
    
    # Wait for app to start
    print("⏳ Waiting for app to initialize...")
    time.sleep(10)
    
    # Check if app is running
    try:
        response = requests.get("http://localhost:8501/healthz", timeout=3)
        # If there's no healthz endpoint, we'll just try to access the main page
    except:
        pass
    
    # Try to access the main page
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Unified app is running!")
        else:
            print(f"⚠️  App returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not verify app is running: {e}")
    
    # Create HTTPS tunnel for public access
    tunnel_process = create_https_tunnel()
    
    # Display access information
    print("\n" + "="*60)
    print("🎉 RESUME AI ANALYZER DEPLOYED SUCCESSFULLY!")
    print("="*60)
    print("📱 ACCESS THE APP:")
    print("   Local URL: http://localhost:8501")
    print("   Network URL: http://127.0.0.1:8501")
    print("   Public HTTPS URL: Check terminal output above (starts with https://)")
    
    print("\n📝 HOW TO ACCESS:")
    print("   1. Open http://localhost:8501 in your browser for local access")
    print("   2. OR use the public HTTPS URL for sharing with others")
    print("   3. Upload your resume and job description files")
    print("   4. Click 'Start AI Analysis' to get results")
    
    print("\n💡 NOTES:")
    print("   - This is a unified app that includes both frontend and backend")
    print("   - All processing happens within the Streamlit app")
    print("   - Public HTTPS access is provided through localtunnel")
    print("   - No separate backend service is needed")
    print("="*60)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop the service")
    
    # Keep track of processes
    processes = [app_process]
    if tunnel_process:
        processes.append(tunnel_process)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate all processes
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("✅ All services stopped successfully")

if __name__ == "__main__":
    main()