#!/usr/bin/env python3
"""
Final launch script for Resume AI Analyzer.
This script launches both services correctly and provides exact access URLs.
"""

import os
import sys
import subprocess
import time
import threading
import requests
import webbrowser
from pathlib import Path

def get_local_ip():
    """Get the local IP address of the machine."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def launch_backend():
    """Launch the FastAPI backend server."""
    print("🚀 Launching FastAPI backend on port 8000...")
    
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ]
    
    try:
        backend_process = subprocess.Popen(
            backend_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def launch_frontend():
    """Launch the Streamlit frontend."""
    print("🎨 Launching Streamlit frontend on port 8501...")
    
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/dashboard/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    try:
        frontend_process = subprocess.Popen(
            frontend_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def check_service(port, path="/"):
    """Check if a service is running on the specified port."""
    try:
        response = requests.get(f"http://localhost:{port}{path}", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function to launch the application."""
    print("🤖 Resume AI Analyzer - Final Launch")
    print("="*50)
    
    # Get local IP for network access
    local_ip = get_local_ip()
    print(f"🌐 Local Network IP: {local_ip}")
    
    # Launch backend first
    backend_process = launch_backend()
    if not backend_process:
        print("❌ Failed to launch backend. Exiting.")
        return
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Check if backend is running
    if not check_service(8000, "/health"):
        print("❌ Backend failed to start properly")
        # Print backend error output
        try:
            stdout, stderr = backend_process.communicate(timeout=1)
            print(f"Backend stdout: {stdout}")
            print(f"Backend stderr: {stderr}")
        except:
            pass
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            pass
        return
    
    print("✅ Backend is running!")
    
    # Launch frontend
    frontend_process = launch_frontend()
    if not frontend_process:
        print("❌ Failed to launch frontend. Stopping backend.")
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            pass
        return
    
    # Wait for frontend to start
    print("⏳ Waiting for frontend to initialize...")
    time.sleep(10)
    
    # Check if frontend is running
    if not check_service(8501):
        print("❌ Frontend failed to start properly")
        # Print frontend error output
        try:
            stdout, stderr = frontend_process.communicate(timeout=1)
            print(f"Frontend stdout: {stdout}")
            print(f"Frontend stderr: {stderr}")
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
    
    print("✅ Frontend is running!")
    
    # Display exact access information
    print("\n" + "="*60)
    print("🎉 RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*60)
    print("📱 EXACT ACCESS URLs (USE THESE, NOT http://0.0.0.0:8501):")
    print(f"   ✅ Local Access:     http://localhost:8501")
    print(f"   ✅ Network Access:   http://{local_ip}:8501")
    print(f"   ✅ Direct IP Access: http://127.0.0.1:8501")
    
    print("\n🔧 BACKEND SERVICES:")
    print(f"   📚 API Documentation: http://localhost:8000/docs")
    print(f"   ❤️  Health Check:      http://localhost:8000/health")
    
    print("\n📝 HOW TO ACCESS CORRECTLY:")
    print("   1. OPEN ONE OF THESE URLs IN YOUR BROWSER:")
    print("      - http://localhost:8501 (recommended)")
    print(f"      - http://{local_ip}:8501 (for other devices)")
    print("      - http://127.0.0.1:8501 (alternative)")
    print("   2. Register a new account or login")
    print("   3. Upload your resume and job description")
    print("   4. Click 'Start AI Analysis' to get results")
    
    print("\n🚫 DO NOT USE THESE (WILL NOT WORK):")
    print("   ❌ http://0.0.0.0:8501 (invalid address)")
    print("   ❌ https://0.0.0.0:8501 (invalid address)")
    
    print("\n💡 TIPS:")
    print("   - Wait a few seconds after opening the URL for the app to load")
    print("   - If one URL doesn't work, try another from the list above")
    print("   - Make sure no firewall is blocking the ports")
    print("="*60)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop all services")
    
    # Keep track of all processes
    processes = [backend_process, frontend_process]
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
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