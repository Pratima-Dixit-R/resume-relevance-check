# Resume AI Analyzer - Access Instructions

## How to Launch the Application

To launch the Resume AI Analyzer with proper HTTPS access and custom domain support, follow these steps:

### 1. Launch the Application

```bash
python launch_with_https_and_git.py
```

This script will:
- Start the FastAPI backend on port 8000
- Start the Streamlit frontend on port 8501
- Create HTTPS tunnels for public access
- Push all changes to GitHub

### 2. Access the Application

#### Local Access:
- Streamlit Dashboard: http://localhost:8501
- FastAPI Backend: http://localhost:8000
- FastAPI Documentation: http://localhost:8000/docs

#### Network Access:
- Streamlit Dashboard: http://YOUR_LOCAL_IP:8501
- FastAPI Backend: http://YOUR_LOCAL_IP:8000

#### Public HTTPS Access:
After launching, you'll see a public HTTPS URL in the terminal output that looks like:
```
https://abc123.loca.lt
```

### 3. Custom Domain Mapping

To use your custom domain `https://www.resumeaianalyzer.com`:

1. **Option 1: Direct Access**
   - Use the public HTTPS URL provided in the terminal output
   - Share this URL with anyone who needs access

2. **Option 2: Domain Mapping**
   - Point your domain's DNS to the public URL
   - Or use a reverse proxy service to forward traffic

### 4. Git Integration

All changes are automatically pushed to your GitHub repository:
- Repository: https://github.com/Pratima-Dixit-R/resume-relevance-check
- Branch: main

### 5. Troubleshooting

#### If HTTPS tunnels fail:
1. Make sure Node.js and npm are installed
2. Install localtunnel: `npm install -g localtunnel`
3. Try manual tunnel creation:
   ```bash
   npx localtunnel --port 8501
   ```

#### If ports are in use:
The script automatically kills processes on ports 8000 and 8501

#### If git push fails:
1. Check your internet connection
2. Verify GitHub credentials
3. Ensure the repository exists and you have write access

## Services Overview

- **Frontend**: Streamlit application for user interface
- **Backend**: FastAPI application for API endpoints
- **Authentication**: JWT-based user authentication
- **AI Analysis**: Resume-JD matching algorithms
- **Database**: SQLite for data storage

## Next Steps

1. Access the application using one of the URLs above
2. Register a new account or login
3. Upload your resume and job description
4. Click 'Start AI Analysis' to get results
5. View detailed analysis and visualizations

For any issues, check the terminal output for error messages and troubleshooting tips.