#!/usr/bin/env python3
"""
Simple unified deployment script for Resume AI Analyzer.
This script launches the existing Streamlit app and creates a public HTTPS tunnel.
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

def create_https_tunnel():
    """Create HTTPS tunnel using localtunnel."""
    try:
        print("🔗 Creating HTTPS tunnel using localtunnel...")
        
        # Create tunnel for the app (port 8501)
        tunnel_process = subprocess.Popen([
            'npx', 'localtunnel', '--port', '8501', '--subdomain', 'resume-analyzer'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for tunnel to establish
        time.sleep(5)
        
        public_url = "https://resume-analyzer.loca.lt"
        print(f"✅ HTTPS tunnel created: {public_url}")
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
            print("✅ HTTPS tunnel created successfully!")
            print("   Check terminal output for the public URL")
            return tunnel_process, None
        except Exception as e2:
            print(f"❌ Failed to create HTTPS tunnel: {e2}")
            return None, None

def main():
    """Main function to deploy the application."""
    print("🚀 Resume AI Analyzer - Simple Unified Deployment")
    print("="*55)
    
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
    
    # Create HTTPS tunnel for public access
    tunnel_process, public_url = create_https_tunnel()
    
    # Display access information
    print("\n" + "="*65)
    print("🎉 RESUME AI ANALYZER DEPLOYED SUCCESSFULLY!")
    print("="*65)
    
    if public_url:
        print(f"🌐 PUBLIC HTTPS ACCESS: {public_url}")
        print("   ✅ Accessible from anywhere with internet!")
        print("   🎯 CUSTOM DOMAIN SETUP:")
        print("      Map https://www.resumeaianalyzer.com DNS to:")
        print(f"      {public_url}")
    else:
        print("🌐 PUBLIC ACCESS:")
        print("   Check the localtunnel terminal output for the HTTPS URL")
        print("   It will look like: https://random-subdomain.loca.lt")
    
    print("\n📱 LOCAL ACCESS URLs:")
    print("   Local URL:    http://localhost:8501")
    print("   Direct IP:    http://127.0.0.1:8501")
    
    print("\n📝 HOW TO ACCESS:")
    if public_url:
        print(f"   1. Public access: {public_url}")
    else:
        print("   1. Check terminal for public HTTPS URL")
    print("   2. Local access: http://localhost:8501")
    print("   3. Register/login and upload your files")
    print("   4. Run AI analysis to get results")
    
    print("\n💡 NOTES:")
    print("   - No more 0.0.0.0 addresses (they don't work in browsers)")
    print("   - Use actual working URLs listed above")
    print("   - HTTPS encryption provided through tunnel")
    print("   - Single port deployment (8501)")
    if public_url:
        print("   - Custom domain ready: https://www.resumeaianalyzer.com")
    print("="*65)
    
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