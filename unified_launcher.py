#!/usr/bin/env python3
"""
Unified launcher for Resume AI Analyzer application.
This script launches both the FastAPI backend and Streamlit frontend with proper path configuration.
"""

import os
import sys
import subprocess
import time
import threading
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
    print("🚀 Launching FastAPI backend...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.api.endpoints:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ]
    
    # Set the PYTHONPATH to include the project root
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent) + os.pathsep + env.get("PYTHONPATH", "")
    
    backend_process = subprocess.Popen(
        backend_cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return backend_process

def launch_frontend():
    """Launch the Streamlit frontend."""
    print("🌐 Launching Streamlit frontend...")
    # Wait a moment for backend to start
    time.sleep(3)
    
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/dashboard/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    # Set the PYTHONPATH to include the project root
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent) + os.pathsep + env.get("PYTHONPATH", "")
    
    frontend_process = subprocess.Popen(
        frontend_cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return frontend_process

def display_urls():
    """Display all available URLs for accessing the application."""
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print("✅ APPLICATION LAUNCHED SUCCESSFULLY!")
    print("="*60)
    print(f"📱 Frontend (Streamlit): http://localhost:8501")
    print(f"📱 Frontend (Network): http://{local_ip}:8501")
    print(f"💻 Backend (FastAPI): http://localhost:8000/docs")
    print(f"💻 Backend (Network): http://{local_ip}:8000/docs")
    print("="*60)
    print("💡 To access from other devices on the same network:")
    print(f"   Use: http://{local_ip}:8501")
    print("="*60)

def main():
    """Main function to launch both backend and frontend."""
    print("🚀 Starting Resume AI Analyzer Application...")
    print("This may take a few moments to initialize AI models...\n")
    
    try:
        # Launch backend
        backend_process = launch_backend()
        
        # Launch frontend
        frontend_process = launch_frontend()
        
        # Display URLs after a short delay
        time.sleep(5)
        display_urls()
        
        print("\n📝 Press Ctrl+C to stop both servers\n")
        
        # Wait for both processes
        try:
            while True:
                if backend_process.poll() is not None:
                    print("❌ Backend process has stopped!")
                    break
                if frontend_process.poll() is not None:
                    print("❌ Frontend process has stopped!")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
            print("✅ Servers stopped.")
            
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Add project root to Python path
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    main()