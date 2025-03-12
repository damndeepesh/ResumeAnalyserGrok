# Resume ATS Scoring Application

An advanced NLP-based Resume ATS (Applicant Tracking System) scoring application built with Streamlit. This application helps users evaluate and improve their resumes for specific job roles.

## Features

- **Resume Analysis**: Upload your resume and get an ATS compatibility score
- **Job Role Matching**: Specify your target job role for tailored analysis
- **Visualization**: View detailed graphs and charts of your resume's performance
- **Word Cloud**: Visual representation of key terms in your resume
- **History Comparison**: Compare previous resume versions to track improvements
- **Advanced NLP**: Powered by Groq API for sophisticated natural language processing

## Setup

### Prerequisites

- Python 3.8+
- Groq API key

### Installation

1. Clone this repository
2. Create and activate the virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```
   streamlit run app.py
   ```

## Project Structure

```
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (not tracked by git)
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── src/                    # Source code
    ├── __init__.py         # Package initialization
    ├── analyzer.py         # Resume analysis logic
    ├── groq_client.py      # Groq API integration
    ├── utils.py            # Utility functions
    ├── visualization.py    # Data visualization components
    └── pages/              # Streamlit pages
        ├── __init__.py     # Package initialization
        ├── home.py         # Home page
        ├── analysis.py     # Analysis page
        ├── visualization.py # Visualization page
        └── history.py      # History comparison page
```

## Usage

1. Navigate to the home page
2. Upload your resume (PDF, DOCX, or TXT format)
3. Enter your target job role
4. View your ATS score and detailed analysis
5. Explore visualizations and recommendations
6. Save your results for future comparison

## License

Apache-2.0 license
