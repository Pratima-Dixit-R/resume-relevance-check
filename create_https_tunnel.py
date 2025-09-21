"""
HTTPS Tunnel for Streamlit App
Creates a secure HTTPS URL for the local Streamlit application
"""

import subprocess
import time
import threading
import sys
from pyngrok import ngrok
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_ngrok_tunnel():
    """Create HTTPS tunnel for Streamlit app"""
    try:
        # Set up ngrok tunnel to Streamlit app (port 8501)
        public_url = ngrok.connect(8501, "http", bind_tls=True)
        logger.info(f"✅ HTTPS tunnel created successfully!")
        logger.info(f"🌍 Public HTTPS URL: {public_url}")
        logger.info("💡 Share this URL with anyone to access your app securely")
        return public_url
    except Exception as e:
        logger.error(f"❌ Failed to create HTTPS tunnel: {e}")
        return None

def main():
    """Main function to create HTTPS tunnel"""
    print("="*60)
    print("🔐 HTTPS TUNNEL FOR STREAMLIT APP")
    print("="*60)
    print("Creating secure HTTPS URL for your Resume Relevance Checker...")
    print()
    
    # Start ngrok tunnel
    public_url = start_ngrok_tunnel()
    
    if public_url:
        print()
        print("✅ SUCCESS! Your app is now accessible via HTTPS:")
        print(f"   🔗 {public_url}")
        print()
        print("📝 Notes:")
        print("   • This URL is secure (HTTPS)")
        print("   • Share it with anyone to access your app")
        print("   • The tunnel will remain active as long as this script runs")
        print("   • Press Ctrl+C to stop the tunnel")
        print()
        
        # Keep the tunnel alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping HTTPS tunnel...")
            ngrok.kill()
            print("✅ Tunnel stopped")
    else:
        print("❌ Failed to create HTTPS tunnel")
        sys.exit(1)

if __name__ == "__main__":
    main()