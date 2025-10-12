#!/usr/bin/env python3
"""
Simple launch script for Resume AI Analyzer.
This script launches the application and pushes changes to GitHub.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def start_services():
    """Start both FastAPI and Streamlit services."""
    print("🚀 Starting Resume AI Analyzer services...")
    
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    # Start FastAPI backend
    print("🔧 Starting FastAPI backend on port 8000...")
    fastapi_cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ]
    
    try:
        fastapi_process = subprocess.Popen(fastapi_cmd, 
                                         stdout=subprocess.DEVNULL, 
                                         stderr=subprocess.DEVNULL)
        print("✅ FastAPI backend started")
    except Exception as e:
        print(f"❌ Failed to start FastAPI: {e}")
        return None, None
    
    # Wait a moment
    time.sleep(3)
    
    # Start Streamlit frontend
    print("🎨 Starting Streamlit frontend on port 8501...")
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", 
        "run", "src/dashboard/streamlit_app.py", 
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    try:
        streamlit_process = subprocess.Popen(streamlit_cmd,
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
        print("✅ Streamlit frontend started")
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        fastapi_process.terminate()
        return None, None
    
    return fastapi_process, streamlit_process

def get_local_ip():
    """Get local IP address."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def push_to_github():
    """Push changes to GitHub."""
    print("🔄 Pushing changes to GitHub...")
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        # Check if there are changes to commit
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            # Commit changes
            subprocess.run(["git", "commit", "-m", "Fix application launch issues and prepare for deployment"], 
                          check=True, capture_output=True)
            
            # Push to GitHub
            subprocess.run(["git", "push", "origin", "main"], 
                          check=True, capture_output=True)
            print("✅ Changes pushed to GitHub successfully")
        else:
            print("✅ No changes to push")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function."""
    print("🤖 Resume AI Analyzer - Final Launch")
    print("=" * 40)
    
    # Start services
    fastapi_process, streamlit_process = start_services()
    
    if not fastapi_process or not streamlit_process:
        print("❌ Failed to start services")
        return
    
    # Wait for services to initialize
    time.sleep(5)
    
    # Show access information
    local_ip = get_local_ip()
    print("\n" + "="*50)
    print("🎉 APPLICATION LAUNCHED SUCCESSFULLY!")
    print("="*50)
    print("🌐 ACCESS URLS:")
    print(f"   Local Access: http://localhost:8501")
    print(f"   Network Access: http://{local_ip}:8501")
    print(f"   API Endpoint: http://localhost:8000")
    print(f"   API Network: http://{local_ip}:8000")
    print("\n📝 HOW TO USE:")
    print("   1. Open your browser and go to one of the URLs above")
    print("   2. Register a new account or login")
    print("   3. Upload resume and job description files")
    print("   4. Click 'Start AI Analysis'")
    print("   5. View results and visualizations")
    print("\n⚠️  Press Ctrl+C to stop services")
    print("="*50)
    
    # Push to GitHub
    push_to_github()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate processes
        for process in [fastapi_process, streamlit_process]:
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except:
                    try:
                        process.kill()
                    except:
                        pass
        
        print("✅ Services stopped successfully")

if __name__ == "__main__":
    main()