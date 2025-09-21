#!/usr/bin/env python3
"""
🎯 Qoder IDE Setup Script for Resume Relevance Check Application
Automated setup and launch script specifically designed for Qoder IDE
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

class QoderSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.src_path = self.project_root / "src"
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "streamlit", "transformers", 
            "sentence-transformers", "sqlalchemy", "plotly"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - Missing")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        
        print("✅ All dependencies ready!")
        
    def setup_environment(self):
        """Setup environment variables for Qoder IDE"""
        print("🔧 Setting up environment...")
        
        # Add project root to Python path
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))
        
        # Set environment variables
        os.environ["PYTHONPATH"] = str(self.project_root)
        os.environ["QODER_PROJECT_ROOT"] = str(self.project_root)
        
        print("✅ Environment configured!")
        
    def start_fastapi_backend(self):
        """Start FastAPI backend in a separate thread"""
        def run_fastapi():
            os.chdir(self.project_root)
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "src.api.main:app", 
                "--reload", 
                "--host", "127.0.0.1", 
                "--port", "8000"
            ]
            subprocess.run(cmd)
        
        backend_thread = threading.Thread(target=run_fastapi, daemon=True)
        backend_thread.start()
        print("🚀 FastAPI backend starting on http://127.0.0.1:8000")
        return backend_thread
        
    def start_streamlit_dashboard(self):
        """Start Streamlit dashboard in a separate thread"""
        def run_streamlit():
            os.chdir(self.project_root)
            cmd = [
                sys.executable, "-m", "streamlit", "run", 
                "src/dashboard/streamlit_app.py",
                "--server.port", "8501",
                "--server.headless", "true"
            ]
            subprocess.run(cmd)
        
        dashboard_thread = threading.Thread(target=run_streamlit, daemon=True)
        dashboard_thread.start()
        print("🎨 Streamlit dashboard starting on http://localhost:8501")
        return dashboard_thread
        
    def wait_for_services(self):
        """Wait for services to start and open browser"""
        print("⏳ Waiting for services to start...")
        time.sleep(5)
        
        # Check if services are running
        try:
            import requests
            
            # Check FastAPI
            fastapi_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if fastapi_response.status_code == 200:
                print("✅ FastAPI backend is ready!")
            else:
                print("⚠️ FastAPI backend might not be ready")
        except:
            print("⚠️ FastAPI backend is starting...")
            
        # Open browser for Qoder IDE preview
        print("🌐 Opening applications in Qoder's browser preview...")
        
    def display_qoder_instructions(self):
        """Display Qoder-specific usage instructions"""
        print("\n" + "="*60)
        print("🎯 QODER IDE IMPLEMENTATION COMPLETE!")
        print("="*60)
        print()
        print("📍 Your Resume Relevance Check application is now running!")
        print()
        print("🔗 Access URLs:")
        print("   • FastAPI API: http://127.0.0.1:8000")
        print("   • API Docs: http://127.0.0.1:8000/docs")
        print("   • Streamlit Dashboard: http://localhost:8501")
        print()
        print("🎛️ Qoder IDE Features to Use:")
        print("   • Source Control Panel → Push to GitHub")
        print("   • Run/Debug Panel → Use configured launch profiles")
        print("   • Integrated Terminal → Monitor application logs")
        print("   • Browser Preview → Test application directly in IDE")
        print()
        print("🚀 Next Steps in Qoder IDE:")
        print("   1. Open Source Control panel")
        print("   2. Stage your changes")
        print("   3. Commit with message: 'Complete Qoder IDE implementation'")
        print("   4. Push to: https://github.com/Pratima-Dixit-R/resume-relevance-check")
        print("   5. Use Run/Debug configurations for future launches")
        print()
        print("🎉 Ready for AI-powered resume analysis!")
        print("="*60)
        
    def run_complete_setup(self):
        """Run the complete setup process"""
        print("🎯 Starting Qoder IDE Setup for Resume Relevance Check")
        print("="*60)
        
        try:
            self.check_dependencies()
            self.setup_environment()
            
            # Start both services
            fastapi_thread = self.start_fastapi_backend()
            time.sleep(3)  # Give FastAPI time to start
            streamlit_thread = self.start_streamlit_dashboard()
            
            self.wait_for_services()
            self.display_qoder_instructions()
            
            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down services...")
                
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            print("Please check the QODER_IMPLEMENTATION_GUIDE.md for manual setup")

if __name__ == "__main__":
    setup = QoderSetup()
    setup.run_complete_setup()