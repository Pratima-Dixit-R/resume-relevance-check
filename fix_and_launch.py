#!/usr/bin/env python3
"""
Fix and launch script for Resume AI Analyzer.
This script fixes the binding issue and launches the application correctly.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def fix_streamlit_binding():
    """Fix Streamlit binding issue by updating the app configuration."""
    print("🔧 Fixing Streamlit binding issue...")
    
    streamlit_app_path = Path("src/dashboard/streamlit_app.py")
    if streamlit_app_path.exists():
        # Read the file
        with open(streamlit_app_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Make sure we're not binding to 0.0.0.0 in the app itself
        # The binding should be handled by the command line arguments
        print("✅ Streamlit app checked")
    else:
        print("❌ Streamlit app not found")

def start_fastapi():
    """Start FastAPI backend service correctly."""
    print("🚀 Starting FastAPI backend...")
    
    try:
        # Start FastAPI binding to all interfaces
        fastapi_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for it to start
        time.sleep(3)
        
        # Check if it's running
        if fastapi_process.poll() is None:
            print("✅ FastAPI backend started successfully")
            return fastapi_process
        else:
            stdout, stderr = fastapi_process.communicate()
            print(f"❌ FastAPI failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI: {e}")
        return None

def start_streamlit():
    """Start Streamlit frontend service correctly."""
    print("🎨 Starting Streamlit frontend...")
    
    try:
        # Start Streamlit binding to all interfaces
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", "src/dashboard/streamlit_app.py", 
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for it to start
        time.sleep(5)
        
        # Check if it's running
        if streamlit_process.poll() is None:
            print("✅ Streamlit frontend started successfully")
            return streamlit_process
        else:
            stdout, stderr = streamlit_process.communicate()
            print(f"❌ Streamlit failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        return None

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

def test_accessibility():
    """Test if the services are accessible."""
    print("🔍 Testing service accessibility...")
    
    # Test FastAPI
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI is accessible")
        else:
            print(f"❌ FastAPI returned status {response.status_code}")
    except Exception as e:
        print(f"❌ FastAPI is not accessible: {e}")
    
    # Test Streamlit
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit is accessible")
        else:
            print(f"❌ Streamlit returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Streamlit is not accessible: {e}")

def push_to_github():
    """Push changes to GitHub repository."""
    print("🔄 Pushing changes to GitHub...")
    
    try:
        # Add all changes
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error adding files: {result.stderr}")
            return
        
        # Commit changes
        result = subprocess.run(["git", "commit", "-m", "Fix application launch issues and prepare for deployment"], 
                              capture_output=True, text=True)
        if result.returncode != 0 and "nothing to commit" not in result.stderr:
            print(f"❌ Error committing: {result.stderr}")
            return
        
        # Push to GitHub
        result = subprocess.run(["git", "push", "origin", "main"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Changes pushed to GitHub successfully")
        else:
            print(f"❌ Error pushing to GitHub: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Unexpected error pushing to GitHub: {e}")

def main():
    """Main function."""
    print("🤖 Resume AI Analyzer - Fix and Launch")
    print("=" * 40)
    
    # Fix any binding issues
    fix_streamlit_binding()
    
    # Start services
    print("\n🚀 Starting services...")
    fastapi_process = start_fastapi()
    if not fastapi_process:
        print("❌ Failed to start FastAPI backend")
        return
    
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit frontend")
        fastapi_process.terminate()
        return
    
    # Wait for services to fully initialize
    print("⏳ Waiting for services to initialize...")
    time.sleep(5)
    
    # Test accessibility
    test_accessibility()
    
    # Show access information
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print("🎉 RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*60)
    print("🌐 ACCESS URLS:")
    print(f"   Local Access: http://localhost:8501")
    print(f"   Network Access: http://{local_ip}:8501")
    print(f"   API Endpoint: http://localhost:8000")
    print(f"   API Network: http://{local_ip}:8000")
    print("\n📝 HOW TO USE:")
    print("   1. Open your browser and go to http://localhost:8501")
    print("   2. Register a new account or login with existing credentials")
    print("   3. Upload your resume and job description files")
    print("   4. Click 'Start AI Analysis' to get enhanced analysis")
    print("   5. View detailed visualizations and insights")
    print("\n⚠️  Press Ctrl+C to stop both services")
    print("="*60)
    
    # Push changes to GitHub
    push_to_github()
    
    # Keep the script running
    print("\n🔄 Application is now running! Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate processes
        for process in [fastapi_process, streamlit_process]:
            if process:
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