#!/usr/bin/env python3
"""
Public Access Information for Resume Relevance Checker
Displays public URLs for accessing the application from anywhere
"""

import socket
import subprocess
import sys
import time
import threading
import webbrowser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        logger.error(f"Failed to get local IP: {e}")
        return None

def get_public_ip():
    """Get the public IP address of this machine"""
    try:
        # Use multiple methods to get public IP
        import urllib.request
        public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        return public_ip
    except:
        try:
            import urllib.request
            public_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
            return public_ip
        except:
            return None

def start_application():
    """Start the unified application"""
    logger.info("🚀 Starting Resume Relevance Checker...")
    
    # Start the unified launcher as a subprocess
    try:
        process = subprocess.Popen(
            [sys.executable, "unified_launcher.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        logger.info("✅ Application process started")
        return process
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        return None

def display_public_access_info():
    """Display public access information"""
    # Get IP addresses
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    # Define ports
    streamlit_port = 8501
    fastapi_port = 8000
    
    print("\n" + "="*80)
    print("🌐 RESUME RELEVANCE CHECKER - PUBLIC ACCESS INFORMATION")
    print("="*80)
    
    # Local access
    print("💻 LOCAL ACCESS (This computer only):")
    print(f"   🎨 Streamlit Dashboard: http://localhost:{streamlit_port}")
    print(f"   🚀 FastAPI Backend:    http://localhost:{fastapi_port}")
    print(f"   📚 API Documentation:  http://localhost:{fastapi_port}/docs")
    
    # Network access
    if local_ip:
        print("\n🌐 NETWORK ACCESS (Same WiFi/LAN):")
        print(f"   🎨 Streamlit Dashboard: http://{local_ip}:{streamlit_port}")
        print(f"   🚀 FastAPI Backend:    http://{local_ip}:{fastapi_port}")
        print(f"   📚 API Documentation:  http://{local_ip}:{fastapi_port}/docs")
    
    # Public access information
    if public_ip:
        print("\n🌍 PUBLIC ACCESS INFORMATION:")
        print(f"   Your Public IP Address: {public_ip}")
        print(f"   🔧 To access from the internet, you need to:")
        print(f"      1. Configure port forwarding on your router for ports {streamlit_port} and {fastapi_port}")
        print(f"      2. Or use a tunneling service like ngrok or localtunnel")
        print(f"   📱 Public URLs (after port forwarding):")
        print(f"      🎨 Streamlit Dashboard: http://{public_ip}:{streamlit_port}")
        print(f"      🚀 FastAPI Backend:    http://{public_ip}:{fastapi_port}")
        print(f"      📚 API Documentation:  http://{public_ip}:{fastapi_port}/docs")
    else:
        print("\n🌍 PUBLIC ACCESS INFORMATION:")
        print("   🔧 To access from the internet, you need to:")
        print("      1. Find your public IP address")
        print("      2. Configure port forwarding on your router for ports 8501 and 8000")
        print("      3. Or use a tunneling service like ngrok or localtunnel")
    
    print("\n" + "="*80)
    print("💡 TIPS FOR SHARING:")
    print("   • For local sharing (same WiFi): Use the NETWORK ACCESS URLs")
    print("   • For internet sharing: Use a tunneling service or configure port forwarding")
    print("   • Make sure your firewall allows connections on ports 8501 and 8000")
    print("="*80)

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
    """Main function to start application and display access information"""
    print("="*80)
    print("🔐 Resume Relevance Checker - Access Setup")
    print("="*80)
    
    # Start the application
    app_process = start_application()
    if not app_process:
        logger.error("❌ Failed to start application")
        return
    
    # Wait a moment for services to initialize
    logger.info("⏳ Waiting for services to start...")
    time.sleep(15)
    
    # Display access information
    display_public_access_info()
    
    # Open local URL in browser
    logger.info("🌐 Opening local URL in your browser...")
    webbrowser.open("http://localhost:8501")
    
    # Monitor the application
    logger.info("🔄 Application is running!")
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
        if app_process:
            app_process.terminate()
        logger.info("✅ All services stopped")

if __name__ == "__main__":
    main()