import streamlit as st
import requests
import tempfile
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from io import BytesIO
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Resume Relevance Analyzer",
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
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Global variables to store uploaded file data
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        from src.utils.text_extraction import extract_text
        
        # Save uploaded file temporarily
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

def main():
    # Main header with styling
    st.markdown('<h1 class="main-header">📄 Resume Relevance Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("🚀 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📋 Upload & Analyze", 
        "📈 Advanced Analytics",
        "📊 View Results", 
        "⚙️ Settings"
    ])
    
    # Advanced settings in sidebar
    st.sidebar.header("⚙️ Analysis Settings")
    use_transformers = st.sidebar.checkbox("Use Advanced AI Models (Transformers)", value=True, 
                                         help="Enable Hugging Face transformers for better semantic analysis")
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"], index=1)
    
    if page == "📋 Upload & Analyze":
        upload_and_analyze_page(use_transformers, analysis_depth)
    elif page == "📈 Advanced Analytics":
        advanced_analytics_page()
    elif page == "📊 View Results":
        view_results_page()
    elif page == "⚙️ Settings":
        settings_page()

def upload_and_analyze_page(use_transformers, analysis_depth):
    """Enhanced upload and analysis page with advanced features"""
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
                        st.success("✅ Job Description processed successfully!")
                        
                        # Show preview with word count
                        word_count = len(jd_text.split())
                        st.markdown(f"**Word Count:** {word_count}")
                        
                        with st.expander("🔍 Preview Job Description"):
                            st.text_area("Content Preview", jd_text[:1000] + "..." if len(jd_text) > 1000 else jd_text, height=200)
    
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
                        st.success("✅ Resume processed successfully!")
                        
                        # Show preview with word count
                        word_count = len(resume_text.split())
                        st.markdown(f"**Word Count:** {word_count}")
                        
                        with st.expander("🔍 Preview Resume"):
                            st.text_area("Content Preview", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200)
    
    # Analysis section
    if getattr(st.session_state, 'jd_processed', False) and getattr(st.session_state, 'resume_processed', False):
        st.markdown("---")
        st.header("🧮 AI-Powered Analysis")
        
        analysis_col1, analysis_col2, analysis_col3 = st.columns([2, 1, 2])
        
        with analysis_col2:
            if st.button("🚀 Start Advanced Analysis", type="primary"):
                perform_advanced_analysis(use_transformers, analysis_depth)
    else:
        st.info("📝 Please upload and process both a job description and resume to start analysis.")

