@echo off
:: GitHub Push Script for Resume Relevance Check
:: Based on user memory: Use .bat script for reliable Windows Git operations

echo ================================================
echo 🚀 PUSHING TO GITHUB - Resume Relevance Check
echo ================================================

:: Navigate to project directory
cd /d "c:\Users\prati\.vscode\resume-relevance-check"

:: Configure Git user (from memory)
echo 🔧 Configuring Git user...
git config user.name "Pratima-Dixit-R"
git config user.email "pratimadixit2305@gmail.com"

:: Check current status
echo 📋 Checking Git status...
git status

:: Check remote configuration
echo 🌐 Checking remote configuration...
git remote -v

:: Check if we need to add remote (from memory)
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Adding GitHub remote...
    git remote add origin https://github.com/Pratima-Dixit-R/resume-relevance-check.git
) else (
    echo ✅ Remote origin already configured
)

:: Final push to GitHub
echo 🚀 Pushing to GitHub...
git push -u origin main

:: Check final status
if errorlevel 0 (
    echo.
    echo ================================================
    echo 🎉 SUCCESS! Application pushed to GitHub!
    echo ================================================
    echo.
    echo 🔗 Repository URL: https://github.com/Pratima-Dixit-R/resume-relevance-check
    echo.
    echo ✅ Your fully functional Resume Relevance Check app is now on GitHub!
    echo.
    echo 🌐 Features deployed:
    echo    • FastAPI backend with AI analysis
    echo    • Streamlit dashboard with charts
    echo    • Hugging Face transformers integration
    echo    • SQLAlchemy database
    echo    • PDF processing capabilities
    echo    • Complete Qoder IDE configuration
    echo.
    echo 🎯 Ready for production use!
) else (
    echo.
    echo ❌ Push failed. Please check your GitHub credentials.
    echo 💡 You may need to use a Personal Access Token for authentication.
)

echo.
pause