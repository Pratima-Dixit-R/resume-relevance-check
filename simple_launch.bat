@echo off
echo ========================================
echo RESUME AI ANALYZER - SIMPLE LAUNCH
echo ========================================
echo.
echo Starting FastAPI backend...
start "FastAPI Backend" /min cmd /c "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul
echo Starting Streamlit frontend...
start "Streamlit Frontend" /max cmd /c "streamlit run src/dashboard/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"
echo.
echo Application should be accessible at:
echo   Local: http://localhost:8501
echo   Network: http://10.60.159.5:8501
echo.
echo Press any key to stop services...
pause >nul
taskkill /F /FI "WINDOWTITLE eq FastAPI Backend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Streamlit Frontend*" >nul 2>&1
echo Services stopped.