import os
import json
from groq import Groq

# Initialize Groq client
def get_groq_client():
    """Initialize and return a Groq client using the API key from environment variables"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please add it to your .env file.")
    return Groq(api_key=api_key)

def analyze_resume(resume_text, job_role, job_description=None):
    """Analyze a resume using the Groq API
    
    Args:
        resume_text (str): The extracted text from the resume
        job_role (str): The target job role
        job_description (str, optional): Specific job description for enhanced analysis
        
    Returns:
        dict: Analysis results including scores and recommendations
    """
    client = get_groq_client()
    
    # Prepare the prompt for the Groq API
    job_desc_text = ""
    if job_description:
        job_desc_text = f"""
        JOB DESCRIPTION:
        {job_description}
        
        Please analyze the resume specifically against this job description, identifying exact matches and gaps.
        """
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) analyzer and resume consultant with deep knowledge of industry trends. 
    Please analyze the following resume for the role of {job_role}.
    
    RESUME TEXT:
    {resume_text}
    {job_desc_text}
    Provide a comprehensive analysis in the following JSON format:
    {{
        "ats_score": <overall score from 0-100>,
        "keyword_match": <keyword match score from 0-100>,
        "format_score": <format and structure score from 0-100>,
        "readability_score": <readability score from 0-100>,
        "document_structure_score": <score for document organization and flow from 0-100>,
        "section_headers_score": <score for section header clarity and formatting from 0-100>,
        "content_organization_score": <score for content layout and organization from 0-100>,
        "visual_layout_score": <score for visual presentation and spacing from 0-100>,
        "strengths": [<list of 3-5 strengths>],
        "improvements": [<list of 3-5 areas for improvement>],
        "missing_keywords": [<list of important keywords missing from the resume>],
        "present_keywords": [<list of important keywords present in the resume>],
        "recommendations": [<list of 3-5 specific recommendations to improve the resume>],
        "skill_gaps": [<list of specific skills mentioned in the job description but missing from the resume>],
        "experience_gaps": [<list of experience requirements mentioned in the job description but not evident in the resume>],
        "resume_enhancement_tips": [<list of 3-5 specific ways to enhance the resume for this exact job>],
        "format_tips": [<list of specific formatting recommendations>],
        "industry_trends": [<list of 3-5 current trends in the industry relevant to the role>],
        "career_recommendations": [<list of 3-5 career development suggestions based on the resume and role>],
        "recommended_certifications": [<list of relevant certifications that would enhance the candidate's profile>]
    }}
    
    Ensure your analysis is detailed, specific to the {job_role} role, and actionable. Include current industry trends, career development paths, and relevant certifications for the role.
    """
    
    # Call the Groq API
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert ATS analyzer and resume consultant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",  # Using Llama 3 70B model for high-quality analysis
            temperature=0.2,  # Low temperature for more consistent results
            max_tokens=4000,  # Allow for detailed analysis
            top_p=0.9
        )
        
        # Extract and parse the response
        response_text = chat_completion.choices[0].message.content
        
        # Find the JSON part in the response
        try:
            # Try to parse the entire response as JSON first
            analysis_results = json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the text
            import re
            json_match = re.search(r'\{\s*"ats_score".*\}', response_text, re.DOTALL)
            if json_match:
                analysis_results = json.loads(json_match.group(0))
            else:
                raise ValueError("Could not extract valid JSON from the API response")
        
        # Ensure all required fields are present
        required_fields = [
            "ats_score", "keyword_match", "format_score", "readability_score",
            "document_structure_score", "section_headers_score", "content_organization_score", "visual_layout_score",
            "strengths", "improvements", "missing_keywords", "present_keywords", "recommendations", "format_tips",
            "industry_trends", "career_recommendations", "recommended_certifications"
        ]
        
        for field in required_fields:
            if field not in analysis_results:
                if field in ["missing_keywords", "present_keywords"]:
                    analysis_results[field] = []
                elif field in ["strengths", "improvements", "recommendations"]:
                    analysis_results[field] = ["No specific " + field + " identified."]
                else:
                    analysis_results[field] = 70  # Default score
        
        return analysis_results
        
    except Exception as e:
        # Handle API errors
        error_msg = f"Error calling Groq API: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)

# Example of how the analysis results should look
SAMPLE_ANALYSIS = {
    "ats_score": 78,
    "keyword_match": 72,
    "format_score": 85,
    "readability_score": 80,
    "document_structure_score": 82,
    "section_headers_score": 88,
    "content_organization_score": 85,
    "visual_layout_score": 80,
    "strengths": [
        "Clear section headings that are ATS-friendly",
        "Good use of action verbs and quantifiable achievements",
        "Relevant technical skills clearly listed",
        "Consistent formatting throughout the document"
    ],
    "improvements": [
        "Missing some key industry-specific keywords",
        "Contact information could be more prominently displayed",
        "Some bullet points are too lengthy for optimal ATS parsing",
        "Education section lacks detail about relevant coursework"
    ],
    "missing_keywords": [
        "project management",
        "agile methodology",
        "cross-functional",
        "stakeholder management",
        "KPI tracking"
    ],
    "present_keywords": [
        "data analysis",
        "team leadership",
        "strategic planning",
        "budget management"
    ],
    "recommendations": [
        "Add more industry-specific keywords relevant to the job description",
        "Shorten bullet points to 1-2 lines for better readability",
        "Include a skills section with both technical and soft skills",
        "Quantify more achievements with specific metrics and results",
        "Ensure consistent date formatting throughout the resume"
    ],
    "format_tips": [
        "Use consistent font sizes for section headers",
        "Maintain standard margins throughout the document",
        "Ensure proper spacing between sections",
        "Use bullet points consistently for better readability"
    ]
}