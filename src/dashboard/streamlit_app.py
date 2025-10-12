import streamlit as st
import tempfile
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
from pathlib import Path
import glob
import requests
import json

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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def register_user(username, email, password):
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Registration failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error during registration: {str(e)}")
        return None

def login_user(username, password):
    """Login user and get token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Login failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error during login: {str(e)}")
        return None

def get_user_info(token):
    """Get user information"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/auth/users/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get user info: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting user info: {str(e)}")
        return None

def get_user_evaluations(token):
    """Get user's evaluation results"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/evaluations/", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get evaluations: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting evaluations: {str(e)}")
        return []

def upload_resume(token, file_bytes, filename):
    """Upload resume file"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        files = {"file": (filename, file_bytes, "application/octet-stream")}
        response = requests.post(f"{API_BASE_URL}/upload_resume/", files=files, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload resume: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error uploading resume: {str(e)}")
        return None

def upload_jd(token, file_bytes, filename):
    """Upload job description file"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        files = {"file": (filename, file_bytes, "application/octet-stream")}
        response = requests.post(f"{API_BASE_URL}/upload_jd/", files=files, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload job description: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error uploading job description: {str(e)}")
        return None

def evaluate_resume(token, resume_text, jd_text):
    """Evaluate resume against job description"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"resume_text": resume_text, "jd_text": jd_text}
        response = requests.post(f"{API_BASE_URL}/evaluate/", data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to evaluate resume: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error evaluating resume: {str(e)}")
        return None

def get_sample_data_paths():
    """Get paths to sample resume and job description files."""
    base_path = Path(__file__).parent.parent.parent
    
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

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        # Add project root to Python path
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
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

def load_sample_file(file_path):
    """Load a sample file and return its content."""
    try:
        # Add project root to Python path
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
            
        if file_path.endswith('.pdf'):
            from src.utils.text_extraction import extract_text
            return extract_text(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file {file_path}: {e}")
        return None

def check_ai_status():
    """Check AI backend status"""
    try:
        # Add project root to Python path
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
            
        from src.scoring.semantic_match import HUGGINGFACE_LLM_AVAILABLE, SENTENCE_TRANSFORMERS_AVAILABLE, SPACY_AVAILABLE
        status_info = []
        
        if HUGGINGFACE_LLM_AVAILABLE:
            status_info.append("✅ Hugging Face LLM available")
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            status_info.append("✅ Sentence Transformers available")
        if SPACY_AVAILABLE:
            status_info.append("✅ spaCy available")
            
        if status_info:
            st.markdown(f'''
            <div class="ai-status">
                🟢 <strong>AI Status:</strong> Connected | {" | ".join(status_info)}
            </div>
            ''', unsafe_allow_html=True)
            return True
        else:
            st.warning("⚠️ No AI backends available.")
            return False
    except Exception as e:
        st.error(f"❌ AI Status Error: {e}")
        return False

def auth_page():
    """Authentication page"""
    st.markdown("## 🔐 User Authentication")
    
    auth_option = st.radio("Choose an option:", ["Login", "Register"])
    
    with st.form("auth_form"):
        username = st.text_input("Username")
        email = ""  # Initialize email variable
        if auth_option == "Register":
            email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button(auth_option)
        
        if submitted:
            if auth_option == "Register":
                if username and email and password:
                    user = register_user(username, email, password)
                    if user:
                        st.success("Registration successful! Please login.")
                        st.rerun()
                else:
                    st.error("Please fill in all fields.")
            else:  # Login
                if username and password:
                    token_response = login_user(username, password)
                    if token_response:
                        st.session_state.token = token_response["access_token"]
                        user_info = get_user_info(st.session_state.token)
                        if user_info:
                            st.session_state.user = user_info
                            st.success("Login successful!")
                            st.rerun()
                else:
                    st.error("Please fill in all fields.")

def logout():
    """Logout user"""
    st.session_state.token = None
    st.session_state.user = None
    st.success("You have been logged out.")
    st.rerun()

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 Resume AI Analyzer</h1>', unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.token:
        # Show authentication page
        auth_page()
        # Check AI status
        check_ai_status()
        return
    
    # User is logged in - show main app
    st.sidebar.markdown(f"## 👤 Welcome, {st.session_state.user['username']}!")
    if st.sidebar.button("Logout"):
        logout()
    
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
    use_huggingface = st.sidebar.checkbox("🚀 Use Hugging Face AI", value=ai_available)
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"], index=1)
    
    if page == "📋 Upload & Analyze":
        upload_and_analyze_page(use_huggingface, analysis_depth)
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "📋 View Results":
        view_results_page()

def upload_and_analyze_page(use_huggingface, analysis_depth):
    """Upload and analysis page with AI integration and sample data"""
    # Sample Data Section
    st.markdown("### 🗂️ Quick Start with Sample Data")
    
    resume_paths, jd_paths = get_sample_data_paths()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 Sample Resumes Available:**")
        
        # Show available sample resumes
        total_resumes = sum(len(files) for files in resume_paths.values())
        st.info(f"📊 {total_resumes} sample resumes ready for analysis")
        
        if st.button("🚀 Load Random Sample Resume", type="secondary"):
            # Get random resume from all available samples
            all_resumes = []
            for category, files in resume_paths.items():
                all_resumes.extend(files)
            
            if all_resumes:
                import random
                selected_resume = random.choice(all_resumes)
                resume_text = load_sample_file(selected_resume)
                
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.session_state.resume_processed = True
                    st.success(f"✅ Loaded: {os.path.basename(selected_resume)}")
                    
                    with st.expander("🔍 Preview"):
                        st.text_area("Content", resume_text[:500] + "...", height=150)
    
    with col2:
        st.markdown("**💼 Sample Job Descriptions Available:**")
        
        # Show available sample JDs
        total_jds = sum(len(files) for files in jd_paths.values())
        st.info(f"📊 {total_jds} sample job descriptions ready for analysis")
        
        if st.button("🚀 Load Random Sample JD", type="secondary"):
            # Get random JD from all available samples
            all_jds = []
            for category, files in jd_paths.items():
                all_jds.extend(files)
            
            if all_jds:
                import random
                selected_jd = random.choice(all_jds)
                jd_text = load_sample_file(selected_jd)
                
                if jd_text:
                    st.session_state.jd_text = jd_text
                    st.session_state.jd_processed = True
                    st.success(f"✅ Loaded: {os.path.basename(selected_jd)}")
                    
                    with st.expander("🔍 Preview"):
                        st.text_area("Content", jd_text[:500] + "...", height=150)
    
    st.markdown("---")
    st.markdown("### 📁 Upload Your Own Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📁 Job Description")
        jd_file = st.file_uploader("Choose a job description file", type=["pdf", "docx"], key="jd")
        
        if jd_file is not None:
            st.info(f"File: {jd_file.name} ({jd_file.size} bytes)")
            if st.button("🔄 Process Job Description", type="secondary"):
                with st.spinner("Processing job description..."):
                    # Upload file to backend
                    file_bytes = jd_file.getvalue()
                    response = upload_jd(st.session_state.token, file_bytes, jd_file.name)
                    if response and "jd_text" in response:
                        st.session_state.jd_text = response["jd_text"]
                        st.session_state.jd_processed = True
                        st.success("✅ Job Description processed!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", response["jd_text"][:500] + "...", height=150)
    
    with col2:
        st.header("📄 Resume")
        resume_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"], key="resume")
        
        if resume_file is not None:
            st.info(f"File: {resume_file.name} ({resume_file.size} bytes)")
            if st.button("🔄 Process Resume", type="secondary"):
                with st.spinner("Processing resume..."):
                    # Upload file to backend
                    file_bytes = resume_file.getvalue()
                    response = upload_resume(st.session_state.token, file_bytes, resume_file.name)
                    if response and "resume_text" in response:
                        st.session_state.resume_text = response["resume_text"]
                        st.session_state.resume_processed = True
                        st.success("✅ Resume processed!")
                        
                        with st.expander("🔍 Preview"):
                            st.text_area("Content", response["resume_text"][:500] + "...", height=150)
    
    # Analysis section
    if getattr(st.session_state, 'jd_processed', False) and getattr(st.session_state, 'resume_processed', False):
        st.markdown("---")
        st.header("🤖 AI-Powered Analysis")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 Start AI Analysis", type="primary"):
                perform_analysis(use_huggingface, analysis_depth)
    else:
        st.info("📝 Please upload/load files and process both resume and job description to start analysis.")

def perform_analysis(use_huggingface, analysis_depth):
    """Perform analysis with AI"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize
        status_text.text('🔄 Initializing analysis...')
        progress_bar.progress(10)
        
        # Perform evaluation using backend API
        status_text.text('🧮 Calculating scores...')
        progress_bar.progress(30)
        
        evaluation_result = evaluate_resume(
            st.session_state.token, 
            st.session_state.resume_text, 
            st.session_state.jd_text
        )
        
        if not evaluation_result:
            st.error("Failed to get evaluation results")
            return
        
        progress_bar.progress(60)
        status_text.text('🏆 Generating detailed analysis...')
        
        # Prepare verdict info
        verdict_info = {
            'combined_score': evaluation_result.get('final_score', 0),
            'verdict': evaluation_result.get('verdict', 'Unknown'),
            'explanation': evaluation_result.get('explanation', 'No explanation available'),
            'recommendation': "Consider tailoring your resume more closely to the job requirements."
        }
        
        progress_bar.progress(80)
        status_text.text('📊 Creating visualizations...')
        
        # Prepare detailed analysis data
        detailed_analysis = {
            'hard_match_score': evaluation_result.get('hard_match_score', 0),
            'semantic_match_score': evaluation_result.get('semantic_match_score', 0),
            'backend_scores': evaluation_result.get('backend_scores', {}),
            'detailed_text': evaluation_result.get('detailed_analysis', '')
        }
        
        progress_bar.progress(100)
        status_text.text('✅ Analysis complete!')
        
        # Display results with enhanced visualization
        display_enhanced_results(
            evaluation_result.get('hard_match_score', 0),
            evaluation_result.get('semantic_match_score', 0),
            verdict_info,
            detailed_analysis
        )
        
        # Store in history
        st.session_state.analysis_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hard_match': evaluation_result.get('hard_match_score', 0),
            'semantic_match': evaluation_result.get('semantic_match_score', 0),
            'final_score': evaluation_result.get('final_score', 0),
            'verdict': evaluation_result.get('verdict', 'Unknown'),
            'analysis_depth': analysis_depth
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
    
    # Backend scores visualization if available
    backend_scores = detailed_analysis.get('backend_scores', {})
    if backend_scores:
        st.markdown("### 🤖 AI Backend Performance")
        
        backend_labels = list(backend_scores.keys())
        backend_values = list(backend_scores.values())
        backend_colors = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7']
        
        fig_backend = go.Figure(data=[
            go.Bar(x=backend_labels, y=backend_values, marker_color=backend_colors[:len(backend_labels)],
                   text=[f"{score:.1f}%" for score in backend_values],
                   textposition='auto')
        ])
        
        fig_backend.update_layout(
            title="AI Backend Score Comparison",
            yaxis_title="Score (%)",
            yaxis_range=[0, 100],
            height=300
        )
        
        st.plotly_chart(fig_backend, use_container_width=True)
    
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
    if detailed_analysis.get('detailed_text'):
        st.markdown("### 🔍 Detailed Breakdown")
        st.text(detailed_analysis['detailed_text'])

def analytics_page():
    """Analytics page with advanced data analysis"""
    st.header("📊 Analytics & Insights")
    
    # Get user evaluations
    evaluations = get_user_evaluations(st.session_state.token)
    
    if evaluations:
        df = pd.DataFrame(evaluations)
        
        # Convert relevance_score to numeric if it's not already
        df['relevance_score'] = pd.to_numeric(df['relevance_score'], errors='coerce')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            st.metric("Average Score", f"{df['relevance_score'].mean():.1f}%")
        with col3:
            st.metric("Best Score", f"{df['relevance_score'].max():.1f}%")
        with col4:
            st.metric("Worst Score", f"{df['relevance_score'].min():.1f}%")
        
        # Score distribution chart
        st.subheader("📈 Score Distribution")
        
        fig_hist = go.Figure(data=[go.Histogram(x=df['relevance_score'], nbinsx=20)])
        fig_hist.update_layout(
            title="Distribution of Analysis Scores",
            xaxis_title="Score (%)",
            yaxis_title="Frequency",
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Trend analysis
        st.subheader("📈 Score Trend Over Time")
        
        # Convert created_at to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        df_sorted = df.sort_values('created_at')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_sorted['created_at'],
            y=df_sorted['relevance_score'],
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
        st.dataframe(df[['id', 'relevance_score', 'verdict', 'created_at']], use_container_width=True)
        
        # Performance insights
        st.subheader("💡 Performance Insights")
        
        avg_score = df['relevance_score'].mean()
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
    
    # Get user evaluations
    evaluations = get_user_evaluations(st.session_state.token)
    
    if evaluations:
        for i, result in enumerate(reversed(evaluations)):
            with st.expander(f"Analysis {len(evaluations)-i}: {result['verdict']} ({result['relevance_score']:.1f}%)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Timestamp:** {result['created_at']}")
                    st.write(f"**Hard Match:** {result['relevance_score']:.1f}%")
                with col2:
                    st.write(f"**Verdict:** {result['verdict']}")
    else:
        st.info("📋 No results available.")

if __name__ == "__main__":
    main()