#!/usr/bin/env python3
"""
Ngrok deployment script for Resume AI Analyzer.
This script launches the Streamlit app and creates a public HTTPS tunnel using ngrok.
"""

import os
import sys
import subprocess
import time
import threading
import requests
import json
from pathlib import Path

def launch_streamlit_app():
    """Launch the existing Streamlit app."""
    print("🚀 Launching Streamlit app on port 8501...")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/dashboard/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start Streamlit app: {e}")
        return None

def check_app_running():
    """Check if the Streamlit app is running."""
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        return response.status_code == 200
    except:
        return False

def create_ngrok_tunnel():
    """Create HTTPS tunnel using ngrok."""
    try:
        from pyngrok import ngrok
        import pyngrok.conf
        
        print("🔗 Creating HTTPS tunnel using ngrok...")
        
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        # Create tunnel for the app (port 8501)
        tunnel = ngrok.connect(addr="8501", proto="http", bind_tls=True)
        public_url = tunnel.public_url
        
        print(f"✅ HTTPS tunnel created: {public_url}")
        return tunnel, public_url
        
    except Exception as e:
        print(f"❌ Failed to create ngrok tunnel: {e}")
        print("   Note: Ngrok may require authentication for custom domains")
        return None, None

def main():
    """Main function to deploy the application."""
    print("🚀 Resume AI Analyzer - Ngrok Deployment")
    print("="*45)
    
    # Launch the Streamlit app
    app_process = launch_streamlit_app()
    if not app_process:
        print("❌ Failed to launch Streamlit app. Exiting.")
        return
    
    # Wait for app to start
    print("⏳ Waiting for app to initialize...")
    time.sleep(15)
    
    # Check if app is running
    if not check_app_running():
        print("❌ App failed to start properly")
        try:
            app_process.terminate()
            app_process.wait(timeout=5)
        except:
            pass
        return
    
    print("✅ Streamlit app is running!")
    
    # Create ngrok tunnel for public access
    tunnel, public_url = create_ngrok_tunnel()
    
    # Display access information
    print("\n" + "="*60)
    print("🎉 RESUME AI ANALYZER DEPLOYED SUCCESSFULLY!")
    print("="*60)
    
    if public_url:
        print(f"🌐 PUBLIC HTTPS ACCESS: {public_url}")
        print("   ✅ Accessible from anywhere with internet!")
        print("   🎯 CUSTOM DOMAIN SETUP:")
        print("      For custom domain, you'll need a paid ngrok plan")
        print("      Or map https://www.resumeaianalyzer.com to this URL")
    else:
        print("🌐 LOCAL ACCESS ONLY:")
        print("   Ngrok tunnel failed. Using local access only.")
    
    print("\n📱 ACCESS URLs:")
    print("   Local URL:    http://localhost:8501")
    print("   Network URL:  http://127.0.0.1:8501")
    if public_url:
        print(f"   Public URL:   {public_url}")
    
    print("\n📝 HOW TO ACCESS:")
    print("   1. Local access: http://localhost:8501")
    if public_url:
        print(f"   2. Public access: {public_url}")
    print("   3. Register/login and upload your files")
    print("   4. Run AI analysis to get results")
    
    print("\n💡 NOTES:")
    print("   - No more 0.0.0.0 addresses (they don't work in browsers)")
    print("   - Use actual working URLs listed above")
    print("   - HTTPS encryption provided through tunnel")
    print("   - Single port deployment (8501)")
    if public_url:
        print("   - Public access available via ngrok")
    print("="*60)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop the service")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Kill ngrok tunnel
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
        
        # Terminate app process
        try:
            app_process.terminate()
            app_process.wait(timeout=5)
        except:
            try:
                app_process.kill()
            except:
                pass
        
        print("✅ All services stopped successfully")

if __name__ == "__main__":
    main()