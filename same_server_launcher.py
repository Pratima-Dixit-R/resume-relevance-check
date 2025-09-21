#!/usr/bin/env python3
"""
Optimized Same-Server Launcher for Resume Relevance Checker
Innomatics Research Labs

Launches Streamlit frontend and FastAPI backend on the same server
with optimized resource management for Windows environments.
"""

import subprocess
import sys
import time
import os
import threading
import signal
import webbrowser
from pathlib import Path
import logging
import json
import gc
import psutil

# Configure lightweight logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OptimizedSameServerLauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.venv_python = self.base_path / "venv" / "Scripts" / "python.exe"
        self.processes = []
        self.running = True
        
        # Optimized configuration for same server
        self.config = {
            "fastapi": {
                "host": "127.0.0.1",  # Local only for better performance
                "port": 8000,
                "module": "src.api.main:app",
                "workers": 1  # Single worker to reduce memory usage
            },
            "streamlit": {
                "host": "127.0.0.1",
                "port": 8501,
                "script": "src/dashboard/streamlit_app.py"
            }
        }
    
    def optimize_environment(self):
        """Optimize environment for better performance."""
        try:
            # Set environment variables for optimization
            os.environ['TORCH_CUDNN_ENABLED'] = 'False'
            os.environ['TORCH_BACKENDS_CUDNN_ENABLED'] = 'False'
            os.environ['PYTORCH_DISABLE_CUDA'] = '1'
            os.environ['CUDA_VISIBLE_DEVICES'] = ''
            os.environ['OMP_NUM_THREADS'] = '2'
            os.environ['MKL_NUM_THREADS'] = '2'
            os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '200'
            os.environ['STREAMLIT_SERVER_MAX_MESSAGE_SIZE'] = '200'
            
            # Force garbage collection
            gc.collect()
            
            logger.info("✅ Environment optimized for same-server deployment")
            return True
            
        except Exception as e:
            logger.error(f"Warning: Could not optimize environment: {e}")
            return True  # Continue anyway
    
    def check_system_resources(self):
        """Check available system resources."""
        try:
            memory = psutil.virtual_memory()
            available_gb = memory.available / (1024**3)
            
            if available_gb < 2.0:
                logger.warning(f"⚠️ Low memory available: {available_gb:.1f}GB")
                logger.info("💡 Consider closing other applications")
            else:
                logger.info(f"✅ Memory available: {available_gb:.1f}GB")
            
            return True
            
        except Exception as e:
            logger.warning(f"Could not check system resources: {e}")
            return True
    
    def start_fastapi_optimized(self):
        """Start FastAPI backend with optimized settings."""
        logger.info("🚀 Starting FastAPI backend (optimized)...")
        
        try:
            cmd = [
                str(self.venv_python), "-m", "uvicorn",
                self.config["fastapi"]["module"],
                "--host", self.config["fastapi"]["host"],
                "--port", str(self.config["fastapi"]["port"]),
                "--workers", str(self.config["fastapi"]["workers"]),
                "--log-level", "warning",  # Reduce log verbosity
                "--access-log",
                "--no-use-colors"
            ]
            
            # Set environment for the process
            env = os.environ.copy()
            env.update({
                'PYTHONUNBUFFERED': '1',
                'PYTHONIOENCODING': 'utf-8'
            })
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                env=env,
                bufsize=1
            )
            
            self.processes.append(("FastAPI", process))
            logger.info(f"✅ FastAPI started on http://{self.config['fastapi']['host']}:{self.config['fastapi']['port']}")
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start FastAPI: {e}")
            return None
    
    def start_streamlit_optimized(self):
        """Start Streamlit frontend with optimized settings."""
        logger.info("🎨 Starting Streamlit frontend (optimized)...")
        
        try:
            cmd = [
                str(self.venv_python), "-m", "streamlit", "run",
                self.config["streamlit"]["script"],
                "--server.address", self.config["streamlit"]["host"],
                "--server.port", str(self.config["streamlit"]["port"]),
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false",
                "--server.maxUploadSize", "200",
                "--server.maxMessageSize", "200",
                "--browser.gatherUsageStats", "false",
                "--logger.level", "warning"
            ]
            
            # Set environment for the process
            env = os.environ.copy()
            env.update({
                'PYTHONUNBUFFERED': '1',
                'PYTHONIOENCODING': 'utf-8',
                'STREAMLIT_SERVER_MAX_UPLOAD_SIZE': '200'
            })
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                env=env,
                bufsize=1
            )
            
            self.processes.append(("Streamlit", process))
            logger.info(f"✅ Streamlit started on http://{self.config['streamlit']['host']}:{self.config['streamlit']['port']}")
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start Streamlit: {e}")
            return None
    
    def wait_for_services_quick(self):
        """Quick service readiness check."""
        logger.info("⏳ Checking services...")
        
        max_attempts = 15
        
        for attempt in range(max_attempts):
            try:
                # Quick check for FastAPI
                import socket
                
                # Check FastAPI port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                fastapi_ready = sock.connect_ex(('127.0.0.1', self.config['fastapi']['port'])) == 0
                sock.close()
                
                # Check Streamlit port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                streamlit_ready = sock.connect_ex(('127.0.0.1', self.config['streamlit']['port'])) == 0
                sock.close()
                
                if fastapi_ready and streamlit_ready:
                    logger.info("✅ Both services are ready!")
                    return True
                    
                if attempt % 3 == 0:  # Log every 3rd attempt
                    logger.info(f"📡 Services starting... (attempt {attempt + 1})")
                
                time.sleep(1)
                
            except Exception as e:
                logger.debug(f"Service check: {e}")
        
        logger.info("⚠️ Services starting (may need a moment more)")
        return True
    
    def display_same_server_info(self):
        """Display unified server information."""
        print("\n" + "="*70)
        print("🏆 INNOMATICS RESEARCH LABS - SAME SERVER DEPLOYMENT")
        print("📊 RESUME RELEVANCE CHECKER WITH AI INTEGRATION")
        print("="*70)
        print(f"🎯 Main Application:      http://127.0.0.1:{self.config['streamlit']['port']}")
        print(f"🚀 API Backend:           http://127.0.0.1:{self.config['fastapi']['port']}")
        print(f"📚 API Documentation:     http://127.0.0.1:{self.config['fastapi']['port']}/docs")
        print("="*70)
        print("🤖 AI STACK: Ollama 3 + LangChain + spaCy (optimized)")
        print("📈 FEATURES: 1-100 Scoring | Sample Data | Multi-model Analysis")
        print("⚡ MODE: Same-Server Deployment (Optimized Performance)")
        print("="*70)
        print("💡 Press Ctrl+C to stop all services")
        print("🌐 Opening browser automatically...")
        print("="*70 + "\n")
    
    def open_main_app(self):
        """Open the main Streamlit application."""
        try:
            url = f"http://127.0.0.1:{self.config['streamlit']['port']}"
            logger.info(f"🌐 Opening main application: {url}")
            webbrowser.open(url)
            time.sleep(2)
            
            # Also show API docs link
            api_url = f"http://127.0.0.1:{self.config['fastapi']['port']}/docs"
            logger.info(f"📚 API Documentation available at: {api_url}")
            
        except Exception as e:
            logger.error(f"Could not open browser: {e}")
    
    def monitor_lightweight(self):
        """Lightweight process monitoring."""
        while self.running:
            try:
                for service_name, process in self.processes:
                    if process.poll() is not None:
                        logger.error(f"❌ {service_name} stopped unexpectedly")
                        return False
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                return False
        
        return True
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("🛑 Shutdown requested...")
        self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown."""
        self.running = False
        
        for service_name, process in self.processes:
            try:
                logger.info(f"🛑 Stopping {service_name}...")
                process.terminate()
                
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                    
            except Exception as e:
                logger.error(f"Error stopping {service_name}: {e}")
        
        logger.info("🎯 All services stopped")
    
    def launch_same_server(self):
        """Main launch method for same-server deployment."""
        try:
            # Setup signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            logger.info("🚀 Starting Same-Server Resume Relevance Checker...")
            
            # Optimize environment
            self.optimize_environment()
            self.check_system_resources()
            
            # Start FastAPI backend first
            fastapi_process = self.start_fastapi_optimized()
            if not fastapi_process:
                logger.error("❌ Failed to start FastAPI backend")
                return False
            
            # Wait a moment for FastAPI to initialize
            time.sleep(3)
            
            # Start Streamlit frontend
            streamlit_process = self.start_streamlit_optimized()
            if not streamlit_process:
                logger.error("❌ Failed to start Streamlit frontend")
                self.shutdown()
                return False
            
            # Quick service check
            self.wait_for_services_quick()
            
            # Display information
            self.display_same_server_info()
            
            # Open browser
            self.open_main_app()
            
            # Lightweight monitoring
            logger.info("🔄 Monitoring services (same-server mode)...")
            success = self.monitor_lightweight()
            
            if not success:
                logger.error("❌ Service monitoring failed")
                return False
                
            return True
            
        except KeyboardInterrupt:
            logger.info("🛑 Keyboard interrupt received")
            return True
        except Exception as e:
            logger.error(f"❌ Launch error: {e}")
            return False
        finally:
            self.shutdown()

def main():
    """Entry point for same-server deployment."""
    launcher = OptimizedSameServerLauncher()
    success = launcher.launch_same_server()
    
    if success:
        print("\n✅ Application ended successfully")
    else:
        print("\n❌ Application ended with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()