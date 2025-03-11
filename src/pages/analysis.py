import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os
from src.groq_client import analyze_resume

def show_analysis_page():
    """Display the analysis page with resume scoring and feedback"""
    st.header("Resume Analysis")
    
    # Check if resume data is available
    if st.session_state.resume_data is None:
        st.info("Please upload your resume on the Home page first.")
        return
    
    # Check if job role is available
    if not st.session_state.job_role:
        st.warning("Please specify your target job role on the Home page.")
        return
    
    # Display resume and job role information
    st.subheader("Analysis Information")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Resume**: {st.session_state.resume_data['filename']}")
    with col2:
        st.markdown(f"**Target Job Role**: {st.session_state.job_role}")
    
    # Check if analysis results are already available
    if st.session_state.analysis_results is None:
        # Show analysis in progress
        with st.spinner("Analyzing your resume... This may take a moment."):
            try:
                # Call the Groq API to analyze the resume
                analysis_results = analyze_resume(
                    resume_text=st.session_state.resume_data["text"],
                    job_role=st.session_state.job_role,
                    job_description=st.session_state.get("job_description", None)
                )
                
                # Store the analysis results in session state
                st.session_state.analysis_results = {
                    **analysis_results,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Add to history for comparison
                st.session_state.history.append({
                    "filename": st.session_state.resume_data["filename"],
                    "job_role": st.session_state.job_role,
                    "timestamp": st.session_state.analysis_results["timestamp"],
                    "ats_score": st.session_state.analysis_results["ats_score"],
                    "keyword_match": st.session_state.analysis_results["keyword_match"],
                    "format_score": st.session_state.analysis_results["format_score"],
                    "readability_score": st.session_state.analysis_results["readability_score"]
                })
                
                # Success message
                st.success("Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"Error analyzing resume: {str(e)}")
                return
    
    # Display the analysis results
    results = st.session_state.analysis_results
    
    # Overall ATS Score
    st.subheader("ATS Compatibility Score")
    score_col1, score_col2 = st.columns([1, 3])
    with score_col1:
        st.markdown(
            f"<div style='background-color: {'#4CAF50' if results['ats_score'] >= 80 else '#FFC107' if results['ats_score'] >= 60 else '#F44336'}; "
            f"padding: 20px; border-radius: 10px; text-align: center;'>"
            f"<h1 style='color: white; margin: 0;'>{results['ats_score']}/100</h1>"
            f"</div>",
            unsafe_allow_html=True
        )
    with score_col2:
        st.markdown(f"**Analysis Date**: {results['timestamp']}")
        st.markdown(f"**Keyword Match**: {results['keyword_match']}/100")
        st.markdown(f"**Format & Structure**: {results['format_score']}/100")
        st.markdown(f"**Readability**: {results['readability_score']}/100")
        
        # Detailed Format Scores
        st.markdown("### Detailed Format Scores")
        format_scores = {
            "Document Structure": results.get('document_structure_score', 0),
            "Section Headers": results.get('section_headers_score', 0),
            "Content Organization": results.get('content_organization_score', 0),
            "Visual Layout": results.get('visual_layout_score', 0)
        }
        
        for score_name, score in format_scores.items():
            st.markdown(
                f"<div style='margin-bottom: 10px;'>"
                f"<span style='color: #666;'>{score_name}:</span> "
                f"<span style='color: {'#4CAF50' if score >= 80 else '#FFC107' if score >= 60 else '#F44336'};'>"
                f"{score}/100</span></div>",
                unsafe_allow_html=True
            )
        
        # Format Tips
        if format_tips := results.get('format_tips', []):
            with st.expander("Format Improvement Tips", expanded=True):
                for tip in format_tips:
                    st.markdown(f"- {tip}")
    
    # Detailed Analysis
    st.subheader("Detailed Analysis")
    with st.expander("Strengths", expanded=True):
        for strength in results['strengths']:
            st.markdown(f"- {strength}")
    
    with st.expander("Areas for Improvement", expanded=True):
        for improvement in results['improvements']:
            st.markdown(f"- {improvement}")
    
    # Missing Keywords
    st.subheader("Missing Keywords")
    st.markdown("These keywords are commonly found in job descriptions for your target role but are missing from your resume:")
    missing_keywords = results['missing_keywords']
    if missing_keywords:
        # Display as a table
        keyword_df = pd.DataFrame({
            "Keyword": missing_keywords,
            "Importance": ["High" if i < len(missing_keywords)//3 else 
                         "Medium" if i < 2*len(missing_keywords)//3 else 
                         "Low" for i in range(len(missing_keywords))]
        })
        st.dataframe(keyword_df, use_container_width=True)
    else:
        st.info("Great job! Your resume contains all the important keywords for this role.")
    
    # Advanced Resume Review (when job description is provided)
    if st.session_state.get("job_description"):
        st.subheader("Advanced Resume Review")
        
        # Create tabs for different aspects of the advanced review
        review_tabs = st.tabs(["Skill Gaps", "Experience Gaps", "Enhancement Tips"])
        
        # Skill Gaps tab
        with review_tabs[0]:
            st.markdown("### Skill Gaps")
            st.markdown("These are specific skills mentioned in the job description that are missing from your resume:")
            skill_gaps = results.get('skill_gaps', [])
            if skill_gaps:
                for skill in skill_gaps:
                    st.markdown(f"- {skill}")
            else:
                st.success("Great job! Your resume covers all the key skills mentioned in the job description.")
        
        # Experience Gaps tab
        with review_tabs[1]:
            st.markdown("### Experience Gaps")
            st.markdown("These are experience requirements from the job description that aren't clearly demonstrated in your resume:")
            experience_gaps = results.get('experience_gaps', [])
            if experience_gaps:
                for exp in experience_gaps:
                    st.markdown(f"- {exp}")
            else:
                st.success("Your experience appears to match the job requirements well!")
        
        # Enhancement Tips tab
        with review_tabs[2]:
            st.markdown("### Resume Enhancement Tips")
            st.markdown("Specific ways to enhance your resume for this exact job:")
            enhancement_tips = results.get('resume_enhancement_tips', [])
            if enhancement_tips:
                for tip in enhancement_tips:
                    st.markdown(f"- {tip}")
    
    # Recommendations
    st.subheader("Recommendations")
    for recommendation in results['recommendations']:
        st.markdown(f"- {recommendation}")
    
    # Action buttons section removed as requested