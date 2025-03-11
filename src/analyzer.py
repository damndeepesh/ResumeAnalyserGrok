import os
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from src.groq_client import analyze_resume

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model is not installed, provide instructions
    print("The spaCy model 'en_core_web_sm' is not installed.")
    print("Please install it using: python3 -m spacy download en_core_web_sm")
    # Create a simple placeholder model for basic functionality
    nlp = spacy.blank("en")

def preprocess_text(text):
    """Preprocess resume text for analysis
    
    Args:
        text (str): Raw text extracted from resume
        
    Returns:
        str: Preprocessed text
    """
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Convert to lowercase
    text = text.lower()
    
    return text

def extract_keywords(text, job_role):
    """Extract keywords from resume text
    
    Args:
        text (str): Preprocessed resume text
        job_role (str): Target job role
        
    Returns:
        list: Extracted keywords
    """
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract nouns, proper nouns, and skill-related words
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2]
    
    # Use CountVectorizer to get the most common terms
    vectorizer = CountVectorizer(max_features=50, stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform([text])
    common_terms = vectorizer.get_feature_names_out()
    
    # Combine and remove duplicates
    all_keywords = list(set(keywords + list(common_terms)))
    
    return all_keywords

def analyze_resume_local(resume_text, job_role):
    """Perform local analysis on resume text before calling the Groq API
    
    Args:
        resume_text (str): Raw text extracted from resume
        job_role (str): Target job role
        
    Returns:
        dict: Local analysis results
    """
    # Preprocess the text
    processed_text = preprocess_text(resume_text)
    
    # Extract keywords
    keywords = extract_keywords(processed_text, job_role)
    
    # Perform basic format analysis
    format_score = calculate_format_score(resume_text)
    
    # Perform basic readability analysis
    readability_score = calculate_readability_score(resume_text)
    
    return {
        "local_keywords": keywords,
        "local_format_score": format_score,
        "local_readability_score": readability_score
    }

def calculate_format_score(text):
    """Calculate a basic format score for the resume
    
    Args:
        text (str): Resume text
        
    Returns:
        int: Format score (0-100)
    """
    score = 70  # Base score
    
    # Check for section headers
    section_patterns = ["experience", "education", "skills", "projects", "certifications", "summary"]
    found_sections = 0
    for pattern in section_patterns:
        if re.search(r'\b' + pattern + r'\b', text.lower()):
            found_sections += 1
    
    # Adjust score based on sections found
    section_score = min(found_sections * 5, 20)
    score += section_score
    
    # Check for bullet points
    bullet_count = text.count('•') + text.count('·') + text.count('-')
    bullet_score = min(bullet_count, 10)
    score += bullet_score
    
    return min(score, 100)  # Cap at 100

def calculate_readability_score(text):
    """Calculate a basic readability score for the resume
    
    Args:
        text (str): Resume text
        
    Returns:
        int: Readability score (0-100)
    """
    # Base score
    score = 70
    
    # Split into sentences and words
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Calculate average sentence length
    if sentences:
        words = []
        for sentence in sentences:
            words.extend(sentence.split())
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Penalize very long sentences
        if avg_sentence_length > 25:
            score -= 10
        elif avg_sentence_length < 10:
            score += 5
    
    return min(max(score, 0), 100)  # Keep between 0-100

def get_resume_analysis(resume_text, job_role, job_description=None):
    """Main function to analyze a resume
    
    Args:
        resume_text (str): Text extracted from resume
        job_role (str): Target job role
        job_description (str, optional): Specific job description for enhanced analysis
        
    Returns:
        dict: Complete analysis results
    """
    # First perform local analysis
    local_results = analyze_resume_local(resume_text, job_role)
    
    # Then call the Groq API for advanced analysis
    groq_results = analyze_resume(resume_text, job_role, job_description)
    
    # Combine results
    combined_results = {
        **groq_results,
        "local_keywords": local_results["local_keywords"]
    }
    
    return combined_results