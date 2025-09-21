@echo off
REM Windows Deployment Script for Resume Relevance Check
REM Python 3.13.7 on Windows - Pratima-Dixit-R
REM Project: https://github.com/Pratima-Dixit-R/resume-relevance-check

echo ========================================
echo Windows Deployment - Resume Relevance Check
echo Python 3.13.7 Environment Setup
echo User: Pratima-Dixit-R
echo ========================================

REM Check Python version
echo Checking Python version...
python --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found. Please install Python 3.13.7
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing project dependencies...
pip install -r src\backend\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create necessary directories
echo Creating necessary directories...
if not exist data mkdir data
if not exist data\temp mkdir data\temp
if not exist data\uploads mkdir data\uploads
if not exist logs mkdir logs

REM Set up environment variables
echo Setting up environment configuration...
if not exist .env (
    echo Creating .env configuration file...
    echo DEBUG=True > .env
    echo DATABASE_URI=sqlite:///resume_relevance_check.db >> .env
    echo SECRET_KEY=windows_deployment_secret_key_2025 >> .env
    echo MAX_CONTENT_LENGTH=16777216 >> .env
    echo EMBEDDING_MODEL=all-MiniLM-L6-v2 >> .env
)

echo ========================================
echo Deployment completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. To start the Streamlit dashboard:
echo    python -m streamlit run src\dashboard\streamlit_app.py --server.port 8501
echo.
echo 2. To start the FastAPI backend:
echo    python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
echo.
echo 3. Access the application:
echo    - Dashboard: http://localhost:8501
echo    - API Docs: http://localhost:8000/docs
echo.
echo Virtual environment is activated. Ready to run!
echo ========================================

pause