#!/usr/bin/env python3
"""
Unified Application Launcher for Resume Relevance Checker
Innomatics Research Labs

Launches both Streamlit frontend and FastAPI backend on the same server
with proper process management and unified access.
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnifiedLauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.venv_python = self.base_path / "venv" / "Scripts" / "python.exe"
        self.processes = []
        self.running = True
        
        # Configuration
        self.config = {
            "fastapi": {
                "host": "0.0.0.0",
                "port": 8000,
                "module": "src.api.main:app"
            },
            "streamlit": {
                "host": "0.0.0.0", 
                "port": 8501,
                "script": "src/dashboard/streamlit_app.py"
            }
        }
    
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        logger.info("Checking dependencies...")
        
        try:
            # Check virtual environment
            if not self.venv_python.exists():
                logger.error("Virtual environment not found. Please run setup first.")
                return False
            
            # Check key packages
            result = subprocess.run([
                str(self.venv_python), "-c", 
                "import streamlit, fastapi, ollama, langchain; print('Dependencies OK')"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Dependency check failed: {result.stderr}")
                return False
                
            logger.info("✅ All dependencies verified")
            return True
            
        except Exception as e:
            logger.error(f"Error checking dependencies: {e}")
            return False
    
    def start_fastapi(self):
        """Start FastAPI backend server."""
        logger.info("🚀 Starting FastAPI backend...")
        
        try:
            cmd = [
                str(self.venv_python), "-m", "uvicorn",
                self.config["fastapi"]["module"],
                "--host", self.config["fastapi"]["host"],
                "--port", str(self.config["fastapi"]["port"]),
                "--reload",
                "--log-level", "info"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes.append(("FastAPI", process))
            logger.info(f"✅ FastAPI started on http://{self.config['fastapi']['host']}:{self.config['fastapi']['port']}")
            
            # Monitor output in thread
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, "FastAPI"),
                daemon=True
            ).start()
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start FastAPI: {e}")
            return None
    
    def start_streamlit(self):
        """Start Streamlit frontend server.""" 
        logger.info("🎨 Starting Streamlit frontend...")
        
        try:
            cmd = [
                str(self.venv_python), "-m", "streamlit", "run",
                self.config["streamlit"]["script"],
                "--server.address", self.config["streamlit"]["host"],
                "--server.port", str(self.config["streamlit"]["port"]),
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes.append(("Streamlit", process))
            logger.info(f"✅ Streamlit started on http://{self.config['streamlit']['host']}:{self.config['streamlit']['port']}")
            
            # Monitor output in thread
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, "Streamlit"),
                daemon=True
            ).start()
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start Streamlit: {e}")
            return None
    
    def _monitor_process_output(self, process, service_name):
        """Monitor process output and log important messages."""
        try:
            while self.running and process.poll() is None:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if any(keyword in line.lower() for keyword in ['error', 'failed', 'exception']):
                        logger.error(f"[{service_name}] {line}")
                    elif any(keyword in line.lower() for keyword in ['started', 'running', 'ready']):
                        logger.info(f"[{service_name}] {line}")
        except Exception as e:
            logger.error(f"Error monitoring {service_name}: {e}")
    
    def wait_for_services(self):
        """Wait for both services to be ready."""
        logger.info("⏳ Waiting for services to be ready...")
        
        max_attempts = 30
        fastapi_ready = False
        streamlit_ready = False
        
        for attempt in range(max_attempts):
            try:
                # Check FastAPI
                if not fastapi_ready:
                    import requests
                    try:
                        response = requests.get(f"http://localhost:{self.config['fastapi']['port']}/health", timeout=2)
                        if response.status_code == 200:
                            fastapi_ready = True
                            logger.info("✅ FastAPI backend is ready")
                    except:
                        pass
                
                # Check Streamlit (simple port check)
                if not streamlit_ready:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('localhost', self.config['streamlit']['port']))
                    sock.close()
                    if result == 0:
                        streamlit_ready = True
                        logger.info("✅ Streamlit frontend is ready")
                
                if fastapi_ready and streamlit_ready:
                    logger.info("🎉 All services are ready!")
                    return True
                    
                time.sleep(2)
                
            except Exception as e:
                logger.debug(f"Service check attempt {attempt + 1}: {e}")
        
        logger.warning("⚠️ Services may not be fully ready, but continuing...")
        return True
    
    def open_browser(self):
        """Open browser to the application."""
        try:
            url = f"http://localhost:{self.config['streamlit']['port']}"
            logger.info(f"🌐 Opening browser to {url}")
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
    
    def display_info(self):
        """Display application information."""
        print("\n" + "="*60)
        print("🏆 INNOMATICS RESEARCH LABS")
        print("📊 RESUME RELEVANCE CHECKER - UNIFIED LAUNCHER")
        print("="*60)
        print(f"🎨 Frontend (Streamlit): http://localhost:{self.config['streamlit']['port']}")
        print(f"🚀 Backend (FastAPI):    http://localhost:{self.config['fastapi']['port']}")
        print(f"📚 API Documentation:    http://localhost:{self.config['fastapi']['port']}/docs")
        print("="*60)
        print("🤖 AI Technologies: Ollama 3, LangChain, Hugging Face, spaCy")
        print("📋 Features: 1-100 Scoring, Sample Data, Multi-model Analysis")
        print("="*60)
        print("💡 Press Ctrl+C to stop all services")
        print("="*60 + "\n")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("🛑 Shutdown signal received. Stopping services...")
        self.shutdown()
    
    def shutdown(self):
        """Shutdown all services gracefully."""
        self.running = False
        
        for service_name, process in self.processes:
            try:
                logger.info(f"🛑 Stopping {service_name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Force killing {service_name}...")
                    process.kill()
                    process.wait()
                    
                logger.info(f"✅ {service_name} stopped")
                
            except Exception as e:
                logger.error(f"Error stopping {service_name}: {e}")
        
        logger.info("🎯 All services stopped successfully")
    
    def launch(self):
        """Main launch method."""
        try:
            # Setup signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            logger.info("🚀 Starting Resume Relevance Checker...")
            
            # Check dependencies
            if not self.check_dependencies():
                sys.exit(1)
            
            # Start services
            fastapi_process = self.start_fastapi()
            if not fastapi_process:
                logger.error("Failed to start FastAPI backend")
                sys.exit(1)
            
            # Small delay between services
            time.sleep(3)
            
            streamlit_process = self.start_streamlit()
            if not streamlit_process:
                logger.error("Failed to start Streamlit frontend")
                self.shutdown()
                sys.exit(1)
            
            # Wait for services to be ready
            self.wait_for_services()
            
            # Display information
            self.display_info()
            
            # Open browser
            self.open_browser()
            
            # Keep running until interrupted
            logger.info("🔄 Services running. Monitoring for shutdown signal...")
            
            while self.running:
                # Check if processes are still alive
                for service_name, process in self.processes:
                    if process.poll() is not None:
                        logger.error(f"❌ {service_name} has stopped unexpectedly")
                        self.shutdown()
                        sys.exit(1)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Keyboard interrupt received")
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
        finally:
            self.shutdown()

if __name__ == "__main__":
    launcher = UnifiedLauncher()
    launcher.launch()#!/usr/bin/env python3
"""
Unified Application Launcher for Resume Relevance Checker
Innomatics Research Labs

