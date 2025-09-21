# Git Setup Script for Resume Relevance Check
# Navigate to project directory
Set-Location "c:\Users\prati\.vscode\resume-relevance-check"

# Set Git path
$gitPath = "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe"

Write-Host "=== Git Configuration Status ===" -ForegroundColor Green

# Check current Git status
Write-Host "`nChecking Git status..." -ForegroundColor Yellow
& $gitPath status

# Check current remotes
Write-Host "`nChecking Git remotes..." -ForegroundColor Yellow
& $gitPath remote -v

# Check recent commits
Write-Host "`nRecent commits:" -ForegroundColor Yellow
& $gitPath log --oneline -5

# Add all changes
Write-Host "`nAdding all changes..." -ForegroundColor Yellow
& $gitPath add .

# Commit if there are changes
Write-Host "`nCommitting changes..." -ForegroundColor Yellow
& $gitPath commit -m "Final commit before GitHub push with all enhancements"

Write-Host "`n=== Ready for GitHub Setup ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create repository on GitHub: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: resume-relevance-check" -ForegroundColor White
Write-Host "3. Run: git remote add origin https://github.com/Pratima-Dixit-R/resume-relevance-check.git" -ForegroundColor White
Write-Host "4. Run: git push -u origin main" -ForegroundColor White
Write-Host "5. Use Personal Access Token when prompted for password" -ForegroundColor White