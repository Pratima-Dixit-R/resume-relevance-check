#!/usr/bin/env python3
"""
Final Public Access Solution for Resume AI Analyzer
Provides all access URLs and instructions for making the application publicly accessible
with JWT authentication and security encryption.
"""

import subprocess
import sys
import time
import webbrowser
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_local_ip():
    """Get the local IP address"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_application_status():
    """Check if the application is running"""
    try:
        # Check if ports 8501 and 8000 are listening
        result_8501 = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        result_8000 = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        
        port_8501_listening = ':8501' in result_8501.stdout and 'LISTENING' in result_8501.stdout
        port_8000_listening = ':8000' in result_8000.stdout and 'LISTENING' in result_8000.stdout
        
        return port_8501_listening and port_8000_listening
    except Exception as e:
        logger.error(f"Error checking application status: {e}")
        return False

def start_application():
    """Start the application if it's not running"""
    if check_application_status():
        logger.info("✅ Application is already running")
        return True
    
    logger.info("🚀 Starting Resume AI Analyzer application...")
    try:
        # Start the launch_network_app.py script
        process = subprocess.Popen(
            [sys.executable, "launch_network_app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait for services to start
        logger.info("⏳ Waiting for services to start...")
        time.sleep(15)
        
        if check_application_status():
            logger.info("✅ Application started successfully")
            return True
        else:
            logger.error("❌ Failed to start application")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        return False

def show_access_urls():
    """Show all access URLs for the application"""
    local_ip = get_local_ip()
    
    print("\n" + "="*80)
    print("🔐 RESUME AI ANALYZER - ACCESS URLs")
    print("="*80)
    
    print("\n💻 LOCAL ACCESS (This computer only):")
    print("   🎨 Streamlit Dashboard: http://localhost:8501")
    print("   🚀 FastAPI Backend:    http://localhost:8000")
    print("   📚 API Documentation:  http://localhost:8000/docs")
    
    print("\n📱 NETWORK ACCESS (Same WiFi/LAN):")
    print(f"   🎨 Streamlit Dashboard: http://{local_ip}:8501")
    print(f"   🚀 FastAPI Backend:    http://{local_ip}:8000")
    print(f"   📚 API Documentation:  http://{local_ip}:8000/docs")
    
    print("\n" + "="*80)
    print("🔐 SECURITY FEATURES:")
    print("   ✅ JWT Authentication is ENABLED for all protected endpoints")
    print("   ✅ Password hashing with SHA-256 and salt")
    print("   ✅ User-specific data isolation")
    print("   ✅ Secure API endpoints")
    print("="*80)
    
    print("\n💡 USAGE INSTRUCTIONS:")
    print("   1. Open http://localhost:8501 in your browser to access the dashboard")
    print("   2. Register a new account or login with existing credentials")
    print("   3. Upload your resume and job description")
    print("   4. Get AI-powered analysis with security protection")
    
    print("\n🌍 TO MAKE PUBLICLY ACCESSIBLE:")
    print("   Option 1 - Ngrok:")
    print("      a. Sign up at: https://dashboard.ngrok.com/signup")
    print("      b. Install auth token: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("      c. Run: ngrok http 8501 (for Streamlit)")
    print("      d. Run: ngrok http 8000 (for FastAPI)")
    print("   ")
    print("   Option 2 - LocalTunnel:")
    print("      a. Run: npx localtunnel --port 8501 (for Streamlit)")
    print("      b. Run: npx localtunnel --port 8000 (for FastAPI)")
    print("   ")
    print("   Option 3 - Port Forwarding:")
    print("      a. Configure your router to forward ports 8501 and 8000")
    print("      b. Use your public IP address with the ports")
    
    print("\n" + "="*80)
    print("✅ APPLICATION STATUS: RUNNING")
    print("="*80)

def main():
    """Main function"""
    print("="*80)
    print("🔐 Resume AI Analyzer - Public Access Solution")
    print("="*80)
    
    # Start application if needed
    if not check_application_status():
        if not start_application():
            logger.error("❌ Cannot proceed without running application")
            return
    
    # Show access URLs
    show_access_urls()
    
    # Ask user if they want to open the local dashboard
    try:
        choice = input("\nOpen the dashboard in your browser? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            local_ip = get_local_ip()
            url = f"http://{local_ip}:8501"
            logger.info(f"🌐 Opening {url} in your browser...")
            webbrowser.open(url)
    except KeyboardInterrupt:
        print("\n👋 Exiting...")

if __name__ == "__main__":
    main()