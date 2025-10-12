#!/usr/bin/env python3
"""
Launch script for the enhanced Resume Relevance Checker with advanced analysis
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_if_running():
    """Check if the services are already running"""
    try:
        # Check FastAPI backend
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI backend is already running")
            fastapi_running = True
        else:
            fastapi_running = False
    except:
        fastapi_running = False
    
    try:
        # Check if port 8501 is in use (Streamlit)
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8501))
        sock.close()
        streamlit_running = (result == 0)
        if streamlit_running:
            print("✅ Streamlit frontend is already running")
    except:
        streamlit_running = False
    
    return fastapi_running, streamlit_running

def start_backend():
    """Start FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])
    return backend_process

def start_frontend():
    """Start Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", 
        "run", "src/dashboard/streamlit_app.py", 
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    return frontend_process

def wait_for_services():
    """Wait for services to be ready"""
    print("⏳ Waiting for services to be ready...")
    
    # Wait for FastAPI
    fastapi_ready = False
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ FastAPI backend is ready")
                fastapi_ready = True
                break
        except:
            time.sleep(1)
    
    if not fastapi_ready:
        print("⚠️  FastAPI backend may not be ready")
    
    # Wait a bit more for Streamlit
    time.sleep(5)
    print("✅ Services should be ready!")

def show_access_info():
    """Show access information"""
    import socket
    
    # Get local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "127.0.0.1"
    
    print("\n" + "="*60)
    print("🤖 RESUME RELEVANCE CHECKER - ENHANCED VERSION")
    print("="*60)
    print("✅ Advanced AI analysis with multiple backends")
    print("✅ Detailed scoring and visualizations")
    print("✅ Enhanced data analytics and insights")
    print("✅ Secure JWT authentication")
    print("\n🌐 ACCESS URLS:")
    print(f"   Local access: http://localhost:8501")
    print(f"   Network access: http://{local_ip}:8501")
    print(f"   API access: http://{local_ip}:8000")
    print("\n📝 LOGIN INFORMATION:")
    print("   First-time users: Register a new account")
    print("   Returning users: Use your existing credentials")
    print("\n📊 ENHANCED FEATURES:")
    print("   - Multi-backend AI analysis (Hugging Face, Sentence Transformers, spaCy)")
    print("   - Detailed score breakdown with visualizations")
    print("   - Advanced analytics and trend analysis")
    print("   - Performance insights and recommendations")
    print("="*60)

def main():
    """Main function"""
    print("🤖 Launching Enhanced Resume Relevance Checker")
    print("🔧 With advanced AI analysis and data visualization")
    
    # Check if services are already running
    fastapi_running, streamlit_running = check_if_running()
    
    processes = []
    
    # Start backend if not running
    if not fastapi_running:
        backend_process = start_backend()
        processes.append(backend_process)
        time.sleep(3)  # Give backend time to start
    else:
        print("⏭️  Skipping backend start (already running)")
    
    # Start frontend if not running
    if not streamlit_running:
        frontend_process = start_frontend()
        processes.append(frontend_process)
    else:
        print("⏭️  Skipping frontend start (already running)")
    
    # Wait for services
    wait_for_services()
    
    # Show access information
    show_access_info()
    
    print("\n📝 INSTRUCTIONS:")
    print("1. Open your browser and go to one of the URLs above")
    print("2. Register a new account or login with existing credentials")
    print("3. Upload your resume and job description")
    print("4. Click 'Start AI Analysis' to get enhanced analysis")
    print("5. View detailed visualizations and insights")
    print("\n⚠️  Press Ctrl+C to stop services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        for process in processes:
            process.terminate()
        
        # Wait for processes to terminate
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print("✅ Services stopped successfully")

if __name__ == "__main__":
    main()