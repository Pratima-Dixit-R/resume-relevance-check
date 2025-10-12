# Build script for Android
Write-Host "🚀 Building Resume AI Analyzer for Android" -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js first." -ForegroundColor Red
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm is not installed. Please install Node.js first." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

# Add Android platform if not already added
if (!(Test-Path -Path "android")) {
    Write-Host "📱 Adding Android platform..." -ForegroundColor Yellow
    npx cap add android
} else {
    Write-Host "✅ Android platform already added" -ForegroundColor Green
}

# Sync the project
Write-Host "🔄 Syncing project..." -ForegroundColor Yellow
npx cap sync

Write-Host "✅ Android build setup completed!" -ForegroundColor Green
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Open Android Studio" -ForegroundColor Yellow
Write-Host "   2. Open the android folder in this directory" -ForegroundColor Yellow
Write-Host "   3. Build the APK using Build > Build Bundle(s) / APK(s) > Build APK" -ForegroundColor Yellow