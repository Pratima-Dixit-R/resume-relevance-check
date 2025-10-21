#!/usr/bin/env python3
"""
Integrated launcher for Resume AI Analyzer.
This script launches both the FastAPI backend and Streamlit frontend together,
and provides correct access URLs.
"""

import os
import sys
import subprocess
import time
import threading
import requests
import json
from pathlib import Path

def launch_backend():
    """Launch the FastAPI backend."""
    print("🚀 Launching FastAPI backend on port 8000...")
    
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def launch_frontend():
    """Launch the Streamlit frontend."""
    print("🎨 Launching Streamlit frontend on port 8501...")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/dashboard/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "127.0.0.1"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def check_backend_health():
    """Check if the backend is healthy."""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend_health():
    """Check if the frontend is responding."""
    try:
        response = requests.get("http://127.0.0.1:8501", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_local_ip():
    """Get the local network IP address."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    """Main function to launch integrated application."""
    print("🤖 Resume AI Analyzer - Integrated Launcher")
    print("="*50)
    
    # Get local IP for network access
    local_ip = get_local_ip()
    print(f"🌐 Local Network IP: {local_ip}")
    
    # Launch backend first
    print("🔧 Starting backend services...")
    backend_process = launch_backend()
    if not backend_process:
        print("❌ Failed to launch backend. Exiting.")
        return
    
    # Wait and check backend
    print("⏳ Waiting for backend to initialize...")
    time.sleep(8)
    
    if not check_backend_health():
        print("❌ Backend failed to start properly")
        # Try to get error output
        try:
            stdout, stderr = backend_process.communicate(timeout=1)
            if stderr:
                print(f"Backend error: {stderr}")
        except:
            pass
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            pass
        return
    
    print("✅ Backend is running and healthy!")
    
    # Launch frontend
    print("🔧 Starting frontend services...")
    frontend_process = launch_frontend()
    if not frontend_process:
        print("❌ Failed to launch frontend. Stopping backend.")
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            pass
        return
    
    # Wait and check frontend
    print("⏳ Waiting for frontend to initialize...")
    time.sleep(12)
    
    if not check_frontend_health():
        print("❌ Frontend failed to start properly")
        # Try to get error output
        try:
            stdout, stderr = frontend_process.communicate(timeout=1)
            if stderr:
                print(f"Frontend error: {stderr}")
        except:
            pass
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except:
            pass
        return
    
    print("✅ Frontend is running and responsive!")
    
    # Display correct access information
    print("\n" + "="*65)
    print("🎉 RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*65)
    print("📱 CORRECT ACCESS URLs (USE THESE, NOT 0.0.0.0):")
    print(f"   🖥️  Local Frontend:     http://localhost:8501")
    print(f"   🌐 Network Frontend:   http://{local_ip}:8501")
    print(f"   📡 Direct Frontend:    http://127.0.0.1:8501")
    print(f"   🔧 Local Backend API:  http://localhost:8000/docs")
    print(f"   ❤️  Backend Health:    http://localhost:8000/health")
    
    print("\n📝 HOW TO ACCESS CORRECTLY:")
    print("   1. OPEN ONE OF THESE FRONTEND URLs IN CHROME/COMET BROWSER:")
    print("      - http://localhost:8501 (recommended for local use)")
    print(f"      - http://{local_ip}:8501 (for other devices on same network)")
    print("      - http://127.0.0.1:8501 (alternative)")
    print("   2. The backend API runs automatically in the background")
    print("   3. Register a new account or login")
    print("   4. Upload your resume and job description files")
    print("   5. Click 'Start AI Analysis' to get results")
    
    print("\n🚫 DO NOT USE THESE (WILL NOT WORK):")
    print("   ❌ http://0.0.0.0:8501")
    print("   ❌ http://0.0.0.0:8000")
    print("   ❌ https://0.0.0.0:8501")
    
    print("\n💡 TIPS:")
    print("   - Wait 5-10 seconds after opening URL for app to load completely")
    print("   - Use Chrome or Comet browser (avoid Microsoft Edge)")
    print("   - If one URL doesn't work, try another from the list")
    print("   - Both frontend and backend are integrated and running")
    print("="*65)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop both services")
    
    # Keep track of processes
    processes = [backend_process, frontend_process]
    
    try:
        # Keep the script running and monitor services
        while True:
            time.sleep(1)
            # Optional: Add health checks here to restart if needed
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate all processes
        for process in processes:
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