import streamlit as st
import requests
import tempfile
import os
from io import BytesIO

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
    st.title("Resume Relevance Check Dashboard")
    
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Upload & Analyze", "View Results"])
    
    if page == "Upload & Analyze":
        st.header("Upload Job Description")
        jd_file = st.file_uploader("Choose a job description file", type=["pdf", "docx"], key="jd")
        
        if jd_file is not None:
            if st.button("Process Job Description"):
                with st.spinner("Processing job description..."):
                    jd_text = extract_text_from_file(jd_file)
                    if jd_text:
                        st.session_state.jd_text = jd_text
                        st.success("Job Description processed successfully!")
                        st.text_area("Job Description Preview", jd_text[:500] + "...", height=150)

        st.header("Upload Resume")
        resume_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"], key="resume")
        
        if resume_file is not None:
            if st.button("Process Resume"):
                with st.spinner("Processing resume..."):
                    resume_text = extract_text_from_file(resume_file)
                    if resume_text:
                        st.session_state.resume_text = resume_text
                        st.success("Resume processed successfully!")
                        st.text_area("Resume Preview", resume_text[:500] + "...", height=150)

        st.header("Evaluation")
        if st.session_state.jd_text and st.session_state.resume_text:
            if st.button("Evaluate Match", type="primary"):
                with st.spinner("Evaluating match..."):
                    try:
                        # Use local imports to evaluate
                        from src.scoring.hard_match import calculate_hard_match
                        from src.scoring.semantic_match import calculate_semantic_match
                        from src.scoring.verdict import get_verdict, get_detailed_verdict
                        from src.storage.database import store_evaluation_results
                        
                        # Prepare data
                        resume_data = {"raw_text": st.session_state.resume_text}
                        jd_data = {"raw_text": st.session_state.jd_text}
                        
                        # Calculate scores
                        hard_match_score = calculate_hard_match(resume_data, jd_data)
                        semantic_match_score = calculate_semantic_match(resume_data, jd_data)
                        
                        # Get detailed verdict
                        verdict_info = get_detailed_verdict(hard_match_score, semantic_match_score)
                        
                        # Store results
                        evaluation_result = {
                            "hard_match_score": hard_match_score,
                            "semantic_match_score": semantic_match_score,
                            "final_score": verdict_info["combined_score"],
                            "verdict": verdict_info["verdict"]
                        }
                        store_evaluation_results(evaluation_result)
                        
                        # Display results
                        st.success("Evaluation completed!")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Hard Match Score", f"{hard_match_score:.1f}%")
                        with col2:
                            st.metric("Semantic Match Score", f"{semantic_match_score:.1f}%")
                        with col3:
                            st.metric("Final Score", f"{verdict_info['combined_score']:.1f}%")
                        
                        # Verdict with color coding
                        verdict_color = {
                            "High": "green",
                            "Medium": "orange", 
                            "Low": "red"
                        }
                        
                        st.markdown(f"### Verdict: :{verdict_color.get(verdict_info['verdict'], 'blue')}[{verdict_info['verdict']}]")
                        st.write(verdict_info['explanation'])
                        
                    except Exception as e:
                        st.error(f"Error during evaluation: {e}")
        else:
            st.info("Please upload and process both a job description and resume to evaluate the match.")
    
    elif page == "View Results":
        st.header("Recent Evaluation Results")
        
        try:
            from src.storage.database import SessionLocal, Evaluation
            db = SessionLocal()
            evaluations = db.query(Evaluation).order_by(Evaluation.id.desc()).limit(10).all()
            db.close()
            
            if evaluations:
                for i, eval in enumerate(evaluations):
                    with st.expander(f"Evaluation {eval.id} - {eval.verdict} ({eval.relevance_score}%)"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {eval.id}")
                            st.write(f"**Score:** {eval.relevance_score}%")
                        with col2:
                            st.write(f"**Verdict:** {eval.verdict}")
                            if eval.missing_elements:
                                st.write(f"**Notes:** {eval.missing_elements}")
            else:
                st.info("No evaluation results found.")
                
        except Exception as e:
            st.error(f"Error loading results: {e}")

if __name__ == "__main__":
    main()