# Setup script for mobile app
Write-Host "🚀 Setting up mobile app for Resume AI Analyzer" -ForegroundColor Green

# Create mobile app directory if it doesn't exist
if (!(Test-Path -Path "mobile-app")) {
    Write-Host "📁 Creating mobile-app directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Name "mobile-app" | Out-Null
}

# Navigate to mobile app directory
Set-Location -Path "mobile-app"

# Create www directory if it doesn't exist
if (!(Test-Path -Path "www")) {
    Write-Host "📁 Creating www directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Name "www" | Out-Null
}

# Create index.html
Write-Host "📄 Creating index.html..." -ForegroundColor Yellow
@"
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Resume AI Analyzer</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #4ECDC4, #45B7D1);
        }
        .container {
            text-align: center;
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .logo {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        .title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
        }
        .redirect-text {
            font-size: 1rem;
            color: #666;
            margin-bottom: 1.5rem;
        }
        .button {
            background: #4ECDC4;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 1rem;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .button:hover {
            background: #45B7D1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📄</div>
        <div class="title">Resume AI Analyzer</div>
        <div class="redirect-text">Redirecting to the application...</div>
        <button class="button" onclick="openApp()">Open App</button>
    </div>

    <script>
        // Redirect to the hosted app after a short delay
        setTimeout(function() {
            window.location.href = 'https://resume-relevance-check.streamlit.app';
        }, 3000);

        function openApp() {
            window.location.href = 'https://resume-relevance-check.streamlit.app';
        }
    </script>
</body>
</html>
"@ | Out-File -FilePath "www\index.html" -Encoding UTF8

# Create capacitor.config.json
Write-Host "⚙️  Creating capacitor.config.json..." -ForegroundColor Yellow
@"
{
  "appId": "com.resumeaianalyzer.app",
  "appName": "Resume AI Analyzer",
  "webDir": "www",
  "bundledWebRuntime": false,
  "server": {
    "url": "https://resume-relevance-check.streamlit.app",
    "allowNavigation": [
      "resume-relevance-check.streamlit.app",
      "www.resumeaianalyzer.in"
    ]
  }
}
"@ | Out-File -FilePath "capacitor.config.json" -Encoding UTF8

Write-Host "✅ Mobile app setup completed!" -ForegroundColor Green
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Run 'npm install' in the mobile-app directory" -ForegroundColor Yellow
Write-Host "   2. Run 'npx cap add android' to add Android platform" -ForegroundColor Yellow
Write-Host "   3. Run 'npx cap open android' to open in Android Studio" -ForegroundColor Yellow