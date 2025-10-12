#!/usr/bin/env python3
"""
Launch Script for Resume AI Analyzer with JWT Authentication
Starts both the FastAPI backend and Streamlit frontend with proper security
"""

import subprocess
import sys
import time
import webbrowser
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_local_ip():
    """Get the local IP address"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_backend():
    """Start the FastAPI backend with JWT authentication"""
    logger.info("🚀 Starting FastAPI backend with JWT authentication...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        logger.info("✅ FastAPI backend started on http://0.0.0.0:8000")
        return backend_process
    except Exception as e:
        logger.error(f"❌ Failed to start FastAPI backend: {e}")
        return None

def start_frontend():
    """Start the Streamlit frontend"""
    logger.info("🎨 Starting Streamlit frontend with authentication...")
    try:
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", 
            "src/dashboard/streamlit_app.py", 
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ])
        logger.info("✅ Streamlit frontend started on http://0.0.0.0:8501")
        return frontend_process
    except Exception as e:
        logger.error(f"❌ Failed to start Streamlit frontend: {e}")
        return None

def show_access_info():
    """Show access information"""
    local_ip = get_local_ip()
    
    print("\n" + "="*80)
    print("🔐 RESUME AI ANALYZER - JWT AUTHENTICATION ENABLED")
    print("="*80)
    
    print("\n💻 LOCAL ACCESS:")
    print("   🎨 Streamlit Dashboard: http://localhost:8501")
    print("   🚀 FastAPI Backend:    http://localhost:8000")
    print("   📚 API Documentation:  http://localhost:8000/docs")
    
    print("\n📱 NETWORK ACCESS:")
    print(f"   🎨 Streamlit Dashboard: http://{local_ip}:8501")
    print(f"   🚀 FastAPI Backend:    http://{local_ip}:8000")
    print(f"   📚 API Documentation:  http://{local_ip}:8000/docs")
    
    print("\n🔐 SECURITY FEATURES:")
    print("   ✅ JWT Authentication for all protected endpoints")
    print("   ✅ Password hashing with SHA-256 and salt")
    print("   ✅ User-specific data isolation")
    print("   ✅ Secure API endpoints")
    
    print("\n💡 USAGE:")
    print("   1. Open the Streamlit dashboard in your browser")
    print("   2. Register a new account or login")
    print("   3. Upload your resume and job description")
    print("   4. Get AI-powered analysis with security protection")
    
    print("\n🛑 Press Ctrl+C to stop both services")
    print("="*80)

def main():
    """Main function to start both services"""
    print("="*80)
    print("🔐 Resume AI Analyzer - Secure Launch with JWT Authentication")
    print("="*80)
    
    # Start backend and frontend
    try:
        backend_process = start_backend()
        if not backend_process:
            logger.error("❌ Failed to start backend")
            return
            
        time.sleep(3)  # Give backend time to start
        
        frontend_process = start_frontend()
        if not frontend_process:
            logger.error("❌ Failed to start frontend")
            backend_process.terminate()
            return
            
        time.sleep(5)  # Give frontend time to start
        
        # Show access information
        show_access_info()
        
        # Open local URL in browser
        print("\n🌐 Opening local URL in your browser...")
        webbrowser.open("http://localhost:8501")
        
        # Wait for processes
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down services...")
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
            print("✅ All services stopped")
            
    except Exception as e:
        logger.error(f"❌ Error starting services: {e}")

if __name__ == "__main__":
    main()