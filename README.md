# Resume Relevance Check Application

A comprehensive application for analyzing resume relevance against job descriptions using both hard skill matching and semantic similarity analysis.

## 🚀 Features

- **Dual Analysis Engine**: Combines hard skill matching with semantic similarity analysis
- **Multiple File Formats**: Supports PDF and DOCX file uploads
- **Interactive Dashboard**: User-friendly Streamlit interface for file uploads and result visualization
- **REST API**: FastAPI backend for programmatic access
- **Database Storage**: SQLAlchemy-based storage for evaluation results
- **Detailed Scoring**: Provides breakdown of hard match, semantic match, and final scores

## 🏗️ Architecture

```
resume-relevance-check/
├── src/
│   ├── api/                 # FastAPI backend
│   │   ├── main.py         # FastAPI application entry point
│   │   └── endpoints.py    # API route definitions
│   ├── dashboard/          # Streamlit frontend
│   │   └── streamlit_app.py # Interactive web dashboard
│   ├── parsing/            # Document parsing modules
│   │   ├── resume_parser.py # Resume text extraction and parsing
│   │   └── jd_parser.py    # Job description parsing
│   ├── scoring/            # Relevance scoring algorithms
│   │   ├── hard_match.py   # Exact skill matching
│   │   ├── semantic_match.py # TF-IDF based semantic similarity
│   │   └── verdict.py      # Final scoring and verdict logic
│   ├── storage/            # Database management
│   │   └── database.py     # SQLAlchemy models and operations
│   └── utils/              # Utility functions
│       └── text_extraction.py # PDF/DOCX text extraction
├── data/                   # Sample data files
├── config.py              # Application configuration
└── requirements.txt       # Python dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Git (configured with your credentials)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd resume-relevance-check
   ```

2. **Install dependencies**:
   ```bash
   pip install -r src/backend/requirements.txt
   ```

3. **Configure environment** (optional):
   ```bash
   # Edit .env file with your configurations
   DATABASE_URL=sqlite:///resume_relevance_check.db
   SECRET_KEY=your_secret_key_here
   ```

## 🚀 Running the Application

### Option 1: Interactive Dashboard (Recommended)

```bash
# Start the Streamlit dashboard
python -m streamlit run src/dashboard/streamlit_app.py --server.port 8501
```

Access the dashboard at: http://localhost:8501

### Option 2: FastAPI Backend

```bash
# Start the FastAPI server
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation available at: http://localhost:8000/docs

### Option 3: Both Services

Run both services simultaneously for full functionality:

```bash
# Terminal 1: Start FastAPI backend
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start Streamlit dashboard
python -m streamlit run src/dashboard/streamlit_app.py --server.port 8501
```

## 📖 Usage

### Using the Streamlit Dashboard

1. **Upload Job Description**: Upload a PDF or DOCX file containing the job description
2. **Process Job Description**: Click to extract and analyze the job requirements
3. **Upload Resume**: Upload a PDF or DOCX resume file
4. **Process Resume**: Click to extract resume content and skills
5. **Evaluate Match**: Get detailed scoring including:
   - Hard Match Score (exact skill matching)
   - Semantic Match Score (contextual similarity)
   - Combined Final Score
   - Verdict (High/Medium/Low)

### Using the REST API

#### Upload and Parse Resume
```bash
curl -X POST "http://localhost:8000/upload_resume/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/resume.pdf"
```

#### Upload and Parse Job Description
```bash
curl -X POST "http://localhost:8000/upload_jd/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/job_description.pdf"
```

#### Evaluate Match
```bash
curl -X POST "http://localhost:8000/evaluate/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "resume_text=<resume_content>&jd_text=<jd_content>"
```

#### Get Evaluation Results
```bash
curl -X GET "http://localhost:8000/evaluations/"
```

## 🧮 Scoring Algorithm

The application uses a two-pronged approach to evaluate resume relevance:

### 1. Hard Match Score (60% weight)
- Exact keyword matching for technical skills
- Fuzzy matching using sequence similarity
- Skills extracted from predefined keyword lists
- Covers technologies, frameworks, tools, and soft skills

### 2. Semantic Match Score (40% weight)
- TF-IDF vectorization of resume and job description texts
- Cosine similarity calculation between document vectors
- Captures contextual and semantic relationships
- Accounts for similar concepts expressed differently

### Final Verdict
- **High** (≥80%): Excellent match with strong alignment
- **Medium** (50-79%): Good match with some gaps
- **Low** (<50%): Limited match with significant gaps

## 📊 Database Schema

The application stores evaluation results in an SQLite database:

```sql
CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY,
    resume_id VARCHAR,
    job_id VARCHAR,
    relevance_score INTEGER,
    missing_elements TEXT,
    verdict VARCHAR
);
```

## 🔧 Configuration

Key configuration options in `config.py`:

- `DEBUG`: Enable/disable debug mode
- `DATABASE_URI`: Database connection string
- `ALLOWED_EXTENSIONS`: Supported file formats
- `MAX_CONTENT_LENGTH`: Maximum upload file size (16MB)
- `EMBEDDING_MODEL`: Model for semantic analysis

## 🧪 Testing

Sample files are provided in the `data/` directory:
- `data/sample_jds/`: Sample job descriptions
- `data/data/sample_resumes/`: Sample resume files

Use these files to test the application functionality.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 Git Configuration

The repository is configured with:
- **User**: Pratima-Dixit-R
- **Email**: pratimadixit2305@gmail.com
- **Branch**: main

All changes are committed and the working tree is clean.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r src/backend/requirements.txt`
2. **File Upload Issues**: Check file format (PDF/DOCX only) and size limits
3. **Port Conflicts**: Use different ports if 8000 or 8501 are already in use
4. **Database Issues**: Delete the SQLite file to reset the database

### Git Path Issues on Windows

If Git commands fail, the application uses the local Git installation at:
```
%LOCALAPPDATA%\Programs\Git\cmd\git.exe
```

## 📄 License

This project is open source and available under the MIT License.

## 🚀 Future Enhancements

- [ ] Advanced NLP models for better semantic matching
- [ ] Support for additional file formats
- [ ] User authentication and session management
- [ ] Advanced reporting and analytics
- [ ] Integration with job boards and HR systems
- [ ] Machine learning model training on historical data

---

**Author**: Pratima Dixit R  
**Email**: pratimadixit2305@gmail.com  
**Status**: ✅ Fully functional and tested