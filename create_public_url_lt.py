#!/usr/bin/env python3
"""
Public URL Generator for Resume Relevance Checker
Creates a secure HTTPS tunnel using localtunnel to make the local application accessible publicly
"""

import subprocess
import sys
import time
import threading
import webbrowser
import requests
import logging
import os
from typing import Optional, Tuple, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_application():
    """Start the unified application"""
    logger.info("🚀 Starting Resume Relevance Checker...")
    
    # Start the unified launcher as a subprocess
    try:
        process = subprocess.Popen(
            [sys.executable, "launch_network_app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        logger.info("✅ Application process started")
        return process
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        return None

def create_tunnel():
    """Create localtunnel for both FastAPI and Streamlit"""
    try:
        # Check if npx is available
        try:
            subprocess.run(["npx", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("❌ npx not found. Please install Node.js and npm to use localtunnel")
            print("\n🔧 INSTALLATION INSTRUCTIONS:")
            print("   1. Download and install Node.js from https://nodejs.org/")
            print("   2. After installation, restart your terminal/command prompt")
            print("   3. Run this script again")
            return None, None, None, None
        
        # Start localtunnel for Streamlit (port 8501) in background
        logger.info("🔗 Starting localtunnel for Streamlit (port 8501)...")
        streamlit_tunnel = subprocess.Popen(
            ["npx", "localtunnel", "--port", "8501"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Start localtunnel for FastAPI (port 8000) in background
        logger.info("🔗 Starting localtunnel for FastAPI (port 8000)...")
        fastapi_tunnel = subprocess.Popen(
            ["npx", "localtunnel", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait a moment for tunnels to establish
        logger.info("⏳ Waiting for tunnels to establish...")
        time.sleep(8)
        
        # Try to get the public URLs
        streamlit_url = ""
        fastapi_url = ""
        
        # Try to read from stdout
        try:
            if streamlit_tunnel.stdout is not None:
                streamlit_output = streamlit_tunnel.stdout.readline().strip()
                if "your url is:" in streamlit_output:
                    streamlit_url = streamlit_output.split("your url is:")[-1].strip()
                else:
                    streamlit_url = streamlit_output
        except:
            pass
            
        try:
            if fastapi_tunnel.stdout is not None:
                fastapi_output = fastapi_tunnel.stdout.readline().strip()
                if "your url is:" in fastapi_output:
                    fastapi_url = fastapi_output.split("your url is:")[-1].strip()
                else:
                    fastapi_url = fastapi_output
        except:
            pass
        
        # If we couldn't get URLs from stdout, provide generic message
        if not streamlit_url:
            streamlit_url = "http://localhost:8501 (localtunnel running, check terminal output for public URL)"
        if not fastapi_url:
            fastapi_url = "http://localhost:8000 (localtunnel running, check terminal output for public URL)"
        
        logger.info(f"🎨 Streamlit Public URL: {streamlit_url}")
        logger.info(f"🚀 FastAPI Public URL: {fastapi_url}")
        
        # Display API documentation URL
        if "http" in fastapi_url and not fastapi_url.startswith("http://localhost"):
            api_docs_url = f"{fastapi_url}/docs"
            logger.info(f"📚 API Documentation: {api_docs_url}")
        else:
            api_docs_url = "http://localhost:8000/docs (check terminal output for public URL)"
        
        print("\n" + "="*80)
        print("🌍 PUBLIC ACCESS URLs")
        print("="*80)
        print(f"🎨 Streamlit Dashboard: {streamlit_url}")
        print(f"🚀 FastAPI Backend:     {fastapi_url}")
        print(f"📚 API Documentation:   {api_docs_url}")
        print("="*80)
        print("💡 Share these URLs with anyone to access your application remotely")
        print("💡 Works on both laptops and mobile devices")
        print("="*80)
        
        # Open the Streamlit URL in browser if it's a valid URL
        if streamlit_url.startswith("http") and not streamlit_url.startswith("http://localhost"):
            logger.info(f"🌐 Opening {streamlit_url} in your browser...")
            webbrowser.open(streamlit_url)
        
        return streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url
        
    except Exception as e:
        logger.error(f"❌ Failed to create tunnel: {e}")
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("   1. Make sure you have Node.js installed (includes npm and npx)")
        print("   2. Alternative: Use ngrok with 'pip install pyngrok'")
        print("   3. Manual: Run 'npx localtunnel --port 8501' in a separate terminal")
        return None, None, None, None

def monitor_application(process):
    """Monitor the application process"""
    try:
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
            if process.poll() is not None:
                break
    except Exception as e:
        logger.error(f"❌ Error monitoring application: {e}")

def main():
    """Main function to start application and create public URLs"""
    print("="*80)
    print("🔐 Resume Relevance Checker - Public Access Setup (LocalTunnel)")
    print("="*80)
    
    # Start the application
    app_process = start_application()
    if not app_process:
        logger.error("❌ Failed to start application")
        return
    
    # Wait a moment for services to initialize
    logger.info("⏳ Waiting for services to start...")
    time.sleep(15)
    
    # Create tunnels
    logger.info("🔗 Creating secure tunnels with localtunnel...")
    streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url = create_tunnel()
    
    if not streamlit_tunnel or not fastapi_tunnel:
        logger.error("❌ Failed to create tunnels")
        app_process.terminate()
        return
    
    # Monitor the application
    logger.info("🔄 Application is running and publicly accessible!")
    logger.info("🛑 Press Ctrl+C to stop all services")
    
    try:
        # Monitor application output
        monitor_thread = threading.Thread(target=monitor_application, args=(app_process,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down services...")
        if streamlit_tunnel:
            streamlit_tunnel.terminate()
        if fastapi_tunnel:
            fastapi_tunnel.terminate()
        if app_process:
            app_process.terminate()
        logger.info("✅ All services stopped")

if __name__ == "__main__":
    main()