#!/usr/bin/env python3
"""
Proper launch script for Resume AI Analyzer.
This script ensures both FastAPI and Streamlit start correctly.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def start_fastapi():
    """Start FastAPI backend service."""
    print("🔧 Starting FastAPI backend on port 8000...")
    
    # Change to the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    try:
        # Start FastAPI with proper error handling
        fastapi_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for it to start (up to 30 seconds)
        for i in range(30):
            try:
                response = requests.get("http://localhost:8000/health", timeout=1)
                if response.status_code == 200:
                    print("✅ FastAPI backend started successfully")
                    return fastapi_process
            except:
                pass
            time.sleep(1)
        
        # Check if process is still running
        if fastapi_process.poll() is None:
            print("✅ FastAPI backend process is running")
            return fastapi_process
        else:
            stdout, stderr = fastapi_process.communicate()
            print(f"❌ FastAPI failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI: {e}")
        return None

def start_streamlit():
    """Start Streamlit frontend service."""
    print("🎨 Starting Streamlit frontend on port 8501...")
    
    # Change to the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    try:
        # Start Streamlit with proper error handling
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", "src/dashboard/streamlit_app.py", 
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for it to start (up to 30 seconds)
        for i in range(30):
            try:
                response = requests.get("http://localhost:8501/healthz", timeout=1)
                if response.status_code == 200:
                    print("✅ Streamlit frontend started successfully")
                    return streamlit_process
            except:
                pass
            time.sleep(1)
        
        # Check if process is still running
        if streamlit_process.poll() is None:
            print("✅ Streamlit frontend process is running")
            return streamlit_process
        else:
            stdout, stderr = streamlit_process.communicate()
            print(f"❌ Streamlit failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        return None

def get_local_ip():
    """Get the local IP address."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    """Main function to launch everything."""
    print("🤖 Resume AI Analyzer - Proper Launch")
    print("=" * 40)
    
    # Start services
    fastapi_process = start_fastapi()
    if not fastapi_process:
        print("❌ Failed to start FastAPI backend")
        return
    
    time.sleep(3)  # Give FastAPI time to fully initialize
    
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit frontend")
        # Terminate FastAPI process
        fastapi_process.terminate()
        try:
            fastapi_process.wait(timeout=5)
        except:
            fastapi_process.kill()
        return
    
    # Wait a moment for services to stabilize
    time.sleep(5)
    
    # Show access information
    local_ip = get_local_ip()
    print("\n" + "="*50)
    print("🎉 RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*50)
    print("🌐 ACCESS URLS:")
    print(f"   Local Access: http://localhost:8501")
    print(f"   Network Access: http://{local_ip}:8501")
    print(f"   API Endpoint: http://localhost:8000")
    print(f"   API Network: http://{local_ip}:8000")
    print("\n📝 HOW TO USE:")
    print("   1. Open your browser and go to one of the URLs above")
    print("   2. Register a new account or login with existing credentials")
    print("   3. Upload your resume and job description files")
    print("   4. Click 'Start AI Analysis' to get enhanced analysis")
    print("   5. View detailed visualizations and insights")
    print("\n⚠️  Press Ctrl+C to stop both services")
    print("="*50)
    
    # Keep the script running
    try:
        while True:
            # Check if processes are still running
            if fastapi_process.poll() is not None:
                print("❌ FastAPI backend has stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit frontend has stopped unexpectedly")
                break
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
    
    print("✅ All services stopped successfully")

if __name__ == "__main__":
    main()