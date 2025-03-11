import streamlit as st
import pandas as pd

def show_suggestions_page():
    """Display suggestions and recommendations for resume improvement"""
    st.header("Resume Suggestions & Recommendations")
    
    # Check if resume data is available
    if st.session_state.resume_data is None:
        st.info("Please upload your resume on the Home page first.")
        return
    
    # Check if analysis results are available
    if st.session_state.analysis_results is None:
        st.warning("Please analyze your resume first to get personalized suggestions.")
        return
    
    # Get analysis results
    results = st.session_state.analysis_results
    
    # Resume Overview Section
    st.subheader("Resume Overview")
    overview_col1, overview_col2 = st.columns(2)
    
    with overview_col1:
        st.markdown("### Current Resume Status")
        st.markdown(f"**Overall ATS Score**: {results['ats_score']}/100")
        st.markdown(f"**Keyword Match Rate**: {results['keyword_match']}/100")
        st.markdown(f"**Format Score**: {results['format_score']}/100")
        st.markdown(f"**Readability Score**: {results['readability_score']}/100")
    
    with overview_col2:
        st.markdown("### Target Job Role")
        st.markdown(f"**Role**: {st.session_state.job_role}")
        if st.session_state.get('job_description'):
            st.markdown("✅ Using specific job description for analysis")
        else:
            st.markdown("ℹ️ Using general role requirements for analysis")
    
    # Detailed Suggestions Tabs
    suggestion_tabs = st.tabs(["Content Enhancement", "Skills & Keywords", "Format & Structure", "Industry Insights"])
    
    # Content Enhancement Tab
    with suggestion_tabs[0]:
        st.markdown("### Content Enhancement Suggestions")
        
        # Current Strengths
        st.markdown("#### Current Strengths")
        for strength in results['strengths']:
            st.markdown(f"✅ {strength}")
        
        # Areas for Improvement
        st.markdown("#### Areas for Improvement")
        for improvement in results['improvements']:
            st.markdown(f"🔄 {improvement}")
        
        # Specific Recommendations
        st.markdown("#### Action Items")
        for recommendation in results['recommendations']:
            st.markdown(f"📌 {recommendation}")
    
    # Skills & Keywords Tab
    with suggestion_tabs[1]:
        st.markdown("### Skills & Keywords Analysis")
        
        # Present Keywords
        st.markdown("#### Present Keywords")
        present_keywords = results.get('present_keywords', [])
        if present_keywords:
            for keyword in present_keywords:
                st.markdown(f"✅ {keyword}")
        else:
            st.info("No keywords were identified in your resume. Consider adding relevant keywords from the job description.")
        
        # Missing Keywords with Importance
        st.markdown("#### Missing Keywords")
        missing_keywords = results.get('missing_keywords', [])
        if missing_keywords:
            keyword_df = pd.DataFrame({
                "Keyword": missing_keywords,
                "Importance": ["High" if i < len(missing_keywords)//3 else 
                             "Medium" if i < 2*len(missing_keywords)//3 else 
                             "Low" for i in range(len(missing_keywords))]
            })
            st.dataframe(keyword_df, use_container_width=True)
        else:
            st.success("Great job! Your resume appears to contain all the important keywords for this role.")
        
        # Industry-Specific Skills
        st.markdown("#### Recommended Industry Skills")
        if 'recommended_skills' in results and results['recommended_skills']:
            for skill in results['recommended_skills']:
                st.markdown(f"💡 {skill}")
        else:
            st.info("No additional industry-specific skills recommendations available for your target role.")
    
    # Format & Structure Tab
    with suggestion_tabs[2]:
        st.markdown("### Format & Structure Analysis")
        
        # Format Score Breakdown
        st.markdown("#### Format Score Components")
        format_components = [
            "Document Structure",
            "Section Headers",
            "Content Organization",
            "Visual Layout"
        ]
        has_scores = False
        for component in format_components:
            score = results.get(f"{component.lower().replace(' ', '_')}_score", 0)
            if score > 0:
                has_scores = True
            st.progress(score/100)
            st.markdown(f"**{component}**: {score}/100")
        
        if not has_scores:
            st.info("Detailed format scoring is not available. Please ensure your resume has been properly analyzed.")
        
        # Format Recommendations
        st.markdown("#### Format Improvement Tips")
        format_tips = results.get('format_tips', [])
        if format_tips:
            for tip in format_tips:
                st.markdown(f"🔧 {tip}")
        else:
            st.info("No specific format improvement tips available. Your resume format may already be well-structured.")
    
    # Industry Insights Tab
    with suggestion_tabs[3]:
        st.markdown("### Industry Insights & Trends")
        
        # Job Market Trends
        st.markdown("#### Current Job Market Trends")
        if 'industry_trends' in results and results['industry_trends']:
            for trend in results['industry_trends']:
                st.markdown(f"📈 {trend}")
        else:
            st.info("Industry trend data is not available at the moment.")
        
        # Career Development Suggestions
        st.markdown("#### Career Development Recommendations")
        if 'career_recommendations' in results and results['career_recommendations']:
            for rec in results['career_recommendations']:
                st.markdown(f"🎯 {rec}")
        else:
            st.info("Career development recommendations will be available after analyzing your resume against specific job requirements.")
        
        # Certification Recommendations
        st.markdown("#### Recommended Certifications")
        if 'recommended_certifications' in results and results['recommended_certifications']:
            for cert in results['recommended_certifications']:
                st.markdown(f"🏅 {cert}")
        else:
            st.info("No specific certification recommendations available for your target role at this time.")