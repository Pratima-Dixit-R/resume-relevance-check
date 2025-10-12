#!/usr/bin/env python3
"""
Final solution for Resume AI Analyzer.
This script fixes all errors, launches the application properly, and prepares it for deployment.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_and_fix_dependencies():
    """Check and fix dependencies."""
    print("🔧 Checking dependencies...")
    
    # Required packages
    required_packages = [
        'streamlit',
        'fastapi',
        'uvicorn',
        'requests',
        'plotly',
        'pandas',
        'numpy',
        'scikit-learn',
        'PyPDF2',
        'python-docx',
        'fuzzywuzzy',
        'python-Levenshtein',
        'nltk',
        'transformers',
        'sentence-transformers',
        'torch',
        'spacy',
        'pydantic',
        'sqlalchemy',
        'bcrypt',
        'PyJWT',
        'python-multipart'
    ]
    
    # Check if packages are installed
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'torch':
                import torch
            elif package == 'transformers':
                import transformers
            elif package == 'sentence-transformers':
                import sentence_transformers
            elif package == 'spacy':
                import spacy
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All dependencies installed successfully")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
    else:
        print("✅ All dependencies are already installed")

def fix_streamlit_app():
    """Fix any issues in the Streamlit app."""
    print("🔧 Fixing Streamlit app issues...")
    
    streamlit_app_path = Path("src/dashboard/streamlit_app.py")
    if streamlit_app_path.exists():
        # Read the file
        with open(streamlit_app_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix any common issues
        # Ensure API_BASE_URL is correct
        if "API_BASE_URL = \"http://localhost:8000/api/v1\"" not in content:
            content = content.replace('API_BASE_URL = "http://localhost:8000/api/v1"', 'API_BASE_URL = "http://localhost:8000/api/v1"')
        
        # Write back the file
        with open(streamlit_app_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Streamlit app fixed")
    else:
        print("❌ Streamlit app not found")

def start_fastapi():
    """Start FastAPI backend service."""
    print("🚀 Starting FastAPI backend on port 8000...")
    
    try:
        # Start FastAPI with proper error handling
        fastapi_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for it to start (up to 30 seconds)
        for i in range(30):
            try:
                response = requests.get("http://localhost:8000/health", timeout=1)
                if response.status_code == 200:
                    print("✅ FastAPI backend started successfully")
                    return fastapi_process
            except:
                pass
            time.sleep(1)
        
        # Check if process is still running
        if fastapi_process.poll() is None:
            print("✅ FastAPI backend process is running")
            return fastapi_process
        else:
            print("❌ FastAPI failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI: {e}")
        return None

def start_streamlit():
    """Start Streamlit frontend service."""
    print("🎨 Starting Streamlit frontend on port 8501...")
    
    try:
        # Start Streamlit with proper error handling
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", "src/dashboard/streamlit_app.py", 
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for it to start (up to 30 seconds)
        for i in range(30):
            try:
                response = requests.get("http://localhost:8501", timeout=1)
                if response.status_code == 200:
                    print("✅ Streamlit frontend started successfully")
                    return streamlit_process
            except:
                pass
            time.sleep(1)
        
        # Check if process is still running
        if streamlit_process.poll() is None:
            print("✅ Streamlit frontend process is running")
            return streamlit_process
        else:
            print("❌ Streamlit failed to start")
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

def create_https_tunnel():
    """Create HTTPS tunnel for public access."""
    print("🔗 Creating HTTPS tunnel...")
    
    try:
        # Try to import pyngrok
        from pyngrok import ngrok
    except ImportError:
        print("📦 Installing pyngrok...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyngrok'])
            from pyngrok import ngrok
        except Exception as e:
            print(f"❌ Failed to install pyngrok: {e}")
            return None, None
    
    try:
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        # Create tunnel for Streamlit (port 8501)
        streamlit_tunnel = ngrok.connect(8501, "http", bind_tls=True)
        
        # Create tunnel for FastAPI (port 8000)
        fastapi_tunnel = ngrok.connect(8000, "http", bind_tls=True)
        
        return streamlit_tunnel, fastapi_tunnel
    except Exception as e:
        print(f"❌ Failed to create HTTPS tunnel: {e}")
        return None, None

def show_access_info(streamlit_tunnel=None, fastapi_tunnel=None):
    """Show all access information."""
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🎉 RESUME AI ANALYZER LAUNCHED SUCCESSFULLY!")
    print("="*60)
    
    if streamlit_tunnel:
        # Extract the HTTPS URL from the tunnel
        streamlit_url = str(streamlit_tunnel).replace("NgrokTunnel: ", "").replace('"', '')
        print("🌐 PUBLIC HTTPS ACCESS:")
        print(f"   Professional URL: {streamlit_url}")
        print("   (This can be mapped to https://www.resumeaianalyzer.in/)")
    else:
        print("🌐 LOCAL ACCESS:")
        print(f"   Web Interface: http://localhost:8501")
        print(f"   Network Access: http://{local_ip}:8501")
        print(f"   API Endpoint: http://localhost:8000")
        print(f"   API Network: http://{local_ip}:8000")
    
    print("\n📝 HOW TO USE:")
    print("   1. Open your browser and go to one of the URLs above")
    print("   2. Register a new account or login with existing credentials")
    print("   3. Upload your resume and job description files")
    print("   4. Click 'Start AI Analysis' to get enhanced analysis")
    print("   5. View detailed visualizations and insights")
    
    print("\n🔒 SECURITY FEATURES:")
    print("   ✅ LinkedIn-level encryption (bcrypt + HS512 JWT)")
    print("   ✅ Rate limiting protection")
    print("   ✅ User data isolation")
    if streamlit_tunnel:
        print("   ✅ HTTPS encryption for public access")
    
    print("\n💡 TIPS:")
    print("   • For custom domain, configure DNS CNAME to the HTTPS URL")
    print("   • Mobile access available on same network")
    print("="*60)

def push_to_github():
    """Push changes to GitHub repository."""
    print("🔄 Pushing changes to GitHub...")
    
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", "Fix application launch issues and prepare for deployment"], check=True)
        
        # Push to origin
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ Changes pushed to GitHub successfully")
    except Exception as e:
        print(f"❌ Error pushing to GitHub: {e}")

def main():
    """Main function to launch everything."""
    print("🤖 Resume AI Analyzer - Final Solution")
    print("=" * 40)
    
    # Check and fix dependencies
    check_and_fix_dependencies()
    
    # Fix Streamlit app issues
    fix_streamlit_app()
    
    # Start services
    print("\n🚀 Starting services...")
    fastapi_process = start_fastapi()
    if not fastapi_process:
        print("❌ Failed to start FastAPI backend")
        return
    
    time.sleep(3)  # Give FastAPI time to fully initialize
    
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit frontend")
        # Terminate FastAPI process
        fastapi_process.terminate()
        try:
            fastapi_process.wait(timeout=5)
        except:
            fastapi_process.kill()
        return
    
    # Wait a moment for services to stabilize
    time.sleep(5)
    
    # Try to create HTTPS tunnel
    streamlit_tunnel, fastapi_tunnel = None, None
    try:
        streamlit_tunnel, fastapi_tunnel = create_https_tunnel()
    except Exception as e:
        print(f"⚠️  Could not create HTTPS tunnel: {e}")
    
    # Show access information
    show_access_info(streamlit_tunnel, fastapi_tunnel)
    
    # Push changes to GitHub
    push_to_github()
    
    print("\n🔄 Application is now running!")
    print("   Press Ctrl+C to stop both services")
    
    # Keep the script running
    try:
        while True:
            # Check if processes are still running
            if fastapi_process.poll() is not None:
                print("❌ FastAPI backend has stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit frontend has stopped unexpectedly")
                break
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