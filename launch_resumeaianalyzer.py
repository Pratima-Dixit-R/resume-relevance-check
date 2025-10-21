#!/usr/bin/env python3
"""
Launch script for Resume AI Analyzer with https://www.resumeaianalyzer.in domain.
This script launches the Streamlit app and creates a tunnel for the specific domain.
"""

import os
import sys
import subprocess
import time
import threading
import requests
import json
import webbrowser
from pathlib import Path

def launch_streamlit_app():
    """Launch the existing Streamlit app."""
    print("🚀 Launching Resume AI Analyzer on port 8501...")
    
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

def create_localtunnel():
    """Create tunnel using localtunnel with a custom subdomain."""
    try:
        print("🔗 Creating tunnel for https://www.resumeaianalyzer.in...")
        
        # Create tunnel for the app (port 8501) with custom subdomain
        tunnel_process = subprocess.Popen([
            'npx', 'localtunnel', '--port', '8501', '--subdomain', 'resumeaianalyzer'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for tunnel to establish
        time.sleep(5)
        
        public_url = "https://resumeaianalyzer.loca.lt"
        print(f"✅ Tunnel created: {public_url}")
        print("   This can be mapped to https://www.resumeaianalyzer.in")
        return tunnel_process, public_url
        
    except Exception as e:
        print(f"⚠️  Failed to create custom subdomain tunnel: {e}")
        try:
            # Try without custom subdomain
            print("   Trying without custom subdomain...")
            tunnel_process = subprocess.Popen([
                'npx', 'localtunnel', '--port', '8501'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for tunnel to establish
            time.sleep(5)
            print("✅ Tunnel created successfully!")
            print("   Check terminal output for the public URL")
            return tunnel_process, None
        except Exception as e2:
            print(f"❌ Failed to create tunnel: {e2}")
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

def main():
    """Main function to launch the application."""
    print("🤖 Resume AI Analyzer - Launch Script")
    print("="*45)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"🌐 Local Network IP: {local_ip}")
    
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
    
    # Create tunnel for public access
    tunnel_process, public_url = create_localtunnel()
    
    # Display access information specifically for https://www.resumeaianalyzer.in
    print("\n" + "="*70)
    print("🎉 RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*70)
    
    if public_url:
        print(f"🌐 PUBLIC ACCESS URL: {public_url}")
        print("   ✅ Accessible from anywhere with internet!")
        print("\n🎯 TO USE YOUR DOMAIN https://www.resumeaianalyzer.in:")
        print("   1. Go to your domain registrar's DNS management")
        print("   2. Add a CNAME record:")
        print("      - Name: www")
        print(f"      - Value: {public_url.replace('https://', '')}")
        print("      - TTL: 3600 (or default)")
        print("   3. Wait for DNS propagation (may take a few minutes to hours)")
    else:
        print("🌐 PUBLIC ACCESS:")
        print("   Check the localtunnel terminal output for the HTTPS URL")
        print("   It will look like: https://random-subdomain.loca.lt")
        print("\n🎯 TO USE YOUR DOMAIN https://www.resumeaianalyzer.in:")
        print("   1. First get the public URL from localtunnel output above")
        print("   2. Go to your domain registrar's DNS management")
        print("   3. Add a CNAME record pointing 'www' to that URL")
    
    print("\n📱 ACCESS OPTIONS:")
    print(f"   Local Access:     http://localhost:8501")
    print(f"   Network Access:   http://{local_ip}:8501")
    print(f"   Direct IP Access: http://127.0.0.1:8501")
    if public_url:
        print(f"   Public Access:    {public_url}")
    
    print("\n📝 HOW TO ACCESS:")
    print("   1. For local use: http://localhost:8501")
    if public_url:
        print(f"   2. For public access: {public_url}")
        print("   3. For your domain: https://www.resumeaianalyzer.in (after DNS setup)")
    else:
        print("   2. For public access: Check localtunnel URL above")
    
    print("\n💡 TIPS:")
    print("   - Use Chrome or Comet browser (avoid Microsoft Edge)")
    print("   - Wait a few seconds for the app to load completely")
    print("   - No more 0.0.0.0 addresses (they don't work in browsers)")
    print("   - HTTPS encryption provided through tunnel")
    print("="*70)
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop the service")
    
    # Keep track of processes
    processes = [app_process]
    if tunnel_process:
        processes.append(tunnel_process)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate all processes
        for process in processes:
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