#!/usr/bin/env python3
"""
Git Deployment Script for Qoder IDE
Handles all Git operations with error handling
"""
import subprocess
import os
import sys

def run_git_command(command, description):
    """Run a git command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=r"c:\Users\prati\.vscode\resume-relevance-check"
        )
        
        if result.returncode == 0:
            print(f"✅ {description} successful!")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️ {description} warning/error:")
            print(f"   {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def deploy_to_github():
    """Complete deployment process"""
    print("🚀 Starting Git Deployment Process")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(r"c:\Users\prati\.vscode\resume-relevance-check")
    
    # Check git status
    print("📋 Checking Git status...")
    status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if status_result.stdout.strip():
        print("📝 Files to commit found:")
        print(status_result.stdout)
    else:
        print("ℹ️ No new changes detected")
    
    # Stage all files
    success1 = run_git_command("git add .", "Staging all files")
    
    # Create commit
    commit_message = """🚀 Complete Qoder IDE deployment - AI Resume Analysis App

✅ Full application deployed:
- FastAPI backend with AI-powered analysis
- Streamlit dashboard with interactive charts  
- Hugging Face transformers integration
- SQLAlchemy database with evaluation storage
- PDF parsing and resume relevance scoring
- Complete Qoder IDE configuration

🔧 Configuration files:
- .vscode/launch.json (Run configurations)
- qoder.json (IDE project settings)
- qoder_setup.py (Automated setup script)
- deploy_complete.bat (Deployment automation)

🌐 Ready URLs:
- API: http://127.0.0.1:8000
- Dashboard: http://localhost:8501  
- API Docs: http://127.0.0.1:8000/docs

Production-ready AI resume analysis application! 🎉"""

    success2 = run_git_command(f'git commit -m "{commit_message}"', "Creating commit")
    
    # Push to GitHub
    success3 = run_git_command("git push origin main", "Pushing to GitHub")
    
    # Verify deployment
    print("\n🔍 Verifying deployment...")
    log_result = subprocess.run("git log --oneline -3", shell=True, capture_output=True, text=True)
    if log_result.returncode == 0:
        print("📜 Recent commits:")
        print(log_result.stdout)
    
    # Final status
    print("\n" + "=" * 50)
    if success1 and success2 and success3:
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("✅ Your Resume Relevance Check app is now on GitHub!")
        print("🔗 Repository: https://github.com/Pratima-Dixit-R/resume-relevance-check")
    else:
        print("⚠️ Deployment completed with some warnings")
        print("Check the output above for details")
    
    print("\n🌐 Application Access URLs:")
    print("   • FastAPI API: http://127.0.0.1:8000")
    print("   • API Documentation: http://127.0.0.1:8000/docs") 
    print("   • Streamlit Dashboard: http://localhost:8501")
    print("\n🎯 Ready for AI-powered resume analysis!")

if __name__ == "__main__":
    deploy_to_github()