#!/usr/bin/env python3
"""
Resume AI Analyzer - Complete Application Launcher
Automated Resume Scoring and Analysis System with AI Integration
"""

import os
import sys
import subprocess
import time
import logging
import webbrowser
from pathlib import Path
import signal
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResumeAnalyzerLauncher:
    """Complete launcher for Resume AI Analyzer application."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.processes = []
        self.ports = {
            'fastapi': 8000,
            'streamlit': 8502
        }
        
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        logger.info("🔍 Checking dependencies...")
        
        required_packages = [
            'streamlit', 'fastapi', 'uvicorn', 'ollama', 
            'transformers', 'sentence-transformers', 'spacy',
            'pandas', 'numpy', 'scikit-learn', 'plotly'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✅ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"❌ {package} is missing")
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.info("Installing missing packages...")
            self.install_packages(missing_packages)
        
        # Check spaCy model
        try:
            import spacy
            spacy.load("en_core_web_sm")
            logger.info("✅ spaCy English model is available")
        except:
            logger.info("📥 Downloading spaCy English model...")
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            
    def install_packages(self, packages):
        """Install missing packages."""
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            logger.info("✅ All packages installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install packages: {e}")
            
    def check_ollama_status(self):
        """Check Ollama availability and models."""
        logger.info("🤖 Checking Ollama status...")
        try:
            import ollama
            models = ollama.list()
            if models.get('models'):
                logger.info(f"✅ Ollama available with {len(models['models'])} models")
                for model in models['models']:
                    logger.info(f"   📦 {model['name']}")
            else:
                logger.warning("⚠️ Ollama is running but no models available")
                logger.info("💡 Consider installing a model: ollama pull llama3.2")
        except Exception as e:
            logger.warning(f"⚠️ Ollama not available: {e}")
            logger.info("💡 Application will use fallback AI models")
            
    def kill_existing_processes(self):
        """Kill any existing processes on our ports."""
        for port_name, port in self.ports.items():
            try:
                for proc in psutil.process_iter(['pid', 'name', 'connections']):
                    try:
                        connections = proc.info['connections']
                        if connections:
                            for conn in connections:
                                if conn.laddr.port == port:
                                    logger.info(f"🔄 Killing existing process on port {port}")
                                    proc.terminate()
                                    proc.wait(timeout=3)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                logger.warning(f"Error checking port {port}: {e}")
                
    def start_fastapi_backend(self):
        """Start FastAPI backend server."""
        logger.info("🚀 Starting FastAPI backend...")
        
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app",
            "--host", "0.0.0.0",
            "--port", str(self.ports['fastapi']),
            "--reload"
        ]
        
        try:
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            self.processes.append(('FastAPI', process))
            logger.info(f"✅ FastAPI backend starting on port {self.ports['fastapi']}")
            
            # Wait a moment for startup
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start FastAPI: {e}")
            return False
            
    def start_streamlit_frontend(self):
        """Start Streamlit frontend."""
        logger.info("🎨 Starting Streamlit frontend...")
        
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "src/dashboard/streamlit_app.py",
            "--server.port", str(self.ports['streamlit']),
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ]
        
        try:
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            self.processes.append(('Streamlit', process))
            logger.info(f"✅ Streamlit frontend starting on port {self.ports['streamlit']}")
            
            # Wait for startup
            time.sleep(5)
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start Streamlit: {e}")
            return False
            
    def wait_for_services(self):
        """Wait for services to be ready."""
        logger.info("⏳ Waiting for services to be ready...")
        
        import requests
        max_retries = 30
        
        # Check FastAPI
        for i in range(max_retries):
            try:
                response = requests.get(f"http://localhost:{self.ports['fastapi']}/health", timeout=2)
                if response.status_code == 200:
                    logger.info("✅ FastAPI backend is ready")
                    break
            except:
                time.sleep(1)
        else:
            logger.warning("⚠️ FastAPI backend may not be fully ready")
            
        # Check Streamlit
        for i in range(max_retries):
            try:
                response = requests.get(f"http://localhost:{self.ports['streamlit']}", timeout=2)
                if response.status_code == 200:
                    logger.info("✅ Streamlit frontend is ready")
                    break
            except:
                time.sleep(1)
        else:
            logger.warning("⚠️ Streamlit frontend may not be fully ready")
            
    def open_browser(self):
        """Open the application in browser."""
        logger.info("🌐 Opening application in browser...")
        time.sleep(2)
        webbrowser.open(f"http://localhost:{self.ports['streamlit']}")
        
    def print_status(self):
        """Print application status and URLs."""
        print("\\n" + "="*80)
        print("🎉 RESUME AI ANALYZER - SUCCESSFULLY LAUNCHED!")
        print("="*80)
        print(f"🎨 Frontend (Streamlit):  http://localhost:{self.ports['streamlit']}")
        print(f"🚀 Backend (FastAPI):     http://localhost:{self.ports['fastapi']}")
        print(f"📚 API Documentation:    http://localhost:{self.ports['fastapi']}/docs")
        print(f"🔍 Health Check:         http://localhost:{self.ports['fastapi']}/health")
        print("="*80)
        print("📁 Sample Data Available:")
        print("   📄 Resume Samples:     ./sample_resumes/")
        print("   💼 Job Descriptions:   ./sample_jds/")
        print("="*80)
        print("🤖 AI Features:")
        print("   🧠 Ollama LLM Integration")
        print("   🔬 Hugging Face Transformers")
        print("   📊 spaCy NLP Analysis")
        print("   📈 Statistical TF-IDF Scoring")
        print("="*80)
        print("💡 Usage:")
        print("   1. Upload resume and job description files")
        print("   2. Get comprehensive AI-powered analysis")
        print("   3. View detailed scoring (1-100 scale)")
        print("   4. Access analytics and insights")
        print("="*80)
        print("⏹️  Press Ctrl+C to stop all services")
        print("="*80)
        
    def cleanup(self):
        """Cleanup processes on exit."""
        logger.info("🧹 Cleaning up processes...")
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"✅ {name} stopped")
            except:
                try:
                    process.kill()
                    logger.info(f"🔥 {name} force killed")
                except:
                    pass
                    
    def run(self):
        """Main launcher method."""
        try:
            logger.info("🚀 Starting Resume AI Analyzer...")
            
            # Setup
            self.check_dependencies()
            self.check_ollama_status()
            self.kill_existing_processes()
            
            # Start services
            if not self.start_fastapi_backend():
                return False
                
            if not self.start_streamlit_frontend():
                return False
                
            # Wait and open
            self.wait_for_services()
            self.print_status()
            self.open_browser()
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
                    # Check if processes are still running
                    for name, process in self.processes:
                        if process.poll() is not None:
                            logger.error(f"❌ {name} process has stopped")
                            return False
            except KeyboardInterrupt:
                logger.info("\\n👋 Shutting down gracefully...")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Launch failed: {e}")
            return False
        finally:
            self.cleanup()

if __name__ == "__main__":
    launcher = ResumeAnalyzerLauncher()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        launcher.cleanup()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    success = launcher.run()
    sys.exit(0 if success else 1)