Launches both Streamlit frontend and FastAPI backend on the same server
with proper process management and unified access.
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnifiedLauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.venv_python = self.base_path / "venv" / "Scripts" / "python.exe"
        self.processes = []
        self.running = True
        
        # Configuration
        self.config = {
            "fastapi": {
                "host": "0.0.0.0",
                "port": 8000,
                "module": "src.api.main:app"
            },
            "streamlit": {
                "host": "0.0.0.0", 
                "port": 8501,
                "script": "src/dashboard/streamlit_app.py"
            }
        }
    
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        logger.info("Checking dependencies...")
        
        try:
            # Check virtual environment
            if not self.venv_python.exists():
                logger.error("Virtual environment not found. Please run setup first.")
                return False
            
            # Check key packages
            result = subprocess.run([
                str(self.venv_python), "-c", 
                "import streamlit, fastapi, ollama, langchain; print('Dependencies OK')"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Dependency check failed: {result.stderr}")
                return False
                
            logger.info("✅ All dependencies verified")
            return True
            
        except Exception as e:
            logger.error(f"Error checking dependencies: {e}")
            return False
    
    def start_fastapi(self):
        """Start FastAPI backend server."""
        logger.info("🚀 Starting FastAPI backend...")
        
        try:
            cmd = [
                str(self.venv_python), "-m", "uvicorn",
                self.config["fastapi"]["module"],
                "--host", self.config["fastapi"]["host"],
                "--port", str(self.config["fastapi"]["port"]),
                "--reload",
                "--log-level", "info"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes.append(("FastAPI", process))
            logger.info(f"✅ FastAPI started on http://{self.config['fastapi']['host']}:{self.config['fastapi']['port']}")
            
            # Monitor output in thread
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, "FastAPI"),
                daemon=True
            ).start()
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start FastAPI: {e}")
            return None
    
    def start_streamlit(self):
        """Start Streamlit frontend server.""" 
        logger.info("🎨 Starting Streamlit frontend...")
        
        try:
            cmd = [
                str(self.venv_python), "-m", "streamlit", "run",
                self.config["streamlit"]["script"],
                "--server.address", self.config["streamlit"]["host"],
                "--server.port", str(self.config["streamlit"]["port"]),
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes.append(("Streamlit", process))
            logger.info(f"✅ Streamlit started on http://{self.config['streamlit']['host']}:{self.config['streamlit']['port']}")
            
            # Monitor output in thread
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, "Streamlit"),
                daemon=True
            ).start()
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start Streamlit: {e}")
            return None
    
    def _monitor_process_output(self, process, service_name):
        """Monitor process output and log important messages."""
        try:
            while self.running and process.poll() is None:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if any(keyword in line.lower() for keyword in ['error', 'failed', 'exception']):
                        logger.error(f"[{service_name}] {line}")
                    elif any(keyword in line.lower() for keyword in ['started', 'running', 'ready']):
                        logger.info(f"[{service_name}] {line}")
        except Exception as e:
            logger.error(f"Error monitoring {service_name}: {e}")
    
    def wait_for_services(self):
        """Wait for both services to be ready."""
        logger.info("⏳ Waiting for services to be ready...")
        
        max_attempts = 30
        fastapi_ready = False
        streamlit_ready = False
        
        for attempt in range(max_attempts):
            try:
                # Check FastAPI
                if not fastapi_ready:
                    import requests
                    try:
                        response = requests.get(f"http://localhost:{self.config['fastapi']['port']}/health", timeout=2)
                        if response.status_code == 200:
                            fastapi_ready = True
                            logger.info("✅ FastAPI backend is ready")
                    except:
                        pass
                
                # Check Streamlit (simple port check)
                if not streamlit_ready:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('localhost', self.config['streamlit']['port']))
                    sock.close()
                    if result == 0:
                        streamlit_ready = True
                        logger.info("✅ Streamlit frontend is ready")
                
                if fastapi_ready and streamlit_ready:
                    logger.info("🎉 All services are ready!")
                    return True
                    
                time.sleep(2)
                
            except Exception as e:
                logger.debug(f"Service check attempt {attempt + 1}: {e}")
        
        logger.warning("⚠️ Services may not be fully ready, but continuing...")
        return True
    
    def open_browser(self):
        """Open browser to the application."""
        try:
            url = f"http://localhost:{self.config['streamlit']['port']}"
            logger.info(f"🌐 Opening browser to {url}")
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
    
    def display_info(self):
        """Display application information."""
        print("\n" + "="*60)
        print("🏆 INNOMATICS RESEARCH LABS")
        print("📊 RESUME RELEVANCE CHECKER - UNIFIED LAUNCHER")
        print("="*60)
        print(f"🎨 Frontend (Streamlit): http://localhost:{self.config['streamlit']['port']}")
        print(f"🚀 Backend (FastAPI):    http://localhost:{self.config['fastapi']['port']}")
        print(f"📚 API Documentation:    http://localhost:{self.config['fastapi']['port']}/docs")
        print("="*60)
        print("🤖 AI Technologies: Ollama 3, LangChain, Hugging Face, spaCy")
        print("📋 Features: 1-100 Scoring, Sample Data, Multi-model Analysis")
        print("="*60)
        print("💡 Press Ctrl+C to stop all services")
        print("="*60 + "\n")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("🛑 Shutdown signal received. Stopping services...")
        self.shutdown()
    
    def shutdown(self):
        """Shutdown all services gracefully."""
        self.running = False
        
        for service_name, process in self.processes:
            try:
                logger.info(f"🛑 Stopping {service_name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Force killing {service_name}...")
                    process.kill()
                    process.wait()
                    
                logger.info(f"✅ {service_name} stopped")
                
            except Exception as e:
                logger.error(f"Error stopping {service_name}: {e}")
        
        logger.info("🎯 All services stopped successfully")
    
    def launch(self):
        """Main launch method."""
        try:
            # Setup signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            logger.info("🚀 Starting Resume Relevance Checker...")
            
            # Check dependencies
            if not self.check_dependencies():
                sys.exit(1)
            
            # Start services
            fastapi_process = self.start_fastapi()
            if not fastapi_process:
                logger.error("Failed to start FastAPI backend")
                sys.exit(1)
            
            # Small delay between services
            time.sleep(3)
            
            streamlit_process = self.start_streamlit()
            if not streamlit_process:
                logger.error("Failed to start Streamlit frontend")
                self.shutdown()
                sys.exit(1)
            
            # Wait for services to be ready
            self.wait_for_services()
            
            # Display information
            self.display_info()
            
            # Open browser
            self.open_browser()
            
            # Keep running until interrupted
            logger.info("🔄 Services running. Monitoring for shutdown signal...")
            
            while self.running:
                # Check if processes are still alive
                for service_name, process in self.processes:
                    if process.poll() is not None:
                        logger.error(f"❌ {service_name} has stopped unexpectedly")
                        self.shutdown()
                        sys.exit(1)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Keyboard interrupt received")
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
        finally:
            self.shutdown()

if __name__ == "__main__":
    launcher = UnifiedLauncher()
    launcher.launch()