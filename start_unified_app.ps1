# Resume Relevance Checker - Unified Launcher
# Innomatics Research Labs
# Windows PowerShell Script

Write-Host "=" -repeat 60 -ForegroundColor Blue
Write-Host "🏆 INNOMATICS RESEARCH LABS" -ForegroundColor Yellow
Write-Host "📊 RESUME RELEVANCE CHECKER - UNIFIED LAUNCHER" -ForegroundColor Green
Write-Host "=" -repeat 60 -ForegroundColor Blue
Write-Host ""

# Set working directory
$WorkDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $WorkDir

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please run setup first or check if venv exists" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Check if ports are available
Write-Host "🔍 Checking port availability..." -ForegroundColor Cyan

$FastAPIPort = 8000
$StreamlitPort = 8501

# Function to check if port is in use
function Test-Port {
    param($Port)
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $false
    }
    catch {
        return $true
    }
}

if (Test-Port $FastAPIPort) {
    Write-Host "⚠️ Port $FastAPIPort is already in use. Trying to stop existing process..." -ForegroundColor Yellow
    Get-Process | Where-Object {$_.ProcessName -like "*uvicorn*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

if (Test-Port $StreamlitPort) {
    Write-Host "⚠️ Port $StreamlitPort is already in use. Trying to stop existing process..." -ForegroundColor Yellow
    Get-Process | Where-Object {$_.ProcessName -like "*streamlit*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

Write-Host "✅ Ports are ready" -ForegroundColor Green

# Launch unified application
Write-Host ""
Write-Host "🚀 Launching Resume Relevance Checker..." -ForegroundColor Green
Write-Host "🤖 AI Technologies: Ollama 3, LangChain, Hugging Face, spaCy" -ForegroundColor Magenta
Write-Host "📋 Features: 1-100 Scoring, Sample Data, Multi-model Analysis" -ForegroundColor Magenta
Write-Host ""

try {
    # Start the unified launcher
    python unified_launcher.py
}
catch {
    Write-Host "❌ Error launching application: $_" -ForegroundColor Red
    Write-Host "Please check the logs above for details" -ForegroundColor Yellow
}
finally {
    Write-Host ""
    Write-Host "🛑 Application stopped" -ForegroundColor Yellow
    Write-Host "Thank you for using Resume Relevance Checker!" -ForegroundColor Blue
    Read-Host "Press Enter to exit"
}