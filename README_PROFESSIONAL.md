# Professional AI Resume Analyzer - Streamlit Cloud Deployment

This is the professional version of the Resume Relevance Checker optimized for deployment on Streamlit Cloud with advanced AI analysis capabilities.

## 🚀 Deployment Instructions

1. **Fork this repository** to your GitHub account
2. **Sign in to Streamlit Cloud** at https://share.streamlit.io/
3. **Click "New app"** and connect to your GitHub repository
4. **Set the following options**:
   - **Repository**: Your forked repository
   - **Branch**: main (or master)
   - **Main file path**: `professional_resume_analyzer.py`
5. **Click "Deploy!"**

## 📁 File Structure for Streamlit Cloud

```
├── professional_resume_analyzer.py     # Main Streamlit app (Professional version)
├── requirements_professional.txt       # Dependencies for Professional version
└── README_PROFESSIONAL.md              # This file
```

## 🛠️ Dependencies

The app uses only essential dependencies for Streamlit Cloud:
- `streamlit` - For the web interface
- `plotly` - For data visualization
- `scikit-learn` - For TF-IDF vectorization and AI analysis
- `numpy` - For numerical computations
- `pandas` - For data handling
- `PyPDF2` - For PDF text extraction
- `python-docx` - For DOCX text extraction

## 🎯 Professional Features

- **Advanced AI Analysis**: Multi-dimensional analysis including keyword matching, semantic analysis, and skill matching
- **Professional Visualizations**: High-quality charts and graphs with zoom capabilities
- **Comprehensive Reporting**: Detailed analysis reports with executive summaries
- **Multi-Page Interface**: Organized navigation for different analysis functions
- **Export Capabilities**: Download analysis results in multiple formats (JSON, CSV, Text)
- **Responsive Design**: Works on all devices including mobile and desktop
- **File Upload**: Supports PDF, DOCX, and TXT files

## 🔒 Privacy Notice

All processing happens in real-time and no data is stored on any servers. Files are processed in-memory and discarded after analysis.

## 🆘 Troubleshooting

If you encounter issues:
1. Ensure all dependencies are correctly specified in `requirements_professional.txt`
2. Check that the main file is `professional_resume_analyzer.py`
3. Make sure your GitHub repository is public or you've granted appropriate permissions

## 📞 Support

For issues with the deployment, please open an issue in the GitHub repository.