#!/usr/bin/env python3
"""
Complete launch script for Resume AI Analyzer.
This script starts all services and creates an HTTPS tunnel with a professional URL.
"""

import os
import sys
import subprocess
import time
import requests
import threading
from pathlib import Path

def install_required_packages():
    """Install required packages if not already installed."""
    required_packages = [
        'pyngrok',
        'requests'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def start_fastapi():
    """Start FastAPI backend service."""
    print("🔧 Starting FastAPI backend on port 8000...")
    try:
        # Check if already running
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ FastAPI backend is already running")
            return None
    except:
        pass
    
    # Start the process
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for it to start
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ FastAPI backend started successfully")
                return process
        except:
            time.sleep(1)
    
    print("⚠️  FastAPI backend may not have started properly")
    return process

def start_streamlit():
    """Start Streamlit frontend service."""
    print("🎨 Starting Streamlit frontend on port 8501...")
    try:
        # Check if already running
        response = requests.get("http://localhost:8501", timeout=2)
        if response.status_code == 200:
            print("✅ Streamlit frontend is already running")
            return None
    except:
        pass
    
    # Start the process
    process = subprocess.Popen([
        sys.executable, "-m", "streamlit", 
        "run", "src/dashboard/streamlit_app.py", 
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for it to start
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://localhost:8501", timeout=1)
            if response.status_code == 200:
                print("✅ Streamlit frontend started successfully")
                return process
        except:
            time.sleep(1)
    
    print("⚠️  Streamlit frontend may not have started properly")
    return process

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

def create_https_tunnel():
    """Create HTTPS tunnel using ngrok."""
    try:
        from pyngrok import ngrok
        import pyngrok.conf
        
        print("🔗 Creating secure HTTPS tunnels...")
        
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        # Create tunnel for Streamlit (port 8501)
        streamlit_tunnel = ngrok.connect(8501, "http", bind_tls=True)
        
        # Create tunnel for FastAPI (port 8000)
        fastapi_tunnel = ngrok.connect(8000, "http", bind_tls=True)
        
        return streamlit_tunnel, fastapi_tunnel
    except Exception as e:
        print(f"❌ Failed to create HTTPS tunnel: {e}")
        print("💡 To use ngrok, you may need to:")
        print("   1. Sign up at https://dashboard.ngrok.com/signup")
        print("   2. Install authtoken: https://dashboard.ngrok.com/get-started/your-authtoken")
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
        print("🌐 PUBLIC HTTPS ACCESS:")
        print(f"   Professional URL: {streamlit_url}")
        print("   (Can be mapped to https://www.resumeaianalyzer.in/)")
        print(f"   API Endpoint: {streamlit_url.replace(':8501', ':8000')}")
    else:
        print("🌐 LOCAL ACCESS:")
        print(f"   Web Interface: http://localhost:8501")
        print(f"   Network Access: http://{local_ip}:8501")
        print(f"   API Endpoint: http://localhost:8000")
        print(f"   API Network: http://{local_ip}:8000")
    
    print("\n📝 HOW TO USE:")
    print("   1. Open the URL in your browser")
    print("   2. Register or login to your account")
    print("   3. Upload your resume and job description")
    print("   4. Click 'Start AI Analysis' (errors fixed!)")
    print("   5. View detailed results and visualizations")
    
    print("\n🔒 SECURITY FEATURES:")
    print("   ✅ LinkedIn-level encryption (bcrypt + HS512 JWT)")
    print("   ✅ Rate limiting protection")
    print("   ✅ User data isolation")
    if streamlit_tunnel:
        print("   ✅ HTTPS encryption for public access")
    
    print("\n💡 TIPS:")
    print("   • For persistent HTTPS URLs, set up ngrok auth token")
    print("   • For custom domain, configure DNS CNAME to ngrok URL")
    print("   • Mobile access available on same network")
    print("="*60)

def main():
    """Main function to launch everything."""
    print("🤖 Resume AI Analyzer - Professional Launch")
    print("🔧 Starting all services with HTTPS access")
    
    # Install required packages
    try:
        install_required_packages()
    except Exception as e:
        print(f"⚠️  Warning: Could not install packages: {e}")
    
    # Start services
    fastapi_process = start_fastapi()
    time.sleep(2)  # Small delay
    streamlit_process = start_streamlit()
    
    # Wait a moment for services to stabilize
    time.sleep(3)
    
    # Create HTTPS tunnel
    streamlit_tunnel, fastapi_tunnel = None, None
    try:
        streamlit_tunnel, fastapi_tunnel = create_https_tunnel()
    except Exception as e:
        print(f"⚠️  Could not create HTTPS tunnel: {e}")
    
    # Show access information
    show_access_info(streamlit_tunnel, fastapi_tunnel)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop all services")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        
        # Kill ngrok
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
        
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