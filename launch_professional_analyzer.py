#!/usr/bin/env python3
"""
Launch script for Professional AI Resume Analyzer
This script launches the professional resume analyzer application locally for testing.
"""

import subprocess
import sys
import os
from pathlib import Path

def launch_application():
    """Launch the Professional AI Resume Analyzer application."""
    print("🚀 Launching Professional AI Resume Analyzer...")
    print("This may take a few moments to initialize...")
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Launch the Streamlit application
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "professional_resume_analyzer.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    try:
        print("🌐 Starting Streamlit application...")
        print("📝 Access the application at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the application")
        
        # Run the Streamlit application
        process = subprocess.Popen(cmd)
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping the application...")
        if 'process' in locals():
            process.terminate()
            process.wait()
        print("✅ Application stopped.")
        
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    launch_application()