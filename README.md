# Resume Relevance Check System

This project aims to automate the evaluation of resumes against job descriptions, providing a scalable and consistent solution for the placement team at Innomatics Research Labs. The system generates a relevance score for each resume, highlights missing elements, and offers personalized feedback to students.

## Project Structure

```
resume-relevance-check
├── src
│   ├── app.py                  # Main entry point of the application
│   ├── api
│   │   ├── endpoints.py        # API endpoints for resume and JD uploads
│   │   └── __init__.py         # Initializes the API module
│   ├── parsing
│   │   ├── resume_parser.py     # Logic for parsing resumes
│   │   ├── jd_parser.py         # Logic for parsing job descriptions
│   │   └── __init__.py         # Initializes the parsing module
│   ├── scoring
│   │   ├── hard_match.py        # Hard matching logic for keywords
│   │   ├── semantic_match.py     # Semantic matching logic using embeddings
│   │   ├── verdict.py           # Determines final suitability verdict
│   │   └── __init__.py         # Initializes the scoring module
│   ├── feedback
│   │   ├── suggestions.py       # Generates feedback for students
│   │   └── __init__.py         # Initializes the feedback module
│   ├── storage
│   │   ├── database.py          # Manages database interactions
│   │   └── __init__.py         # Initializes the storage module
│   ├── dashboard
│   │   ├── streamlit_app.py     # Streamlit application for the dashboard
│   │   └── __init__.py         # Initializes the dashboard module
│   └── utils
│       ├── text_extraction.py   # Utility functions for text extraction
│       ├── embeddings.py         # Functions for managing embeddings
│       └── __init__.py         # Initializes the utils module
├── requirements.txt             # Lists project dependencies
├── README.md                    # Documentation for the project
├── config.py                    # Configuration settings
└── .env                         # Environment variables
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd resume-relevance-check
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file.

## Usage

1. Start the application:
   ```
   python src/app.py
   ```

2. Access the API endpoints to upload resumes and job descriptions.

3. Use the Streamlit dashboard to view evaluation results and feedback.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.