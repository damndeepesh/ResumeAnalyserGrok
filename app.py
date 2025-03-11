import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import page modules
from src.pages.home import show_home_page
from src.pages.analysis import show_analysis_page
from src.pages.visualization import show_visualization_page
from src.pages.history import show_history_page
from src.pages.suggestions import show_suggestions_page

# App configuration
st.set_page_config(
    page_title="Resume ATS Scorer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4a86e8;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">Resume ATS Scoring System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Optimize your resume for Applicant Tracking Systems</p>', unsafe_allow_html=True)

# Session state initialization
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'job_role' not in st.session_state:
    st.session_state.job_role = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Navigation tabs
tabs = st.tabs(["Home", "Analysis", "Visualization", "Suggestions", "History"])

# Display the appropriate page based on the selected tab
with tabs[0]:
    show_home_page()
    
with tabs[1]:
    show_analysis_page()
    
with tabs[2]:
    show_visualization_page()
    
with tabs[3]:
    show_suggestions_page()
    
with tabs[4]:
    show_history_page()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    <p>Resume ATS Scoring System | Powered by Groq API</p>
</div>
""", unsafe_allow_html=True)