def perform_advanced_analysis(use_transformers, analysis_depth):
    """Perform advanced analysis with progress tracking"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Initialize analysis
        status_text.text('🔄 Initializing analysis...')
        time.sleep(0.5)
        progress_bar.progress(20)
        
        # Import modules
        from src.scoring.hard_match import calculate_hard_match
        from src.scoring.semantic_match import calculate_semantic_match, calculate_detailed_semantic_match
        from src.scoring.verdict import get_verdict, get_detailed_verdict
        from src.storage.database import store_evaluation_results
        
        # Step 2: Prepare data
        status_text.text('📊 Preparing data...')
        progress_bar.progress(40)
        
        resume_data = {"raw_text": st.session_state.resume_text}
        jd_data = {"raw_text": st.session_state.jd_text}
        
        # Step 3: Calculate scores
        status_text.text('🧮 Calculating relevance scores...')
        progress_bar.progress(60)
        
        # Hard match score
        hard_match_score = calculate_hard_match(resume_data, jd_data)
        
        # Semantic match score with transformer option
        if analysis_depth == "Deep":
            semantic_results = calculate_detailed_semantic_match(resume_data, jd_data)
            semantic_match_score = semantic_results.get('weighted_score', 0)
        else:
            semantic_match_score = calculate_semantic_match(resume_data, jd_data, use_transformers)
        
        progress_bar.progress(80)
        status_text.text('🏆 Generating final verdict...')
        
        # Get detailed verdict
        verdict_info = get_detailed_verdict(hard_match_score, semantic_match_score)
        
        progress_bar.progress(100)
        status_text.text('✅ Analysis complete!')
        
        # Display results
        display_analysis_results(hard_match_score, semantic_match_score, verdict_info, analysis_depth)
        
        # Store results
        evaluation_result = {
            "hard_match_score": hard_match_score,
            "semantic_match_score": semantic_match_score,
            "final_score": verdict_info["combined_score"],
            "verdict": verdict_info["verdict"]
        }
        store_evaluation_results(evaluation_result)
        
        # Clear progress indicators
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"🚨 Error during analysis: {e}")
        progress_bar.empty()
        status_text.empty()

def display_analysis_results(hard_match_score, semantic_match_score, verdict_info, analysis_depth):
    """Display comprehensive analysis results with visualizations"""
    st.success("✅ Analysis completed successfully!")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏅 Hard Match Score",
            value=f"{hard_match_score:.1f}%",
            help="Exact skill and keyword matching"
        )
    
    with col2:
        st.metric(
            label="🧮 Semantic Match Score",
            value=f"{semantic_match_score:.1f}%",
            help="AI-powered contextual similarity"
        )
    
    with col3:
        st.metric(
            label="🎥 Final Score",
            value=f"{verdict_info['combined_score']:.1f}%",
            help="Weighted combination of all factors"
        )
    
    with col4:
        verdict_emoji = {
            "High": "🟢",
            "Medium": "🟡", 
            "Low": "🔴"
        }
        st.metric(
            label="🏆 Verdict",
            value=f"{verdict_emoji.get(verdict_info['verdict'], '🔵')} {verdict_info['verdict']}",
            help="Overall recommendation"
        )
    
    # Detailed explanation
    st.markdown(f"### 📝 Analysis Summary")
    st.info(verdict_info['explanation'])
    
    # Visualization section
    st.markdown("### 📈 Score Breakdown")
    
    # Create score visualization
    scores_data = {
        'Metric': ['Hard Match', 'Semantic Match', 'Final Score'],
        'Score': [hard_match_score, semantic_match_score, verdict_info['combined_score']],
        'Color': ['#FF6B6B', '#4ECDC4', '#45B7D1']
    }
    
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(
                x=scores_data['Metric'],
                y=scores_data['Score'],
                marker_color=scores_data['Color'],
                text=[f"{score:.1f}%" for score in scores_data['Score']],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Resume Relevance Analysis",
            yaxis_title="Score (%)",
            yaxis_range=[0, 100],
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except ImportError:
        # Fallback to simple bar chart if plotly not available
        chart_data = pd.DataFrame({
            'Metric': scores_data['Metric'],
            'Score': scores_data['Score']
        })
        st.bar_chart(chart_data.set_index('Metric'))
    
    # Save results to session for history
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    st.session_state.analysis_history.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'hard_match': hard_match_score,
        'semantic_match': semantic_match_score,
        'final_score': verdict_info['combined_score'],
        'verdict': verdict_info['verdict'],
        'analysis_depth': analysis_depth
    })

def advanced_analytics_page():
    """Advanced analytics and insights page"""
    st.header("📈 Advanced Analytics & Insights")
    
    if 'analysis_history' in st.session_state and st.session_state.analysis_history:
        df = pd.DataFrame(st.session_state.analysis_history)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_score = df['final_score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with col2:
            best_score = df['final_score'].max()
            st.metric("Best Score", f"{best_score:.1f}%")
        
        with col3:
            total_analyses = len(df)
            st.metric("Total Analyses", total_analyses)
        
        # Trend analysis
        if len(df) > 1:
            st.subheader("📈 Score Trends")
            
            try:
                import plotly.express as px
                
                fig = px.line(df, x='timestamp', y=['hard_match', 'semantic_match', 'final_score'],
                             title="Score Trends Over Time")
                st.plotly_chart(fig, use_container_width=True)
                
            except ImportError:
                st.line_chart(df.set_index('timestamp')[['hard_match', 'semantic_match', 'final_score']])
        
        # Data table
        st.subheader("📊 Analysis History")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("📊 No analysis history available. Please perform some analyses first.")

def view_results_page():
    """Enhanced results viewing page"""
    st.header("📊 Evaluation Results Database")
    
    try:
        from src.storage.database import SessionLocal, Evaluation
        db = SessionLocal()
        evaluations = db.query(Evaluation).order_by(Evaluation.id.desc()).limit(20).all()
        db.close()
        
        if evaluations:
            # Summary stats
            scores = [int(eval.relevance_score) for eval in evaluations]  # Ensure scores are integers
            avg_score = sum(scores) / len(scores)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Evaluations", len(evaluations))
            with col2:
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col3:
                high_quality = len([s for s in scores if s >= 80])
                st.metric("High Quality Matches", f"{high_quality}/{len(scores)}")
            
            # Individual results
            for i, eval in enumerate(evaluations):
                with st.expander(f"Evaluation {eval.id} - {eval.verdict} ({eval.relevance_score}%)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {eval.id}")
                        st.write(f"**Score:** {eval.relevance_score}%")
                        st.write(f"**Verdict:** {eval.verdict}")
                    with col2:
                        if eval.missing_elements and str(eval.missing_elements).strip():  # Safe string check
                            st.write(f"**Notes:** {eval.missing_elements}")
                        
                        # Action buttons
                        if st.button(f"View Details", key=f"view_{eval.id}"):
                            st.json({
                                "id": eval.id,
                                "score": eval.relevance_score,
                                "verdict": eval.verdict
                            })
        else:
            st.info("📊 No evaluation results found in database.")
            
    except Exception as e:
        st.error(f"🚨 Error loading results: {e}")

def settings_page():
    """Application settings and configuration page"""
    st.header("⚙️ Application Settings")
    
    # Model selection
    st.subheader("🤖 AI Model Configuration")
    
    model_option = st.selectbox(
        "Choose Embedding Model",
        [
            "all-MiniLM-L6-v2 (Fast, Lightweight)",
            "all-mpnet-base-v2 (High Quality)",
            "paraphrase-MiniLM-L6-v2 (Balanced)"
        ]
    )
    
    # Analysis preferences
    st.subheader("📈 Analysis Preferences")
    
    weight_hard = st.slider("Hard Match Weight", 0.0, 1.0, 0.6, 0.1)
    weight_semantic = 1.0 - weight_hard
    st.write(f"Semantic Match Weight: {weight_semantic:.1f}")
    
    # Performance settings
    st.subheader("⚡ Performance Settings")
    
    cache_enabled = st.checkbox("Enable Result Caching", value=True)
    batch_processing = st.checkbox("Enable Batch Processing", value=False)
    
    # Export settings
    st.subheader("💾 Export & Import")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Export Results"):
            if 'analysis_history' in st.session_state:
                results_json = json.dumps(st.session_state.analysis_history, indent=2)
                st.download_button(
                    label="Download Results JSON",
                    data=results_json,
                    file_name=f"resume_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No results to export")
    
    with col2:
        uploaded_results = st.file_uploader("Import Results", type=["json"])
        if uploaded_results is not None:
            try:
                imported_data = json.loads(uploaded_results.read())
                if st.button("Import Data"):
                    if 'analysis_history' not in st.session_state:
                        st.session_state.analysis_history = []
                    st.session_state.analysis_history.extend(imported_data)
                    st.success("Data imported successfully!")
            except Exception as e:
                st.error(f"Error importing data: {e}")

if __name__ == "__main__":
    main()