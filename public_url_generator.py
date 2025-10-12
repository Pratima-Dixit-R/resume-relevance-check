#!/usr/bin/env python3
"""
Unified Public URL Generator for Resume AI Analyzer
Creates secure HTTPS tunnels using either ngrok or localtunnel to make the local application accessible publicly
with JWT authentication and security encryption.
"""

import subprocess
import sys
import time
import threading
import webbrowser
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_application_running():
    """Check if the application is already running"""
    try:
        # Check if ports 8501 and 8000 are already in use
        result_8501 = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        result_8000 = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        
        if ':8501' in result_8501.stdout and ':8000' in result_8000.stdout:
            logger.info("✅ Application appears to be already running")
            return True
        return False
    except Exception as e:
        logger.warning(f"Could not check if application is running: {e}")
        return False

def start_application():
    """Start the unified application"""
    logger.info("🚀 Starting Resume AI Analyzer...")
    
    # Check if application is already running
    if check_application_running():
        logger.info("Application is already running, proceeding with tunnel creation")
        return "running"
    
    # Start the unified launcher as a subprocess
    try:
        # Use the launch_network_app.py script which we know works
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

def create_ngrok_tunnel():
    """Create ngrok tunnel for both FastAPI and Streamlit"""
    try:
        from pyngrok import ngrok
        
        logger.info("🔗 Creating ngrok tunnels...")
        
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        # Set up ngrok tunnel for Streamlit (port 8501)
        streamlit_tunnel = ngrok.connect(8501, "http")
        streamlit_public_url = streamlit_tunnel.public_url
        logger.info(f"🎨 Streamlit Public URL: {streamlit_public_url}")
        
        # Set up ngrok tunnel for FastAPI (port 8000)
        fastapi_tunnel = ngrok.connect(8000, "http")
        fastapi_public_url = fastapi_tunnel.public_url
        logger.info(f"🚀 FastAPI Public URL: {fastapi_public_url}")
        
        # Display API documentation URL
        api_docs_url = f"{fastapi_public_url}/docs"
        logger.info(f"📚 API Documentation: {api_docs_url}")
        
        print("\n" + "="*80)
        print("🌍 PUBLIC ACCESS URLs (ngrok)")
        print("="*80)
        print(f"🎨 Streamlit Dashboard: {streamlit_public_url}")
        print(f"🚀 FastAPI Backend:     {fastapi_public_url}")
        print(f"📚 API Documentation:   {api_docs_url}")
        print("="*80)
        print("🔐 JWT Authentication is ENABLED")
        print("💡 Share these URLs with anyone to access your application remotely")
        print("💡 Works on both laptops and mobile devices")
        print("="*80)
        
        # Open the Streamlit URL in browser
        logger.info(f"🌐 Opening {streamlit_public_url} in your browser...")
        try:
            webbrowser.open(streamlit_public_url)
        except:
            logger.warning("Could not open browser automatically")
        
        return streamlit_tunnel, fastapi_tunnel, streamlit_public_url, fastapi_public_url
        
    except Exception as e:
        logger.error(f"❌ Failed to create ngrok tunnel: {e}")
        return None, None, None, None

