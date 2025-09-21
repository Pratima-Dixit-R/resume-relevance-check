# Quick Start Script for Resume Relevance Check
# Windows PowerShell - Python 3.13.7
# User: Pratima-Dixit-R

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Resume Relevance Check - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "Choose an option:" -ForegroundColor Yellow
Write-Host "1. Start Streamlit Dashboard (Port 8501)" -ForegroundColor White
Write-Host "2. Start FastAPI Backend (Port 8000)" -ForegroundColor White
Write-Host "3. Start Both Services" -ForegroundColor White
Write-Host "4. Install/Update Dependencies" -ForegroundColor White
Write-Host "5. Run Tests" -ForegroundColor White
Write-Host "6. Exit" -ForegroundColor White

$choice = Read-Host "Enter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "Starting Streamlit Dashboard..." -ForegroundColor Green
        Write-Host "Access at: http://localhost:8501" -ForegroundColor Cyan
        python -m streamlit run src\dashboard\streamlit_app.py --server.port 8501
    }
    "2" {
        Write-Host "Starting FastAPI Backend..." -ForegroundColor Green
        Write-Host "Access at: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API Docs at: http://localhost:8000/docs" -ForegroundColor Cyan
        python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
    }
    "3" {
        Write-Host "Starting both services..." -ForegroundColor Green
        Write-Host "Dashboard: http://localhost:8501" -ForegroundColor Cyan
        Write-Host "API: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "Opening two PowerShell windows..." -ForegroundColor Yellow
        
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python -m streamlit run src\dashboard\streamlit_app.py --server.port 8501"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000"
        
        Write-Host "Both services started in separate windows!" -ForegroundColor Green
    }
    "4" {
        Write-Host "Installing/Updating dependencies..." -ForegroundColor Green
        python -m pip install --upgrade pip
        pip install -r src\backend\requirements.txt
        Write-Host "Dependencies updated successfully!" -ForegroundColor Green
    }
    "5" {
        Write-Host "Running tests..." -ForegroundColor Green
        python -m pytest
    }
    "6" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
    }
}

Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")