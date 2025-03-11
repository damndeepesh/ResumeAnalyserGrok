import os
import re
import pickle
from datetime import datetime
import pandas as pd

def save_analysis_to_history(analysis_results, resume_data, job_role):
    """Save the current analysis results to history
    
    Args:
        analysis_results (dict): The analysis results from the Groq API
        resume_data (dict): The resume data including filename and text
        job_role (str): The target job role
        
    Returns:
        dict: The history entry that was created
    """
    # Create a history entry
    history_entry = {
        "filename": resume_data["filename"],
        "job_role": job_role,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ats_score": analysis_results["ats_score"],
        "keyword_match": analysis_results["keyword_match"],
        "format_score": analysis_results["format_score"],
        "readability_score": analysis_results["readability_score"]
    }
    
    return history_entry

def format_timestamp(timestamp_str):
    """Format a timestamp string for display
    
    Args:
        timestamp_str (str): Timestamp string in format '%Y-%m-%d %H:%M:%S'
        
    Returns:
        str: Formatted timestamp for display
    """
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return timestamp_str

def get_score_color(score):
    """Get a color based on a score value
    
    Args:
        score (int): Score value (0-100)
        
    Returns:
        str: Hex color code
    """
    if score >= 80:
        return "#4CAF50"  # Green
    elif score >= 60:
        return "#FFC107"  # Yellow/Amber
    else:
        return "#F44336"  # Red

def clean_text(text):
    """Clean and normalize text for analysis
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters that might interfere with analysis
    text = re.sub(r'[^\w\s.,;:!?\-\(\)]', ' ', text)
    
    return text

def export_analysis_to_csv(history_data, filename="resume_analysis_history.csv"):
    """Export analysis history to a CSV file
    
    Args:
        history_data (list): List of history entries
        filename (str): Output filename
        
    Returns:
        str: Path to the saved file
    """
    # Convert to DataFrame
    df = pd.DataFrame(history_data)
    
    # Save to CSV
    output_path = os.path.join(os.getcwd(), filename)
    df.to_csv(output_path, index=False)
    
    return output_path