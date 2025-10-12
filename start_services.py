#!/usr/bin/env python3
"""
Simple service starter for Resume Relevance Checker
"""

import subprocess
import sys
import time
from pathlib import Path

def start_fastapi():
    """Start FastAPI backend."""
    print("🚀 Starting FastAPI backend...")
    cmd = [
        sys.executable, "-m", "uvicorn",
        "src.api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    process = subprocess.Popen(cmd, cwd=Path(__file__).parent)
    print("✅ FastAPI backend started on http://localhost:8000")
    return process

def start_streamlit():
    """Start Streamlit frontend."""
    print("🎨 Starting Streamlit frontend...")
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/dashboard/streamlit_app.py",
        "--server.address", "0.0.0.0",
        "--server.port", "8501"
    ]
    
    process = subprocess.Popen(cmd, cwd=Path(__file__).parent)
    print("✅ Streamlit frontend started on http://localhost:8501")
    return process

def main():
    """Main function to start both services."""
    print("="*50)
    print("Resume Relevance Checker - Service Starter")
    print("="*50)
    
    try:
        # Start FastAPI
        fastapi_process = start_fastapi()
        time.sleep(3)  # Wait for FastAPI to start
        
        # Start Streamlit
        streamlit_process = start_streamlit()
        
        print("\n" + "="*50)
        print("Services started successfully!")
        print("💻 Access on PC: http://localhost:8501")
        print("📱 Access on Mobile (same WiFi): http://YOUR_IP_ADDRESS:8501")
        print("🛑 Press Ctrl+C to stop services")
        print("="*50)
        
        # Keep the script running
        try:
            while True:
                if fastapi_process.poll() is not None or streamlit_process.poll() is not None:
                    print("❌ One of the services has stopped")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            fastapi_process.terminate()
            streamlit_process.terminate()
            fastapi_process.wait()
            streamlit_process.wait()
            print("✅ Services stopped")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()