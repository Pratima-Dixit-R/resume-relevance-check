# Resume AI Analyzer - Deployment Automation Script
# This script automates the deployment process for the Resume AI Analyzer app

Write-Host "🚀 Resume AI Analyzer - Deployment Automation" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Function to check if required tools are installed
function Check-Prerequisites {
    Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
    
    # Check Git
    try {
        $gitVersion = git --version
        Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
        exit 1
    }
    
    # Check Python
    try {
        $pythonVersion = python --version
        Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python is not installed. Please install Python first." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ All prerequisites satisfied!" -ForegroundColor Green
}

# Function to update and commit changes
function Update-Repository {
    Write-Host "🔄 Updating repository..." -ForegroundColor Yellow
    
    # Add all changes
    git add .
    
    # Check if there are changes to commit
    $status = git status --porcelain
    if ($status) {
        # Commit changes
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "Automated deployment: $timestamp"
        
        # Push to GitHub
        Write-Host "📤 Pushing changes to GitHub..." -ForegroundColor Yellow
        git push origin main
        
        Write-Host "✅ Changes pushed to GitHub successfully!" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  No changes to commit." -ForegroundColor Blue
    }
}

# Function to check Streamlit Cloud deployment status
function Check-DeploymentStatus {
    Write-Host "🌐 Checking deployment status..." -ForegroundColor Yellow
    Write-Host "Please visit https://streamlit.io/cloud to check your app deployment status." -ForegroundColor Cyan
    Write-Host "Your app will be available at: https://resume-relevance-check.streamlit.app" -ForegroundColor Cyan
}

# Function to open browser with the app
function Open-AppInBrowser {
    Write-Host "🖥️  Opening app in browser..." -ForegroundColor Yellow
    Start-Process "https://resume-relevance-check.streamlit.app"
}

# Main execution
try {
    # Check prerequisites
    Check-Prerequisites
    
    # Update repository
    Update-Repository
    
    # Check deployment status
    Check-DeploymentStatus
    
    # Ask user if they want to open the app
    $openBrowser = Read-Host "Do you want to open the app in your browser? (y/n)"
    if ($openBrowser -eq 'y' -or $openBrowser -eq 'Y') {
        Open-AppInBrowser
    }
    
    Write-Host "🎉 Deployment automation completed!" -ForegroundColor Green
    Write-Host "📝 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Configure your custom domain DNS settings" -ForegroundColor Yellow
    Write-Host "   2. Add your domain in Streamlit Cloud settings" -ForegroundColor Yellow
    Write-Host "   3. Wait for SSL certificate provisioning" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ An error occurred: $_" -ForegroundColor Red
    exit 1
}