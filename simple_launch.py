#!/usr/bin/env python3
"""
Simple launch script for Resume AI Analyzer.
This script launches both services in the correct order with proper error handling.
"""

import os
import sys
import subprocess
import time
import threading
import requests
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
    
    # Change to project root directory
    os.chdir(Path(__file__).parent)
    
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
    
    # Change to project root directory
    os.chdir(Path(__file__).parent)
    
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

def check_if_running(port, path="/"):
    """Check if a service is running on the specified port."""
    try:
        response = requests.get(f"http://localhost:{port}{path}", timeout=3)
        return response.status_code == 200
    except:
        return False

def create_https_tunnel():
    """Create HTTPS tunnel using localtunnel."""
    try:
        # Try to create tunnel for Streamlit (port 8501)
        print("🔗 Creating HTTPS tunnel for Streamlit...")
        streamlit_tunnel = subprocess.Popen([
            'npx', 'localtunnel', '--port', '8501'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Try to create tunnel for FastAPI (port 8000)
        print("🔗 Creating HTTPS tunnel for FastAPI...")
        fastapi_tunnel = subprocess.Popen([
            'npx', 'localtunnel', '--port', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        time.sleep(5)  # Give tunnels time to establish
        
        print("✅ HTTPS tunnels initiated")
        print("   Check terminal output for actual HTTPS URLs")
        return streamlit_tunnel, fastapi_tunnel
        
    except Exception as e:
        print(f"❌ Failed to create HTTPS tunnels: {e}")
        return None, None

def main():
    """Main function to launch the application."""
    print("🤖 Resume AI Analyzer - Simple Launch")
    print("="*50)
    
    # Get local IP for network access
    local_ip = get_local_ip()
    print(f"🌐 Local IP: {local_ip}")
    
    # Launch backend first
    backend_process = launch_backend()
    if not backend_process:
        print("❌ Failed to launch backend. Exiting.")
        return
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Check if backend is running
    if not check_if_running(8000, "/health"):
        print("❌ Backend failed to start properly")
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
    time.sleep(8)
    
    # Check if frontend is running
    if not check_if_running(8501):
        print("❌ Frontend failed to start properly")
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except:
            pass
        return
    
    print("✅ Frontend is running!")
    
    # Display access information
    print("\n" + "="*60)
    print("🎉 APPLICATION LAUNCHED SUCCESSFULLY!")
    print("="*60)
    print("📱 ACCESS THE APP:")
    print(f"   Local URL:  http://localhost:8501")
    print(f"   Network URL: http://{local_ip}:8501")
    print(f"   Backend API: http://localhost:8000/docs")
    print("\n💡 INSTRUCTIONS:")
    print("   1. Open http://localhost:8501 in your browser")
    print("   2. Register a new account or login")
    print("   3. Upload your resume and job description")
    print("   4. Click 'Start AI Analysis' to get results")
    print("\n🔒 FOR HTTPS ACCESS:")
    print("   Run this command in a new terminal:")
    print("   npx localtunnel --port 8501")
    print("="*60)
    
    print("\n🔄 Application is running! Press Ctrl+C to stop.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Terminate processes
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
            print("✅ Services stopped successfully")
        except Exception as e:
            print(f"⚠️  Error stopping services: {e}")

if __name__ == "__main__":
    main()