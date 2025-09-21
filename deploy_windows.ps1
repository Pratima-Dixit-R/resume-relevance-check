# Windows PowerShell Deployment Script for Resume Relevance Check
# Python 3.13.7 on Windows - Pratima-Dixit-R
# Project: https://github.com/Pratima-Dixit-R/resume-relevance-check

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Windows PowerShell Deployment - Resume Relevance Check" -ForegroundColor Cyan
Write-Host "Python 3.13.7 Environment Setup" -ForegroundColor Cyan
Write-Host "User: Pratima-Dixit-R" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Set error action preference
$ErrorActionPreference = "Stop"

try {
    # Check Python version
    Write-Host "Checking Python version..." -ForegroundColor Yellow
    $pythonVersion = python --version
    Write-Host $pythonVersion -ForegroundColor Green
    
    # Create virtual environment
    Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
    if (Test-Path "venv") {
        Write-Host "Virtual environment already exists" -ForegroundColor Green
    } else {
        python -m venv venv
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    
    # Upgrade pip
    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    
    # Install dependencies
    Write-Host "Installing project dependencies..." -ForegroundColor Yellow
    pip install -r "src\backend\requirements.txt"
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
    
    # Create necessary directories
    Write-Host "Creating necessary directories..." -ForegroundColor Yellow
    $directories = @("data", "data\temp", "data\uploads", "logs")
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "Created directory: $dir" -ForegroundColor Green
        }
    }
    
    # Set up environment configuration
    Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
    if (!(Test-Path ".env")) {
        $envContent = @"
DEBUG=True
DATABASE_URI=sqlite:///resume_relevance_check.db
SECRET_KEY=windows_deployment_secret_key_2025
MAX_CONTENT_LENGTH=16777216
EMBEDDING_MODEL=all-MiniLM-L6-v2
API_KEY=your_api_key_here
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "Created .env configuration file" -ForegroundColor Green
    }
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Deployment completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. To start the Streamlit dashboard:" -ForegroundColor White
    Write-Host "   python -m streamlit run src\dashboard\streamlit_app.py --server.port 8501" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. To start the FastAPI backend:" -ForegroundColor White
    Write-Host "   python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. Access the application:" -ForegroundColor White
    Write-Host "   - Dashboard: http://localhost:8501" -ForegroundColor Cyan
    Write-Host "   - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Virtual environment is activated. Ready to run!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    
} catch {
    Write-Host "ERROR: Deployment failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "Please check the error above and try again." -ForegroundColor Yellow
    exit 1
}

# Keep PowerShell window open
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")