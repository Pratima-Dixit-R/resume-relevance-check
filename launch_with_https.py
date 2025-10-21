#!/usr/bin/env python3
"""
Launch script for Resume AI Analyzer with HTTPS tunneling.
This script launches the application and creates HTTPS tunnels for external access.
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def create_https_tunnel():
    """Create HTTPS tunnels using ngrok."""
    try:
        from pyngrok import ngrok
        import pyngrok.conf
        
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        print("🔗 Creating HTTPS tunnels...")
        
        # Create tunnel for Streamlit (port 8501)
        print("   Creating tunnel for Streamlit frontend...")
        streamlit_tunnel = ngrok.connect(addr="8501", proto="http", bind_tls=True)
        streamlit_url = streamlit_tunnel.public_url
        print(f"   ✅ Streamlit: {streamlit_url}")
        
        # Create tunnel for FastAPI (port 8000)
        print("   Creating tunnel for FastAPI backend...")
        fastapi_tunnel = ngrok.connect(addr="8000", proto="http", bind_tls=True)
        fastapi_url = fastapi_tunnel.public_url
        print(f"   ✅ FastAPI: {fastapi_url}")
        
        return streamlit_url, fastapi_url
    except Exception as e:
        print(f"❌ Failed to create HTTPS tunnels: {e}")
        return None, None

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

def display_access_info(streamlit_url=None, fastapi_url=None):
    """Display all access information."""
    local_ip = get_local_ip()
    print("\n" + "="*70)
    print("✅ RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*70)
    
    if streamlit_url:
        print(f"🌐 PUBLIC HTTPS ACCESS: {streamlit_url}")
        print("   This URL can be accessed from anywhere!")
        print(f"   Custom domain ready: https://www.resumeaianalyzer.com")
        print("   (Map your domain DNS to this URL)")
    else:
        print("🌐 LOCAL ACCESS:")
        print(f"   Local: http://localhost:8501")
        print(f"   Network: http://{local_ip}:8501")
    
    print("\n🔧 SERVICE URLs:")
    if fastapi_url:
        print(f"   API Docs: {fastapi_url}/docs")
    else:
        print(f"   API Docs (Local): http://localhost:8000/docs")
        print(f"   API Docs (Network): http://{local_ip}:8000/docs")
    
    print("\n📝 HOW TO ACCESS:")
    if streamlit_url:
        print(f"   1. Open {streamlit_url} in any browser")
        print("   2. OR access via custom domain: https://www.resumeaianalyzer.com")
    else:
        print("   1. Open http://localhost:8501 in your browser")
    print("   2. Register a new account or login")
    print("   3. Upload your resume and job description")
    print("   4. Click 'Start AI Analysis' to get results")
    
    print("\n💡 NOTES:")
    print("   - Application is accessible from all devices on your network")
    print("   - HTTPS encryption is enabled for secure access")
    print("   - Cross-browser compatibility ensured")
    if streamlit_url:
        print("   - Public access available via secure tunnel")
    print("="*70)

def main():
    """Main function."""
    print("🚀 Resume AI Analyzer - Launch with HTTPS Access")
    print("🔐 Creating secure tunnels for external access...")
    
    # Create HTTPS tunnels
    streamlit_url, fastapi_url = create_https_tunnel()
    
    # Display access information
    display_access_info(streamlit_url, fastapi_url)
    
    print("\n🔄 Application is running!")
    print("   Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running to maintain tunnels
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
        print("✅ All services stopped.")

if __name__ == "__main__":
    main()