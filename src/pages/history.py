import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def show_history_page():
    """Display the history page with previous resume analyses"""
    st.header("Resume Analysis History")
    
    # Check if there's any history data
    if not st.session_state.history:
        st.info("You haven't analyzed any resumes yet. Upload and analyze a resume to see your history.")
        return
    
    # Display history data
    st.subheader("Previous Analyses")
    
    # Create a DataFrame from history data
    history_df = pd.DataFrame(st.session_state.history)
    
    # Format the DataFrame for display
    display_df = history_df[['timestamp', 'filename', 'job_role', 'ats_score', 'keyword_match', 'format_score', 'readability_score']].copy()
    display_df.columns = ['Timestamp', 'Resume', 'Job Role', 'ATS Score', 'Keyword Match', 'Format Score', 'Readability Score']
    
    # Display the history table
    st.dataframe(display_df, use_container_width=True)
    
    # Option to clear history
    if st.button("Clear History", type="secondary"):
        st.session_state.history = []
        st.success("History cleared successfully!")
        st.experimental_rerun()
    
    # Trend analysis (if there are multiple entries)
    if len(st.session_state.history) > 1:
        st.subheader("Score Trend Analysis")
        
        # Create trend data
        trend_data = history_df.sort_values('timestamp')
        
        # Plot the trend
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot each score type
        ax.plot(trend_data['timestamp'], trend_data['ats_score'], marker='o', linewidth=2, label='ATS Score')
        ax.plot(trend_data['timestamp'], trend_data['keyword_match'], marker='s', linewidth=2, label='Keyword Match')
        ax.plot(trend_data['timestamp'], trend_data['format_score'], marker='^', linewidth=2, label='Format Score')
        ax.plot(trend_data['timestamp'], trend_data['readability_score'], marker='d', linewidth=2, label='Readability Score')
        
        # Customize the plot
        ax.set_title('Resume Score Trends Over Time')
        ax.set_ylim(0, 100)
        ax.set_ylabel('Score')
        ax.set_xlabel('Analysis Date')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Display the plot
        st.pyplot(fig)
        
        # Improvement analysis
        if len(st.session_state.history) >= 2:
            st.subheader("Improvement Analysis")
            
            # Get the first and last entries
            first_entry = trend_data.iloc[0]
            last_entry = trend_data.iloc[-1]
            
            # Calculate improvements
            ats_improvement = last_entry['ats_score'] - first_entry['ats_score']
            keyword_improvement = last_entry['keyword_match'] - first_entry['keyword_match']
            format_improvement = last_entry['format_score'] - first_entry['format_score']
            readability_improvement = last_entry['readability_score'] - first_entry['readability_score']
            
            # Display improvements
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "ATS Score Improvement",
                    f"{last_entry['ats_score']}/100",
                    delta=f"{ats_improvement:+.1f}"
                )
            
            with col2:
                st.metric(
                    "Keyword Match Improvement",
                    f"{last_entry['keyword_match']}/100",
                    delta=f"{keyword_improvement:+.1f}"
                )
            
            with col3:
                st.metric(
                    "Format Score Improvement",
                    f"{last_entry['format_score']}/100",
                    delta=f"{format_improvement:+.1f}"
                )
            
            with col4:
                st.metric(
                    "Readability Score Improvement",
                    f"{last_entry['readability_score']}/100",
                    delta=f"{readability_improvement:+.1f}"
                )
            
            # Overall assessment
            if ats_improvement > 0:
                st.success("Your resume has improved since your first analysis! Keep up the good work.")
            elif ats_improvement == 0:
                st.info("Your overall score has remained the same. Check the specific metrics to see where you can improve.")
            else:
                st.warning("Your overall score has decreased. This might be because you're targeting a different job role or have made changes that reduced ATS compatibility.")
    
    # Tips for improvement
    st.subheader("Tips for Improving Your Score")
    st.markdown("""
    ### How to Improve Your ATS Score
    
    1. **Add missing keywords** from your target job descriptions
    2. **Use standard section headings** that ATS systems can easily recognize
    3. **Simplify formatting** by removing tables, text boxes, and complex layouts
    4. **Quantify achievements** with numbers and metrics
    5. **Use industry-standard terminology** relevant to your target role
    6. **Tailor your resume** for each specific job application
    7. **Use a clean, simple design** with standard fonts
    8. **Save as PDF or DOCX** formats that are ATS-friendly
    """)