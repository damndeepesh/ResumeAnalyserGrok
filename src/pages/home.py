import streamlit as st
import os
import tempfile
from PyPDF2 import PdfReader
import docx
from datetime import datetime

def extract_text_from_pdf(file):
    """Extract text from a PDF file"""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    """Extract text from a DOCX file"""
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def show_home_page():
    """Display the home page with resume upload and job role input"""
    # Initialize session state variables if they don't exist
    if "job_role" not in st.session_state:
        st.session_state.job_role = ""
    if "job_description" not in st.session_state:
        st.session_state.job_description = ""
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = None
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0
        
    st.header("Upload Your Resume")
    
    # File uploader for resume
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)", 
        type=["pdf", "docx", "txt"],
        help="Upload your resume to get an ATS compatibility score"
    )
    
    # Job role input
    job_role = st.text_input(
        "Enter your target job role",
        value=st.session_state.job_role if st.session_state.job_role else "",
        placeholder="e.g., Data Scientist, Software Engineer, Product Manager",
        help="Specify the job role you're applying for to get tailored analysis"
    )
    
    # Job description toggle and input
    job_desc_toggle = st.checkbox(
        "Add specific job description for enhanced analysis",
        help="Toggle this to add a specific job description for more accurate ATS analysis"
    )
    
    job_description = ""
    if job_desc_toggle:
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.get("job_description", ""),
            height=200,
            placeholder="Paste the full job description here for more precise keyword matching and tailored recommendations...",
            help="Adding the actual job description significantly improves analysis accuracy"
        )
    
    # Process the uploaded file
    if uploaded_file is not None:
        try:
            # Create a temporary file to store the uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Extract text from the file based on its type
            if uploaded_file.name.endswith('.pdf'):
                resume_text = extract_text_from_pdf(tmp_file_path)
            elif uploaded_file.name.endswith('.docx'):
                resume_text = extract_text_from_docx(tmp_file_path)
            else:  # Assume it's a text file
                resume_text = uploaded_file.getvalue().decode("utf-8")
            
            # Clean up the temporary file
            os.unlink(tmp_file_path)
            
            # Store the resume data, job role, and job description in session state
            st.session_state.resume_data = {
                "filename": uploaded_file.name,
                "text": resume_text,
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.job_role = job_role
            
            # Store job description if provided
            if job_desc_toggle and job_description:
                st.session_state.job_description = job_description
            elif not job_desc_toggle:
                # Clear job description if toggle is off
                st.session_state.job_description = ""
            
            # Display success message
            st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")
            
            # Preview the extracted text
            with st.expander("Preview Extracted Text"):
                st.text_area("Extracted Text", resume_text, height=300)
        
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
    
    # Instructions and tips
    with st.expander("Tips for ATS-Friendly Resumes"):
        st.markdown("""
        ### Tips to Make Your Resume ATS-Friendly
        
        1. **Use standard section headings** (e.g., Education, Experience, Skills)
        2. **Include relevant keywords** from the job description
        3. **Avoid using tables, headers, footers, and text boxes**
        4. **Use standard fonts** like Arial, Calibri, or Times New Roman
        5. **Save your resume as a simple PDF or DOCX file**
        6. **Include your contact information** at the top of the resume
        7. **Quantify your achievements** with numbers and metrics
        8. **Proofread carefully** for spelling and grammar errors
        """)
    
    # Action buttons at the bottom of the page
    if uploaded_file is not None and job_role:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save to History", type="primary", use_container_width=True, key="save_history_bottom"):
                # Create a basic entry with available information
                if "history" not in st.session_state:
                    st.session_state.history = []
                
                history_entry = {
                    "filename": st.session_state.resume_data["filename"],
                    "job_role": st.session_state.job_role,
                    "timestamp": st.session_state.resume_data["upload_time"],
                    "ats_score": 0,  # Placeholder until analysis is done
                    "keyword_match": 0,
                    "format_score": 0,
                    "readability_score": 0
                }
                
                st.session_state.history.append(history_entry)
                st.success("Resume saved to history!")
        with col2:
            if st.button("Analyze Resume", type="primary", use_container_width=True, key="analyze_bottom"):
                if job_role:
                    st.session_state.active_tab = 1  # Switch to Analysis tab
                    st.rerun()
                else:
                    st.warning("Please enter your target job role before analyzing.")