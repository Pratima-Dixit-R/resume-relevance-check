#!/usr/bin/env python3
"""
Public URL Generator for Resume Relevance Checker
Creates a secure HTTPS tunnel using ngrok to make the local application accessible publicly
"""

import subprocess
import sys
import time
import threading
import webbrowser
import os
from pyngrok import ngrok
import logging

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
    """Create ngrok tunnel for both FastAPI and Streamlit"""
    try:
        # Check if ngrok auth token is set
        auth_token = os.environ.get("NGROK_AUTH_TOKEN")
        if auth_token:
            ngrok.set_auth_token(auth_token)
            logger.info("🔑 Ngrok auth token set")
        else:
            logger.warning("⚠️  No ngrok auth token found. Using free tier (may have limitations)")
        
        # Set up ngrok tunnel for Streamlit (port 8501)
        streamlit_tunnel = ngrok.connect(addr="8501", proto="http")
        streamlit_public_url = str(streamlit_tunnel.public_url) if streamlit_tunnel.public_url else ""
        logger.info(f"🎨 Streamlit Public URL: {streamlit_public_url}")
        
        # Set up ngrok tunnel for FastAPI (port 8000)
        fastapi_tunnel = ngrok.connect(addr="8000", proto="http")
        fastapi_public_url = str(fastapi_tunnel.public_url) if fastapi_tunnel.public_url else ""
        logger.info(f"🚀 FastAPI Public URL: {fastapi_public_url}")
        
        # Display API documentation URL
        api_docs_url = f"{fastapi_public_url}/docs"
        logger.info(f"📚 API Documentation: {api_docs_url}")
        
        print("\n" + "="*80)
        print("🌍 PUBLIC ACCESS URLs")
        print("="*80)
        print(f"🎨 Streamlit Dashboard: {streamlit_public_url}")
        print(f"🚀 FastAPI Backend:     {fastapi_public_url}")
        print(f"📚 API Documentation:   {api_docs_url}")
        print("="*80)
        print("💡 Share these URLs with anyone to access your application remotely")
        print("💡 Works on both laptops and mobile devices")
        print("="*80)
        
        # Open the Streamlit URL in browser
        if streamlit_public_url:
            logger.info(f"🌐 Opening {streamlit_public_url} in your browser...")
            webbrowser.open(streamlit_public_url)
        
        return streamlit_tunnel, fastapi_tunnel
        
    except Exception as e:
        logger.error(f"❌ Failed to create tunnel: {e}")
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("   1. Make sure you have ngrok installed: 'pip install pyngrok'")
        print("   2. For persistent tunnels, sign up at https://ngrok.com and set NGROK_AUTH_TOKEN environment variable")
        print("   3. Alternative: Use localtunnel with 'npx localtunnel --port 8501'")
        return None, None

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
    print("🔐 Resume Relevance Checker - Public Access Setup")
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
    logger.info("🔗 Creating secure tunnels with ngrok...")
    streamlit_tunnel, fastapi_tunnel = create_tunnel()
    
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
        try:
            ngrok.kill()
        except:
            pass
        app_process.terminate()
        logger.info("✅ All services stopped")

if __name__ == "__main__":
    main()