def create_localtunnel():
    """Create localtunnel for both FastAPI and Streamlit"""
    try:
        logger.info("🔗 Creating localtunnel connections...")
        
        # Start localtunnel for Streamlit (port 8501)
        streamlit_cmd = ["npx", "localtunnel", "--port", "8501"]
        streamlit_tunnel = subprocess.Popen(
            streamlit_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Start localtunnel for FastAPI (port 8000)
        fastapi_cmd = ["npx", "localtunnel", "--port", "8000"]
        fastapi_tunnel = subprocess.Popen(
            fastapi_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait for tunnels to establish and capture URLs
        time.sleep(5)
        
        # Try to get URLs from the output
        streamlit_url = None
        fastapi_url = None
        
        # Read output from streamlit tunnel
        try:
            streamlit_output = streamlit_tunnel.stdout.readline()
            if "your url is:" in streamlit_output:
                streamlit_url = streamlit_output.split("your url is:")[-1].strip()
            else:
                streamlit_url = "http://localhost:8501 (check terminal for localtunnel URL)"
        except:
            streamlit_url = "http://localhost:8501 (localtunnel running)"
        
        # Read output from fastapi tunnel
        try:
            fastapi_output = fastapi_tunnel.stdout.readline()
            if "your url is:" in fastapi_output:
                fastapi_url = fastapi_output.split("your url is:")[-1].strip()
            else:
                fastapi_url = "http://localhost:8000 (check terminal for localtunnel URL)"
        except:
            fastapi_url = "http://localhost:8000 (localtunnel running)"
        
        logger.info(f"🎨 Streamlit Public URL: {streamlit_url}")
        logger.info(f"🚀 FastAPI Public URL: {fastapi_url}")
        
        # Display API documentation URL
        if "http" in fastapi_url:
            api_docs_url = f"{fastapi_url}/docs"
            logger.info(f"📚 API Documentation: {api_docs_url}")
        
        print("\n" + "="*80)
        print("🌍 PUBLIC ACCESS URLs (localtunnel)")
        print("="*80)
        print(f"🎨 Streamlit Dashboard: {streamlit_url}")
        print(f"🚀 FastAPI Backend:     {fastapi_url}")
        if "http" in fastapi_url:
            print(f"📚 API Documentation:   {api_docs_url}")
        print("="*80)
        print("🔐 JWT Authentication is ENABLED")
        print("💡 Share these URLs with anyone to access your application remotely")
        print("💡 Works on both laptops and mobile devices")
        print("="*80)
        
        # Open the Streamlit URL in browser (if we have a proper URL)
        if "http" in streamlit_url and "localhost" not in streamlit_url:
            logger.info(f"🌐 Opening {streamlit_url} in your browser...")
            try:
                webbrowser.open(streamlit_url)
            except:
                logger.warning("Could not open browser automatically")
        
        return streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url
        
    except Exception as e:
        logger.error(f"❌ Failed to create localtunnel: {e}")
        return None, None, None, None

def monitor_application(process):
    """Monitor the application process"""
    if process == "running":
        logger.info("Application is already running, no monitoring needed")
        return
        
    try:
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
            if process.poll() is not None:
                break
    except Exception as e:
        logger.error(f"❌ Error monitoring application: {e}")

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

def show_local_access():
    """Show local access URLs"""
    local_ip = get_local_ip()
    print("\n" + "="*80)
    print("💻 LOCAL ACCESS URLs")
    print("="*80)
    print(f"🎨 Streamlit Dashboard: http://localhost:8501")
    print(f"🎨 Streamlit Dashboard: http://{local_ip}:8501")
    print(f"🚀 FastAPI Backend:     http://localhost:8000")
    print(f"🚀 FastAPI Backend:     http://{local_ip}:8000")
    print(f"📚 API Documentation:   http://localhost:8000/docs")
    print(f"📚 API Documentation:   http://{local_ip}:8000/docs")
    print("="*80)
    print("🔐 JWT Authentication is ENABLED for all protected endpoints")
    print("="*80)

def main():
    """Main function to start application and create public URLs"""
    print("="*80)
    print("🔐 Resume AI Analyzer - Public Access Setup")
    print("="*80)
    
    # Show local access URLs first
    show_local_access()
    
    print("\nTunneling Options:")
    print("1. ngrok (requires account for persistent URLs)")
    print("2. localtunnel (no account required)")
    print("3. Exit")
    
    try:
        choice = input("\nSelect tunneling service (1, 2, or 3): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        return
    
    if choice == "3":
        print("👋 Exiting...")
        return
    
    # Start the application
    app_process = start_application()
    if app_process is None:
        logger.error("❌ Failed to start application")
        return
    
    # Wait a moment for services to initialize
    logger.info("⏳ Waiting for services to start...")
    time.sleep(10)
    
    if choice == "1":
        # Create ngrok tunnels
        logger.info("🔗 Creating secure tunnels with ngrok...")
        streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url = create_ngrok_tunnel()
        
        if not streamlit_tunnel or not fastapi_tunnel:
            logger.error("❌ Failed to create ngrok tunnels")
            if app_process != "running":
                app_process.terminate()
            return
            
    elif choice == "2":
        # Create localtunnel connections
        logger.info("🔗 Creating secure tunnels with localtunnel...")
        streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url = create_localtunnel()
        
        if not streamlit_tunnel or not fastapi_tunnel:
            logger.error("❌ Failed to create localtunnel connections")
            if app_process != "running":
                app_process.terminate()
            return
    else:
        print("❌ Invalid choice")
        if app_process != "running":
            app_process.terminate()
        return
    
    # Monitor the application
    logger.info("🔄 Application is running and publicly accessible!")
    logger.info("🛑 Press Ctrl+C to stop all services")
    
    try:
        # Monitor application output in a separate thread
        monitor_thread = threading.Thread(target=monitor_application, args=(app_process,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down services...")
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
            
        if app_process != "running" and app_process:
            app_process.terminate()
            
        logger.info("✅ All services stopped")

if __name__ == "__main__":
    main()