# 🎯 Qoder IDE Implementation Guide
# Resume Relevance Check Application

## 🔧 Quick Setup in Qoder IDE

### 1. Git Integration (Already Configured ✅)
- Qoder IDE automatically detects your `.git` repository
- Access Git operations through the Source Control panel
- Current branch: main
- Remote: https://github.com/Pratima-Dixit-R/resume-relevance-check.git

### 2. Project Structure Overview
```
resume-relevance-check/
├── 🤖 AI Backend (FastAPI)
│   ├── src/api/main.py          # FastAPI entry point
│   └── src/api/endpoints.py     # REST API endpoints
├── 🎨 Frontend (Streamlit)
│   └── src/dashboard/streamlit_app.py  # Interactive dashboard
├── 🧠 AI Components
│   ├── src/parsing/             # Document parsing
│   ├── src/scoring/             # AI scoring algorithms
│   └── src/utils/embeddings.py # Hugging Face integration
├── 💾 Database
│   └── src/storage/database.py # SQLAlchemy models
└── 📦 Dependencies
    └── requirements.txt         # Python packages
```

## 🚀 Running in Qoder IDE

### Option 1: Using Qoder's Integrated Terminal

#### Start FastAPI Backend:
```bash
# Terminal 1
cd \"c:\\Users\\prati\\.vscode\\resume-relevance-check\"
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

#### Start Streamlit Dashboard:
```bash
# Terminal 2 (New Terminal)
cd \"c:\\Users\\prati\\.vscode\\resume-relevance-check\"
python -m streamlit run src/dashboard/streamlit_app.py --server.port 8501
```

### Option 2: Using Qoder's Run Configurations

#### Create FastAPI Run Configuration:
1. Open Qoder's Run/Debug panel
2. Create new configuration:
   - **Name**: \"FastAPI Backend\"
   - **Type**: Python Module
   - **Module**: `uvicorn`
   - **Parameters**: `src.api.main:app --reload --host 127.0.0.1 --port 8000`
   - **Working Directory**: `c:\\Users\\prati\\.vscode\\resume-relevance-check`

#### Create Streamlit Run Configuration:
1. Create another configuration:
   - **Name**: \"Streamlit Dashboard\"
   - **Type**: Python Module
   - **Module**: `streamlit`
   - **Parameters**: `run src/dashboard/streamlit_app.py --server.port 8501`
   - **Working Directory**: `c:\\Users\\prati\\.vscode\\resume-relevance-check`

## 🌐 Access URLs

- **FastAPI API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Streamlit Dashboard**: http://localhost:8501
- **Qoder Preview**: Use built-in browser preview

## 🔧 Qoder IDE Specific Features

### 1. Integrated Git Operations
- **Commit**: Use Source Control panel → Stage changes → Write commit message → Commit
- **Push**: Click sync/push button in Source Control panel
- **Branch**: Create branches through Git panel

### 2. Debugging Support
- Set breakpoints in Python files
- Use Qoder's built-in debugger
- Debug both FastAPI and Streamlit components

### 3. Extensions/Plugins
Enable these Qoder extensions for better development:
- **Python Language Server**
- **Git Integration** (should be built-in)
- **REST Client** (for API testing)
- **JSON/YAML Support**

### 4. Environment Management
- Use Qoder's Python interpreter settings
- Configure virtual environments if needed
- Set environment variables in run configurations

## 📦 Dependencies Installation

### Using Qoder's Terminal:
```bash
cd \"c:\\Users\\prati\\.vscode\\resume-relevance-check\"
pip install -r requirements.txt
```

### Using Qoder's Package Manager (if available):
- Open Qoder's Python package manager
- Install from requirements.txt
- Or install packages individually through UI

## 🚀 Deployment from Qoder IDE

### 1. GitHub Integration
- Qoder should detect your GitHub remote automatically
- Use Source Control panel to push changes
- View repository: https://github.com/Pratima-Dixit-R/resume-relevance-check

### 2. Cloud Deployment (Optional)
If Qoder supports cloud deployment:
- Look for Deploy/Cloud integration panels
- Configure cloud providers (Heroku, Vercel, etc.)
- Deploy directly from IDE

## 🔍 Testing in Qoder IDE

### 1. Unit Testing
- Run tests using Qoder's test runner
- View test results in integrated panel

### 2. API Testing
- Use Qoder's REST client to test API endpoints
- Test file uploads and analysis features

### 3. Live Preview
- Use Qoder's built-in browser for live preview
- Test Streamlit dashboard interactively

## 🛠️ Troubleshooting in Qoder IDE

### Common Issues:
1. **Import Errors**: Check Python interpreter settings
2. **Port Conflicts**: Use different ports in run configurations
3. **Git Issues**: Use Qoder's Git panel instead of terminal
4. **Package Issues**: Reinstall dependencies through Qoder

### Qoder-Specific Solutions:
- Check Qoder's Output/Problems panel for errors
- Use integrated terminal for debugging
- Restart Qoder IDE if issues persist

## 📱 Quick Start Checklist

- ✅ Repository detected by Qoder IDE
- ✅ Python interpreter configured
- ✅ Dependencies installed
- ⏳ Create run configurations
- ⏳ Start both services
- ⏳ Test functionality
- ⏳ Push to GitHub using Qoder's Git panel

## 🎉 Success Indicators

- FastAPI backend responds at http://127.0.0.1:8000/docs
- Streamlit dashboard loads at http://localhost:8501
- File uploads work in dashboard
- AI analysis produces results
- Database stores evaluation results
- Git operations work through Qoder's UI

---

**Your Resume Relevance Check application is ready to run in Qoder IDE! 🚀**

Use the integrated features for a seamless development experience.