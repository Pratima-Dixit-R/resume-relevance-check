# Resume Relevance Checker - Streamlit Cloud Deployment

This is a simplified version of the Resume Relevance Checker optimized for deployment on Streamlit Cloud.

## 🚀 Deployment Instructions

1. **Fork this repository** to your GitHub account
2. **Sign in to Streamlit Cloud** at https://share.streamlit.io/
3. **Click "New app"** and connect to your GitHub repository
4. **Set the following options**:
   - **Repository**: Your forked repository
   - **Branch**: main (or master)
   - **Main file path**: `resume_analyzer.py`
5. **Click "Deploy!"**

## 📁 File Structure for Streamlit Cloud

```
├── resume_analyzer.py          # Main Streamlit app
├── requirements_streamlit.txt  # Dependencies for Streamlit Cloud
└── README_STREAMLIT.md         # This file
```

## 🛠️ Dependencies

The app uses only essential dependencies for Streamlit Cloud:
- `streamlit` - For the web interface
- `plotly` - For data visualization
- `scikit-learn` - For TF-IDF vectorization
- `numpy` - For numerical computations
- `pandas` - For data handling
- `PyPDF2` - For PDF text extraction
- `python-docx` - For DOCX text extraction

## 🎯 Features

- **File Upload**: Supports PDF, DOCX, and TXT files
- **Hard Match Analysis**: Keyword matching between resume and job description
- **Semantic Analysis**: TF-IDF based similarity scoring
- **Visual Results**: Interactive charts and score breakdowns
- **History Tracking**: Analysis history within the session

## 🔒 Privacy Notice

All processing happens in real-time and no data is stored on any servers. Files are processed in-memory and discarded after analysis.

## 🆘 Troubleshooting

If you encounter issues:
1. Ensure all dependencies are correctly specified in `requirements_streamlit.txt`
2. Check that the main file is `resume_analyzer.py`
3. Make sure your GitHub repository is public or you've granted appropriate permissions

## 📞 Support

For issues with the deployment, please open an issue in the GitHub repository.