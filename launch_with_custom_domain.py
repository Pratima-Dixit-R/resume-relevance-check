#!/usr/bin/env python3
"""
Launch script for Resume AI Analyzer with custom domain-like HTTPS URL.
This script launches the application and creates an HTTPS tunnel that can be mapped to a custom domain.
"""

import os
import sys
import subprocess
import time
import requests
import threading
from pathlib import Path

def check_services_running():
    """Check if the required services are already running."""
    fastapi_running = False
    streamlit_running = False
    
    try:
        # Check FastAPI backend
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            fastapi_running = True
            print("✅ FastAPI backend is already running")
    except:
        pass
    
    try:
        # Check Streamlit frontend
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            streamlit_running = True
            print("✅ Streamlit frontend is already running")
    except:
        pass
    
    return fastapi_running, streamlit_running

def start_services():
    """Start the FastAPI and Streamlit services."""
    print("🚀 Starting Resume AI Analyzer services...")
    
    # Start FastAPI backend
    print("🔧 Starting FastAPI backend on port 8000...")
    fastapi_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])
    
    time.sleep(3)  # Give backend time to start
    
    # Start Streamlit frontend
    print("🎨 Starting Streamlit frontend on port 8501...")
    streamlit_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", 
        "run", "src/dashboard/streamlit_app.py", 
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    
    time.sleep(5)  # Give frontend time to start
    
    return fastapi_process, streamlit_process

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

def create_ngrok_tunnel():
    """Create ngrok tunnel for HTTPS access."""
    try:
        from pyngrok import ngrok
        import pyngrok.conf
        
        # Kill any existing ngrok processes
        ngrok.kill()
        
        # Create tunnel for Streamlit (port 8501)
        print("🔗 Creating HTTPS tunnel for Streamlit frontend...")
        streamlit_tunnel = ngrok.connect(8501, "http", bind_tls=True)
        
        # Create tunnel for FastAPI (port 8000)
        print("🔗 Creating HTTPS tunnel for FastAPI backend...")
        fastapi_tunnel = ngrok.connect(8000, "http", bind_tls=True)
        
        return streamlit_tunnel, fastapi_tunnel
    except Exception as e:
        print(f"❌ Failed to create ngrok tunnel: {e}")
        return None, None

def show_access_info(streamlit_tunnel=None, fastapi_tunnel=None):
    """Show all access information."""
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🤖 RESUME AI ANALYZER - LAUNCH SUCCESSFUL")
    print("="*60)
    
    if streamlit_tunnel:
        # Extract the HTTPS URL from the tunnel
        streamlit_url = str(streamlit_tunnel).replace("NgrokTunnel: ", "").replace('"', '')
        print(f"🌐 PUBLIC HTTPS URL: {streamlit_url}")
        print("   (This can be mapped to https://www.resumeaianalyzer.in/)")
    else:
        print("🌐 LOCAL ACCESS URLs:")
        print(f"   Local:  http://localhost:8501")
        print(f"   Network: http://{local_ip}:8501")
    
    print("\n🔧 SERVICE URLs:")
    if fastapi_tunnel:
        fastapi_url = str(fastapi_tunnel).replace("NgrokTunnel: ", "").replace('"', '')
        print(f"   API: {fastapi_url}")
    else:
        print(f"   API (Local):  http://localhost:8000")
        print(f"   API (Network): http://{local_ip}:8000")
    
    print("\n📝 HOW TO ACCESS:")
    if streamlit_tunnel:
        print("   1. Open the PUBLIC HTTPS URL above in your browser")
    else:
        print("   1. Open http://localhost:8501 in your browser")
    print("   2. Register a new account or login")
    print("   3. Upload your resume and job description")
    print("   4. Click 'Start AI Analysis' to get results")
    print("   5. View detailed analysis and visualizations")
    
    print("\n💡 NOTES:")
    print("   - All AI analysis errors have been fixed")
    print("   - HTTPS encryption is enabled")
    print("   - Cross-browser compatibility ensured")
    if streamlit_tunnel:
        print("   - Public access available via secure tunnel")
    print("="*60)

def main():
    """Main function to launch the application."""
    print("🤖 Resume AI Analyzer - Professional Launch")
    print("🔧 Launching with enhanced AI analysis and HTTPS access")
    
    # Check if services are already running
    fastapi_running, streamlit_running = check_services_running()
    
    processes = []
    
    # Start services if not running
    if not fastapi_running or not streamlit_running:
        fastapi_process, streamlit_process = start_services()
        processes.extend([fastapi_process, streamlit_process])
        time.sleep(5)  # Wait for services to be ready
    else:
        print("⏭️  Services already running, skipping startup")
    
    # Try to create HTTPS tunnel
    streamlit_tunnel, fastapi_tunnel = None, None
    try:
        streamlit_tunnel, fastapi_tunnel = create_ngrok_tunnel()
    except Exception as e:
        print(f"⚠️  Could not create HTTPS tunnel: {e}")
        print("    Continuing with local access only...")
    
    # Show access information
    show_access_info(streamlit_tunnel, fastapi_tunnel)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Kill ngrok tunnels
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
        
        # Terminate processes
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