@echo off
cd /d "c:\Users\prati\.vscode\resume-relevance-check"

echo === Resume Relevance Check - Git Setup ===
echo.

:: Set Git path
set "GIT_PATH=%LOCALAPPDATA%\Programs\Git\cmd\git.exe"

echo Checking Git installation...
"%GIT_PATH%" --version
if errorlevel 1 (
    echo Error: Git not found. Please install Git first.
    pause
    exit /b 1
)

echo.
echo Current directory: %CD%
echo.

echo === Current Git Status ===
"%GIT_PATH%" status

echo.
echo === Adding all files ===
"%GIT_PATH%" add .

echo.
echo === Committing changes ===
"%GIT_PATH%" commit -m "Final commit with all enhancements ready for GitHub"

echo.
echo === Current branches ===
"%GIT_PATH%" branch -a

echo.
echo === Recent commits ===
"%GIT_PATH%" log --oneline -3

echo.
echo === Git Setup Complete ===
echo.
echo Next steps to push to GitHub:
echo 1. Go to https://github.com/new
echo 2. Create repository named: resume-relevance-check
echo 3. Copy these commands to run:
echo.
echo    "%GIT_PATH%" remote add origin https://github.com/Pratima-Dixit-R/resume-relevance-check.git
echo    "%GIT_PATH%" push -u origin main
echo.
echo IMPORTANT: Use a Personal Access Token instead of your password when prompted
echo.
pause