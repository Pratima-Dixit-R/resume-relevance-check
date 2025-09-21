# Windows Deployment Guide - Resume Relevance Check

## 🖥️ Windows Setup for Python 3.13.7

**Target Environment:**
- Windows 11/10
- Python 3.13.7
- User: Pratima-Dixit-R
- Repository: https://github.com/Pratima-Dixit-R/resume-relevance-check

## 🚀 Quick Start (Automated)

### Option 1: PowerShell Script (Recommended)
```powershell
# Run the automated deployment script
.\deploy_windows.ps1
```

### Option 2: Batch Script
```cmd
# Run the batch deployment script
deploy_windows.bat
```

### Option 3: Quick App Launcher
```powershell
# Use the quick start menu
.\start_app.ps1
```

## 📋 Manual Setup Steps

### Step 1: Clone Repository
```powershell
git clone https://github.com/Pratima-Dixit-R/resume-relevance-check.git
cd resume-relevance-check
```

### Step 2: Create Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r src\backend\requirements.txt
```

### Step 4: Create Environment Configuration
```powershell
# Create .env file (if not exists)
echo "DEBUG=True" > .env
echo "DATABASE_URI=sqlite:///resume_relevance_check.db" >> .env
echo "SECRET_KEY=windows_deployment_secret_key_2025" >> .env
echo "MAX_CONTENT_LENGTH=16777216" >> .env
echo "EMBEDDING_MODEL=all-MiniLM-L6-v2" >> .env
```

### Step 5: Create Necessary Directories
```powershell
mkdir data -Force
mkdir data\temp -Force
mkdir data\uploads -Force
mkdir logs -Force
```

## 🔧 Running the Application

### Streamlit Dashboard
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Start Streamlit dashboard
python -m streamlit run src\dashboard\streamlit_app.py --server.port 8501
```

**Access at:** http://localhost:8501

### FastAPI Backend
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Start FastAPI server
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

**Access at:** 
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Run Both Services Simultaneously
```powershell
# Use the quick start script for easy management
.\start_app.ps1
# Choose option 3 to start both services
```

## 🧪 Testing the Installation

### Test API Endpoints
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/
```

### Test Dashboard
- Open http://localhost:8501 in your browser
- Upload a test resume (PDF/DOCX)
- Upload a test job description
- Verify the matching functionality works

## 📁 Project Structure
```
resume-relevance-check/
├── src/
│   ├── api/                 # FastAPI backend
│   ├── dashboard/           # Streamlit frontend
│   ├── parsing/             # Document parsing
│   ├── scoring/             # Relevance scoring
│   ├── storage/             # Database management
│   └── utils/               # Utility functions
├── data/                    # Application data
├── logs/                    # Application logs
├── venv/                    # Python virtual environment
├── deploy_windows.ps1       # PowerShell deployment script
├── deploy_windows.bat       # Batch deployment script
├── start_app.ps1           # Quick start launcher
└── requirements.txt         # Python dependencies
```

## 🔍 Python 3.13.7 Compatibility Notes

### Updated Dependencies for Python 3.13:
- **NumPy**: Updated to >=1.26.0 for Python 3.13 support
- **Pandas**: Updated to >=2.2.0 for better compatibility
- **Scikit-learn**: Updated to >=1.4.0
- **Torch**: Updated to >=2.1.0
- **Transformers**: Updated to >=4.36.0

### Windows-Specific Optimizations:
- Added `colorama` for better terminal output
- Configured proper PowerShell execution policies
- Optimized for Windows file paths and directory structure

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### PowerShell Execution Policy Error
```powershell
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Virtual Environment Activation Issues
```powershell
# If activation fails, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

#### Dependency Installation Errors
```powershell
# Update pip and try again
python -m pip install --upgrade pip
pip install -r src\backend\requirements.txt --force-reinstall
```

#### Port Already in Use
```powershell
# Check what's using the port
netstat -ano | findstr :8501
netstat -ano | findstr :8000

# Kill the process if needed (replace PID with actual process ID)
taskkill /PID <process_id> /F
```

## 📊 Performance Optimization for Windows

### Recommended System Requirements:
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space for dependencies
- **CPU**: Multi-core processor for ML operations

### Performance Tips:
1. Use SSD storage for better I/O performance
2. Close unnecessary applications before running ML models
3. Consider using GPU acceleration for PyTorch operations
4. Monitor memory usage during large document processing

## 🔐 Security Configuration

### Environment Variables (.env):
```bash
DEBUG=False                    # Set to False for production
DATABASE_URI=sqlite:///app.db  # Use absolute path for production
SECRET_KEY=your_secure_key     # Generate a strong secret key
MAX_CONTENT_LENGTH=16777216    # 16MB file upload limit
```

### File Permissions:
- Ensure proper read/write permissions for data directory
- Restrict access to .env file containing sensitive information

## 📈 Monitoring and Logs

### Log Files:
- Application logs: `logs/app.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`

### Monitoring Commands:
```powershell
# Monitor application logs
Get-Content logs\app.log -Wait

# Check system resources
Get-Process python
```

## 🌐 GitHub Integration

### Repository Information:
- **Repository**: https://github.com/Pratima-Dixit-R/resume-relevance-check
- **User**: Pratima-Dixit-R
- **Email**: pratimadixit2305@gmail.com
- **Branch**: main

### Git Configuration:
```powershell
git config user.name "Pratima-Dixit-R"
git config user.email "pratimadixit2305@gmail.com"
git config core.autocrlf true  # Windows line endings
```

## ✅ Deployment Checklist

- [ ] Python 3.13.7 installed and accessible
- [ ] Git configured with proper credentials
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Environment configuration (.env) created
- [ ] Directory structure set up
- [ ] Streamlit dashboard accessible at port 8501
- [ ] FastAPI backend accessible at port 8000
- [ ] API documentation accessible at /docs
- [ ] Test files processed successfully
- [ ] Logs generated and accessible

---

**Deployment Status**: ✅ Ready for Windows Production Environment  
**Last Updated**: 2025-09-21  
**Python Version**: 3.13.7  
**User**: Pratima-Dixit-R