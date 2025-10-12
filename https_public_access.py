#!/usr/bin/env python3
"""
HTTPS Public Access for Resume AI Analyzer
Creates secure HTTPS tunnels using ngrok for cross-browser access
"""

import subprocess
import sys
import time
import webbrowser
import logging
import os
from pyngrok import ngrok
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_ngrok_auth():
    """Setup ngrok authentication if authtoken is available"""
    # Check if NGROK_AUTH_TOKEN environment variable is set
    auth_token = os.environ.get("NGROK_AUTH_TOKEN")
    if auth_token:
        try:
            ngrok.set_auth_token(auth_token)
            logger.info("✅ Ngrok auth token set successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to set ngrok auth token: {e}")
            return False
    else:
        logger.warning("⚠️  No NGROK_AUTH_TOKEN environment variable found")
        logger.info("💡 For persistent HTTPS URLs, set NGROK_AUTH_TOKEN environment variable")
        logger.info("   Sign up at: https://dashboard.ngrok.com/signup")
        logger.info("   Get token at: https://dashboard.ngrok.com/get-started/your-authtoken")
        return True  # Continue with free tier

def start_application():
    """Start the Resume AI Analyzer application"""
    logger.info("🚀 Starting Resume AI Analyzer application...")
    try:
        # Start the launch_with_auth.py script
        process = subprocess.Popen(
            [sys.executable, "launch_with_auth.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait for services to start
        logger.info("⏳ Waiting for services to start...")
        time.sleep(15)
        
        # Check if services are running
        result_8501 = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        result_8000 = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        
        port_8501_listening = ':8501' in result_8501.stdout and 'LISTENING' in result_8501.stdout
        port_8000_listening = ':8000' in result_8000.stdout and 'LISTENING' in result_8000.stdout
        
        if port_8501_listening and port_8000_listening:
            logger.info("✅ Application started successfully")
            return process
        else:
            logger.error("❌ Failed to start application services")
            return None
            
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        return None

def create_https_tunnels():
    """Create HTTPS tunnels for both Streamlit and FastAPI"""
    try:
        logger.info("🔗 Creating secure HTTPS tunnels with ngrok...")
        
        # Create HTTPS tunnel for Streamlit (port 8501)
        streamlit_tunnel = ngrok.connect(
            addr="8501",
            proto="http",
            bind_tls=True  # This ensures HTTPS
        )
        streamlit_https_url = str(streamlit_tunnel.public_url) if streamlit_tunnel.public_url else ""
        logger.info(f"🎨 Streamlit HTTPS URL: {streamlit_https_url}")
        
        # Create HTTPS tunnel for FastAPI (port 8000)
        fastapi_tunnel = ngrok.connect(
            addr="8000",
            proto="http",
            bind_tls=True  # This ensures HTTPS
        )
        fastapi_https_url = str(fastapi_tunnel.public_url) if fastapi_tunnel.public_url else ""
        logger.info(f"🚀 FastAPI HTTPS URL: {fastapi_https_url}")
        
        # Display API documentation URL
        if fastapi_https_url:
            api_docs_url = f"{fastapi_https_url}/docs"
            logger.info(f"📚 API Documentation: {api_docs_url}")
        
        print("\n" + "="*80)
        print("🔒 SECURE HTTPS ACCESS URLs")
        print("="*80)
        print(f"🎨 Streamlit Dashboard: {streamlit_https_url}")
        print(f"🚀 FastAPI Backend:     {fastapi_https_url}")
        print(f"📚 API Documentation:   {api_docs_url if 'api_docs_url' in locals() else 'N/A'}")
        print("="*80)
        print("💡 These HTTPS URLs can be accessed from any browser including:")
        print("   • Google Chrome")
        print("   • Firefox")
        print("   • Safari (Apple)")
        print("   • DuckDuckGo Browser")
        print("   • Yahoo Mobile Browser")
        print("   • Comet Browser")
        print("   • And any other modern browser")
        print("="*80)
        
        # Open the Streamlit URL in browser
        if streamlit_https_url:
            logger.info(f"🌐 Opening {streamlit_https_url} in your default browser...")
            webbrowser.open(streamlit_https_url)
        
        return streamlit_tunnel, fastapi_tunnel
        
    except Exception as e:
        logger.error(f"❌ Failed to create HTTPS tunnels: {e}")
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("   1. Make sure you have internet connection")
        print("   2. For persistent HTTPS URLs, set NGROK_AUTH_TOKEN environment variable")
        print("   3. Sign up at: https://dashboard.ngrok.com/signup")
        print("   4. Get token at: https://dashboard.ngrok.com/get-started/your-authtoken")
        return None, None

def main():
    """Main function to start application and create HTTPS tunnels"""
    print("="*80)
    print("🔒 Resume AI Analyzer - Secure HTTPS Public Access")
    print("="*80)
    
    # Setup ngrok authentication
    if not setup_ngrok_auth():
        logger.error("❌ Failed to setup ngrok authentication")
        return
    
    # Start the application
    app_process = start_application()
    if not app_process:
        logger.error("❌ Failed to start application")
        return
    
    # Create HTTPS tunnels
    streamlit_tunnel, fastapi_tunnel = create_https_tunnels()
    
    if not streamlit_tunnel or not fastapi_tunnel:
        logger.error("❌ Failed to create HTTPS tunnels")
        app_process.terminate()
        return
    
    # Keep the script running
    logger.info("🔄 Application is running and securely accessible via HTTPS!")
    logger.info("🛑 Press Ctrl+C to stop all services")
    
    try:
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