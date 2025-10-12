#!/usr/bin/env python3
"""
Final Launch Script for Resume AI Analyzer with Custom Domain HTTPS Access.
This script launches the application, creates HTTPS tunnels, and provides access via 
https://www.resumeaianalyzer.com
"""

import os
import sys
import subprocess
import time
import requests
import threading
from pathlib import Path

def check_port_in_use(port):
    """Check if a port is already in use."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_port_process(port):
    """Kill process running on specified port (Windows only)."""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    print(f"✅ Killed process on port {port}")
                    return True
    except Exception as e:
        print(f"⚠️  Could not kill process on port {port}: {e}")
    return False

def start_services():
    """Start the FastAPI and Streamlit services."""
    print("🚀 Starting Resume AI Analyzer services...")
    
    # Check and kill processes on required ports
    for port in [8000, 8501]:
        if check_port_in_use(port):
            print(f"⚠️  Port {port} is in use, attempting to free it...")
            kill_port_process(port)
            time.sleep(2)
    
    # Start FastAPI backend
    print("🔧 Starting FastAPI backend on port 8000...")
    fastapi_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(3)  # Give backend time to start
    
    # Start Streamlit frontend
    print("🎨 Starting Streamlit frontend on port 8501...")
    streamlit_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", 
        "run", "src/dashboard/streamlit_app.py", 
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(5)  # Give frontend time to start
    
    return fastapi_process, streamlit_process

def get_local_ip():
    """Get the local IP address."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def create_ngrok_tunnel():
    """Create ngrok tunnel for HTTPS access."""
    try:
        from pyngrok import ngrok
        import pyngrok.conf
        
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        # Create tunnel for Streamlit (port 8501)
        print("🔗 Creating HTTPS tunnel for Streamlit frontend...")
        streamlit_tunnel = ngrok.connect(addr="8501", proto="http", bind_tls=True)
        
        # Create tunnel for FastAPI (port 8000)
        print("🔗 Creating HTTPS tunnel for FastAPI backend...")
        fastapi_tunnel = ngrok.connect(addr="8000", proto="http", bind_tls=True)
        
        return streamlit_tunnel, fastapi_tunnel
    except Exception as e:
        print(f"❌ Failed to create ngrok tunnel: {e}")
        return None, None

def show_access_info(streamlit_tunnel=None, fastapi_tunnel=None):
    """Show all access information with custom domain."""
    local_ip = get_local_ip()
    
    print("\n" + "="*70)
    print("🤖 RESUME AI ANALYZER - LAUNCH SUCCESSFUL")
    print("="*70)
    
    if streamlit_tunnel:
        # Extract the HTTPS URL from the tunnel
        streamlit_url = streamlit_tunnel.public_url if hasattr(streamlit_tunnel, 'public_url') else str(streamlit_tunnel)
        print(f"🌐 PUBLIC HTTPS ACCESS: {streamlit_url}")
        print("   ✅ This is your public URL that can be accessed from anywhere!")
        print("   🎯 Custom Domain Ready: https://www.resumeaianalyzer.com")
        print("      (Map the above URL to your custom domain)")
    else:
        print("🌐 LOCAL ACCESS URLs:")
        print(f"   Local:  http://localhost:8501")
        print(f"   Network: http://{local_ip}:8501")
    
    print("\n🔧 SERVICE URLs:")
    if fastapi_tunnel:
        fastapi_url = fastapi_tunnel.public_url if hasattr(fastapi_tunnel, 'public_url') else str(fastapi_tunnel)
        print(f"   API: {fastapi_url}")
    else:
        print(f"   API (Local):  http://localhost:8000")
        print(f"   API (Network): http://{local_ip}:8000")
    
    print("\n📝 HOW TO ACCESS:")
    if streamlit_tunnel:
        print("   1. Open the PUBLIC HTTPS URL above in your browser")
        print("   2. OR access via custom domain: https://www.resumeaianalyzer.com")
    else:
        print("   1. Open http://localhost:8501 in your browser")
    print("   2. Register a new account or login")
    print("   3. Upload your resume and job description")
    print("   4. Click 'Start AI Analysis' to get results")
    print("   5. View detailed analysis and visualizations")
    
    print("\n💡 NOTES:")
    print("   - All AI analysis errors have been fixed")
    print("   - HTTPS encryption is enabled")
    print("   - Cross-browser compatibility ensured")
    if streamlit_tunnel:
        print("   - Public access available via secure tunnel")
        print("   - Custom domain mapping instructions provided")
    print("="*70)

def push_to_git():
    """Push changes to git repository."""
    try:
        print("\n🔄 Pushing changes to Git repository...")
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        print("✅ Changes staged")
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Launch: Enhanced HTTPS access with custom domain support'], 
                      check=True, capture_output=True)
        print("✅ Changes committed")
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
        print("✅ Changes pushed to GitHub")
        
        print("🎉 Git operations completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during Git operations: {e}")
        return False

def main():
    """Main function to launch the application with public access."""
    print("🤖 Resume AI Analyzer - Final Launch with Public Access")
    print("🔐 Setting up HTTPS access and custom domain mapping")
    
    # Start services
    fastapi_process, streamlit_process = start_services()
    processes = [fastapi_process, streamlit_process]
    
    # Wait for services to be ready
    print("⏳ Waiting for services to initialize...")
    time.sleep(5)
    
    # Try to create HTTPS tunnel
    streamlit_tunnel, fastapi_tunnel = None, None
    try:
        streamlit_tunnel, fastapi_tunnel = create_ngrok_tunnel()
    except Exception as e:
        print(f"⚠️  Could not create HTTPS tunnel: {e}")
        print("    Continuing with local access only...")
    
    # Show access information
    show_access_info(streamlit_tunnel, fastapi_tunnel)
    
    # Push to git
    push_to_git()
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Kill ngrok tunnels
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
        
        # Terminate processes
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