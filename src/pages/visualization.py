import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re

def show_visualization_page():
    """Display visualizations of resume analysis results"""
    st.header("Resume Analysis Visualizations")
    
    # Check if analysis results are available
    if st.session_state.analysis_results is None:
        st.info("Please analyze your resume on the Analysis page first.")
        return
    
    # Get analysis results
    results = st.session_state.analysis_results
    resume_text = st.session_state.resume_data["text"]
    job_role = st.session_state.job_role
    
    # Create tabs for different visualizations
    viz_tabs = st.tabs(["Score Breakdown", "Word Cloud", "Keyword Analysis", "Comparison"])
    
    # Score Breakdown tab
    with viz_tabs[0]:
        st.subheader("ATS Score Breakdown")
        
        # Create data for the score breakdown chart
        score_data = pd.DataFrame({
            'Category': ['Overall ATS Score', 'Keyword Match', 'Format & Structure', 'Readability'],
            'Score': [
                results['ats_score'], 
                results['keyword_match'], 
                results['format_score'], 
                results['readability_score']
            ]
        })
        
        # Create a horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(
            score_data['Category'], 
            score_data['Score'],
            color=['#4a86e8', '#ff9900', '#6aa84f', '#e06666']
        )
        
        # Add score labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 2, 
                bar.get_y() + bar.get_height()/2, 
                f'{width}/100', 
                va='center'
            )
        
        # Customize the chart
        ax.set_xlim(0, 105)
        ax.set_xlabel('Score')
        ax.set_title('Resume ATS Score Breakdown')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Display the chart
        st.pyplot(fig)
        
        # Add explanation
        st.markdown("""
        ### Score Explanation
        
        - **Overall ATS Score**: Composite score indicating how well your resume would perform in an ATS system
        - **Keyword Match**: How well your resume matches keywords for the target job role
        - **Format & Structure**: Assessment of your resume's formatting and structure for ATS compatibility
        - **Readability**: How easy your resume is to read and understand
        """)
    
    # Word Cloud tab
    with viz_tabs[1]:
        st.subheader("Resume Word Cloud")
        
        # Process text for word cloud
        def preprocess_text(text):
            # Remove special characters and numbers
            text = re.sub(r'[^\w\s]', '', text)
            text = re.sub(r'\d+', '', text)
            # Convert to lowercase
            text = text.lower()
            # Remove common stop words (simplified version)
            stop_words = ['and', 'the', 'to', 'of', 'in', 'a', 'for', 'with', 'on', 'at', 'from', 'by', 'an', 'is', 'was', 'were', 'are', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'but', 'or', 'as', 'if', 'while', 'because', 'so', 'than', 'that', 'this', 'these', 'those', 'then', 'not', 'no']
            words = text.split()
            filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
            return ' '.join(filtered_words)
        
        processed_text = preprocess_text(resume_text)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white', 
            colormap='viridis', 
            max_words=100, 
            contour_width=1, 
            contour_color='steelblue'
        ).generate(processed_text)
        
        # Display word cloud
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        
        st.markdown("""
        ### Word Cloud Analysis
        
        The word cloud visualizes the most frequently used words in your resume. 
        Larger words appear more frequently. This can help you identify:
        
        - Which terms are most prominent in your resume
        - Whether your resume emphasizes the right skills and experiences
        - Potential overused words that could be replaced with more impactful terms
        """)
    
    # Keyword Analysis tab
    with viz_tabs[2]:
        st.subheader("Keyword Analysis")
        
        # Create data for present and missing keywords
        present_keywords = results.get('present_keywords', [])
        missing_keywords = results.get('missing_keywords', [])
        
        # Display keyword match percentage
        st.metric(
            "Keyword Match Rate", 
            f"{results['keyword_match']}%",
            delta=f"{len(present_keywords)} present, {len(missing_keywords)} missing"
        )
        
        # Create columns for present and missing keywords
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Present Keywords")
            if present_keywords:
                for keyword in present_keywords:
                    st.markdown(f"✅ {keyword}")
            else:
                st.info("No matching keywords found.")
        
        with col2:
            st.markdown("### Missing Keywords")
            if missing_keywords:
                for keyword in missing_keywords:
                    st.markdown(f"❌ {keyword}")
            else:
                st.success("Great job! Your resume contains all important keywords.")
        
        # Keyword distribution chart
        if present_keywords or missing_keywords:
            st.subheader("Keyword Distribution")
            
            # Create data for pie chart
            labels = ['Present', 'Missing']
            sizes = [len(present_keywords), len(missing_keywords)]
            colors = ['#4CAF50', '#F44336']
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(
                sizes, 
                labels=labels, 
                colors=colors, 
                autopct='%1.1f%%',
                startangle=90,
                shadow=True,
                explode=(0.05, 0)
            )
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            # Display the chart
            st.pyplot(fig)
    
    # Comparison tab (if history exists)
    with viz_tabs[3]:
        st.subheader("Historical Comparison")
        
        if len(st.session_state.history) <= 1:
            st.info("You need at least two resume analyses to see a comparison. Save your current analysis and upload a different version of your resume to compare.")
        else:
            # Create data for the comparison chart
            history_data = pd.DataFrame(st.session_state.history)
            
            # Select which versions to compare
            selected_versions = st.multiselect(
                "Select resume versions to compare",
                options=history_data['timestamp'].tolist(),
                default=history_data['timestamp'].tolist()[-2:]
            )
            
            if selected_versions:
                # Filter data based on selection
                filtered_data = history_data[history_data['timestamp'].isin(selected_versions)]
                
                # Create a comparison chart
                st.subheader("Score Comparison")
                
                # Reshape data for grouped bar chart
                chart_data = pd.melt(
                    filtered_data,
                    id_vars=['timestamp', 'filename'],
                    value_vars=['ats_score', 'keyword_match', 'format_score'],
                    var_name='Score Type',
                    value_name='Score'
                )
                
                # Create a grouped bar chart
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.barplot(
                    x='Score Type', 
                    y='Score', 
                    hue='timestamp', 
                    data=chart_data,
                    palette='viridis'
                )
                
                # Customize the chart
                ax.set_title('Resume Score Comparison')
                ax.set_ylim(0, 100)
                ax.set_xlabel('Score Category')
                ax.set_ylabel('Score')
                ax.legend(title='Version')
                
                # Display the chart
                st.pyplot(fig)
                
                # Display a table with detailed comparison
                st.subheader("Detailed Comparison")
                comparison_table = filtered_data[['timestamp', 'filename', 'job_role', 'ats_score', 'keyword_match', 'format_score']]
                comparison_table.columns = ['Timestamp', 'Filename', 'Job Role', 'ATS Score', 'Keyword Match', 'Format Score']
                st.dataframe(comparison_table, use_container_width=True)