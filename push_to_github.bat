cd "c:\Users\prati\.vscode\resume-relevance-check"
@echo cd "c:\Users\prati\.vscode\resume-relevance-check"
push_to_github.bat
cd /d "c:\Users\prati\.vscode\resume-relevance-check"

echo === GitHub Push Script ===
echo Pushing to: https://github.com/Pratima-Dixit-R/resume-relevance-check.git
echo.

echo Checking Git status...
git status --porcelain

echo.
echo Checking remote configuration...
git remote -v

echo.
echo Attempting to push to GitHub...
echo IMPORTANT: When prompted for credentials:
echo   Username: Pratima-Dixit-R
echo   Password: Use your Personal Access Token (NOT your GitHub password)
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === SUCCESS ===
    echo Code successfully pushed to GitHub!
    echo Repository: https://github.com/Pratima-Dixit-R/resume-relevance-check
    echo.
    echo You can now view your repository at:
    echo https://github.com/Pratima-Dixit-R/resume-relevance-check
) else (
    echo.
    echo === FAILED ===
    echo Push failed. Please check:
    echo 1. Repository exists on GitHub
    echo 2. Using correct Personal Access Token
    echo 3. Internet connection is stable
)

echo.
pause