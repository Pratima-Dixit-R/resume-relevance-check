#!/usr/bin/env python3
"""
Deployment Script for Resume Relevance Checker
Makes the app accessible from both PC and mobile devices
"""

import subprocess
import sys
import time
import os
import webbrowser
import threading
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_prerequisites():
    """Check if all prerequisites are met."""
    logger.info("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    
    # Check if required packages are installed
    required_packages = ['streamlit', 'fastapi', 'uvicorn', 'transformers', 'spacy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {missing_packages}")
        logger.info("Please install them using: pip install -r requirements.txt")
        return False
    
    logger.info("✅ All prerequisites met")
    return True

def setup_spacy_model():
    """Setup spaCy model if not already installed."""
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            logger.info("✅ spaCy model already installed")
        except OSError:
            logger.info("📥 Downloading spaCy English model...")
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            logger.info("✅ spaCy model installed successfully")
    except Exception as e:
        logger.warning(f"spaCy setup issue: {e}")

def get_local_ip():
    """Get local IP address for network access."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def start_services():
    """Start both FastAPI and Streamlit services."""
    logger.info("🚀 Starting deployment services...")
    
    base_path = Path(__file__).parent
    processes = []
    
    # Start FastAPI backend
    logger.info("🚀 Starting FastAPI backend...")
    fastapi_cmd = [
        sys.executable, "-m", "uvicorn",
        "src.api.main:app",
        "--host", "0.0.0.0",  # Listen on all interfaces for network access
        "--port", "8000",
        "--reload"
    ]
    
    fastapi_process = subprocess.Popen(
        fastapi_cmd,
        cwd=str(base_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(("FastAPI", fastapi_process))
    logger.info("✅ FastAPI backend started on port 8000")
    
    # Wait a moment before starting Streamlit
    time.sleep(3)
    
    # Start Streamlit frontend
    logger.info("🎨 Starting Streamlit frontend...")
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/dashboard/streamlit_app.py",
        "--server.address", "0.0.0.0",  # Listen on all interfaces for network access
        "--server.port", "8501",
        "--server.headless", "true"
    ]
    
    streamlit_process = subprocess.Popen(
        streamlit_cmd,
        cwd=str(base_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(("Streamlit", streamlit_process))
    logger.info("✅ Streamlit frontend started on port 8501")
    
    return processes

def display_access_info():
    """Display access information for both PC and mobile."""
    local_ip = get_local_ip()
    
    print("\n" + "="*70)
    print("🏆 RESUME RELEVANCE CHECKER - FULLY DEPLOYED")
    print("="*70)
    print("💻 PC ACCESS:")
    print("   🎨 Frontend (Streamlit): http://localhost:8501")
    print("   🚀 Backend (FastAPI):    http://localhost:8000")
    print("   📚 API Documentation:    http://localhost:8000/docs")
    
    if local_ip:
        print("\n📱 MOBILE ACCESS (Same WiFi Network):")
        print(f"   🎨 Frontend (Streamlit): http://{local_ip}:8501")
        print(f"   🚀 Backend (FastAPI):    http://{local_ip}:8000")
        print(f"   📚 API Documentation:    http://{local_ip}:8000/docs")
        print("\n💡 TIP: Connect your mobile device to the same WiFi network")
        print(f"   and open your browser to http://{local_ip}:8501")
    
    print("\n" + "="*70)
    print("🔧 DEVELOPMENT MODE: Services will reload automatically on code changes")
    print("🛑 Press Ctrl+C to stop all services")
    print("="*70)

def monitor_processes(processes):
    """Monitor running processes and handle shutdown."""
    try:
        while True:
            for name, process in processes:
                if process.poll() is not None:
                    logger.error(f"❌ {name} process has stopped unexpectedly")
                    return False
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutdown requested...")
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"✅ {name} stopped")
            except:
                process.kill()
                logger.info(f"🔥 {name} force killed")
        return True

def main():
    """Main deployment function."""
    logger.info("🚀 Starting Resume Relevance Checker Deployment")
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup spaCy model
    setup_spacy_model()
    
    # Start services
    try:
        processes = start_services()
        
        # Wait for services to initialize
        time.sleep(5)
        
        # Display access information
        display_access_info()
        
        # Open browser to local access
        logger.info("🌐 Opening browser to local access...")
        webbrowser.open("http://localhost:8501")
        
        # Monitor processes
        monitor_processes(processes)
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        sys.exit(1)
    
    logger.info("🎯 Deployment completed successfully")

if __name__ == "__main__":
    main()