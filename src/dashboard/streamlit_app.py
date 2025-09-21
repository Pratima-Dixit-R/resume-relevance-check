import streamlit as st
import tempfile
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="🤖 Resume AI Analyzer with Ollama",
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
    .ollama-status {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Global variables
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        from src.utils.text_extraction import extract_text
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.flush()
            
            try:
                text = extract_text(tmp_file.name)
                return text
            finally:
                os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

def check_ollama_status():
    """Check if Ollama is running"""
    try:
        from src.scoring.semantic_match import get_available_ollama_models
        models = get_available_ollama_models()
        if models:
            st.markdown(f'''
            <div class="ollama-status">
                🟢 <strong>Ollama Status:</strong> Connected | 🤖 {len(models)} models available
            </div>
            ''', unsafe_allow_html=True)
            return True
        else:
            st.warning("⚠️ Ollama is not running or no models available.")
            return False
    except Exception as e:
        st.error(f"❌ Ollama Error: {e}")
        return False

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 Resume AI Analyzer with Ollama</h1>', unsafe_allow_html=True)
    
    # Check Ollama status
    ollama_available = check_ollama_status()
    
    # Sidebar
    st.sidebar.header("🚀 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📋 Upload & Analyze", 
        "📊 Analytics",
        "📋 View Results"
    ])
    
    # Ollama settings
    st.sidebar.header("🤖 AI Settings")
    use_ollama = st.sidebar.checkbox("🚀 Use Ollama AI", value=ollama_available)
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"], index=1)
    
    if page == "📋 Upload & Analyze":
        upload_and_analyze_page(use_ollama, analysis_depth)
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "📋 View Results":
        view_results_page()

def upload_and_analyze_page(use_ollama, analysis_depth):
    """Upload and analysis page with Ollama integration"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📁 Job Description")
        jd_file = st.file_uploader("Choose a job description file", type=["pdf", "docx"], key="jd")
        
        if jd_file is not None:
            st.info(f"File: {jd_file.name} ({jd_file.size} bytes)")
            if st.button("🔄 Process Job Description", type="secondary"):
                with st.spinner("Processing job description..."):
                    jd_text = extract_text_from_file(jd_file)
                    if jd_text:
                        st.session_state.jd_text = jd_text
                        st.session_state.jd_processed = True
                        st.success("✅ Job Description processed!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", jd_text[:500] + "...", height=150)
    
    with col2:
        st.header("📄 Resume")
        resume_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"], key="resume")
        
        if resume_file is not None:
            st.info(f"File: {resume_file.name} ({resume_file.size} bytes)")
            if st.button("🔄 Process Resume", type="secondary"):
                with st.spinner("Processing resume..."):
                    resume_text = extract_text_from_file(resume_file)
                    if resume_text:
                        st.session_state.resume_text = resume_text
                        st.session_state.resume_processed = True
                        st.success("✅ Resume processed!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", resume_text[:500] + "...", height=150)
    
    # Analysis section
    if getattr(st.session_state, 'jd_processed', False) and getattr(st.session_state, 'resume_processed', False):
        st.markdown("---")
        st.header("🤖 AI-Powered Analysis")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 Start Ollama Analysis", type="primary"):
                perform_analysis(use_ollama, analysis_depth)
    else:
        st.info("📝 Please upload and process both files to start analysis.")

def perform_analysis(use_ollama, analysis_depth):
    """Perform analysis with Ollama"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize
        status_text.text('🔄 Initializing analysis...')
        progress_bar.progress(20)
        
        # Import modules
        from src.scoring.hard_match import calculate_hard_match
        from src.scoring.semantic_match import calculate_semantic_match, calculate_detailed_semantic_match
        from src.scoring.verdict import get_detailed_verdict
        
        # Prepare data
        status_text.text('📊 Preparing data...')
        progress_bar.progress(40)
        
        resume_data = {"raw_text": st.session_state.resume_text}
        jd_data = {"raw_text": st.session_state.jd_text}
        
        # Calculate scores
        status_text.text('🧮 Calculating scores...')
        progress_bar.progress(60)
        
        hard_match_score = calculate_hard_match(resume_data, jd_data)
        
        if analysis_depth == "Deep":
            semantic_results = calculate_detailed_semantic_match(resume_data, jd_data)
            semantic_match_score = semantic_results.get('weighted_score', 0)
            detailed_analysis = semantic_results.get('detailed_analysis', '')
        else:
            semantic_match_score = calculate_semantic_match(resume_data, jd_data, use_ollama)
            detailed_analysis = "Standard analysis completed"
        
        progress_bar.progress(80)
        status_text.text('🏆 Generating verdict...')
        
        verdict_info = get_detailed_verdict(hard_match_score, semantic_match_score)
        
        progress_bar.progress(100)
        status_text.text('✅ Analysis complete!')
        
        # Display results
        display_results(hard_match_score, semantic_match_score, verdict_info, detailed_analysis)
        
        # Store in history
        st.session_state.analysis_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hard_match': hard_match_score,
            'semantic_match': semantic_match_score,
            'final_score': verdict_info['combined_score'],
            'verdict': verdict_info['verdict'],
            'analysis_depth': analysis_depth
        })
        
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"🚨 Analysis error: {e}")
        progress_bar.empty()
        status_text.empty()

def display_results(hard_match_score, semantic_match_score, verdict_info, detailed_analysis):
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
    
    if detailed_analysis and detailed_analysis != "Standard analysis completed":
        st.markdown("### 🤖 Ollama AI Analysis")
        st.write(detailed_analysis)
    
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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            st.metric("Average Score", f"{df['final_score'].mean():.1f}%")
        with col3:
            st.metric("Best Score", f"{df['final_score'].max():.1f}%")
        
        st.subheader("📈 Analysis History")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("📊 No analysis history available.")

def view_results_page():
    """View results page"""
    st.header("📋 Recent Results")
    
    if st.session_state.analysis_history:
        for i, result in enumerate(reversed(st.session_state.analysis_history)):
            with st.expander(f"Analysis {len(st.session_state.analysis_history)-i}: {result['verdict']} ({result['final_score']:.1f}%)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Timestamp:** {result['timestamp']}")
                    st.write(f"**Hard Match:** {result['hard_match']:.1f}%")
                with col2:
                    st.write(f"**Semantic Match:** {result['semantic_match']:.1f}%")
                    st.write(f"**Analysis Depth:** {result['analysis_depth']}")
    else:
        st.info("📋 No results available.")

if __name__ == "__main__":
    main()