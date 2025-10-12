#!/usr/bin/env python3
"""
Simple Tunnel Creator for Resume AI Analyzer
Creates secure HTTPS tunnels using either ngrok or localtunnel for the already running application
with JWT authentication and security encryption.
"""

import subprocess
import sys
import time
import webbrowser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_ngrok_tunnel():
    """Create ngrok tunnel for both FastAPI and Streamlit"""
    try:
        from pyngrok import ngrok
        
        logger.info("🔗 Creating ngrok tunnels...")
        
        # Kill any existing ngrok processes
        try:
            ngrok.kill()
        except:
            pass
        
        # Set up ngrok tunnel for Streamlit (port 8501)
        streamlit_tunnel = ngrok.connect(8501, "http")
        streamlit_public_url = streamlit_tunnel.public_url
        logger.info(f"🎨 Streamlit Public URL: {streamlit_public_url}")
        
        # Set up ngrok tunnel for FastAPI (port 8000)
        fastapi_tunnel = ngrok.connect(8000, "http")
        fastapi_public_url = fastapi_tunnel.public_url
        logger.info(f"🚀 FastAPI Public URL: {fastapi_public_url}")
        
        # Display API documentation URL
        api_docs_url = f"{fastapi_public_url}/docs"
        logger.info(f"📚 API Documentation: {api_docs_url}")
        
        print("\n" + "="*80)
        print("🌍 PUBLIC ACCESS URLs (ngrok)")
        print("="*80)
        print(f"🎨 Streamlit Dashboard: {streamlit_public_url}")
        print(f"🚀 FastAPI Backend:     {fastapi_public_url}")
        print(f"📚 API Documentation:   {api_docs_url}")
        print("="*80)
        print("🔐 JWT Authentication is ENABLED")
        print("💡 Share these URLs with anyone to access your application remotely")
        print("💡 Works on both laptops and mobile devices")
        print("="*80)
        
        # Open the Streamlit URL in browser
        logger.info(f"🌐 Opening {streamlit_public_url} in your browser...")
        try:
            webbrowser.open(streamlit_public_url)
        except:
            logger.warning("Could not open browser automatically")
        
        return streamlit_tunnel, fastapi_tunnel, streamlit_public_url, fastapi_public_url
        
    except Exception as e:
        logger.error(f"❌ Failed to create ngrok tunnel: {e}")
        return None, None, None, None

def create_localtunnel():
    """Create localtunnel for both FastAPI and Streamlit"""
    try:
        logger.info("🔗 Creating localtunnel connections...")
        
        # Start localtunnel for Streamlit (port 8501) in background
        print("Starting localtunnel for Streamlit on port 8501...")
        streamlit_cmd = ["npx", "localtunnel", "--port", "8501"]
        streamlit_process = subprocess.Popen(
            streamlit_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Start localtunnel for FastAPI (port 8000) in background
        print("Starting localtunnel for FastAPI on port 8000...")
        fastapi_cmd = ["npx", "localtunnel", "--port", "8000"]
        fastapi_process = subprocess.Popen(
            fastapi_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait for tunnels to establish
        print("Waiting for tunnels to establish...")
        time.sleep(8)
        
        # Try to get URLs by checking the process output
        try:
            # Check if we can read the URLs from stdout
            streamlit_output = ""
            fastapi_output = ""
            
            # Read available output
            try:
                streamlit_output = streamlit_process.stdout.readline()
                if not streamlit_output:
                    # Try to peek at the output
                    streamlit_process.poll()
            except:
                pass
                
            try:
                fastapi_output = fastapi_process.stdout.readline()
                if not fastapi_output:
                    # Try to peek at the output
                    fastapi_process.poll()
            except:
                pass
            
            print(f"Streamlit tunnel output: {streamlit_output}")
            print(f"FastAPI tunnel output: {fastapi_output}")
            
            # Extract URLs if available
            streamlit_url = "http://localhost:8501 (check terminal for localtunnel URL)"
            fastapi_url = "http://localhost:8000 (check terminal for localtunnel URL)"
            
            if "your url is:" in streamlit_output.lower():
                streamlit_url = streamlit_output.split("your url is:")[-1].strip()
                
            if "your url is:" in fastapi_output.lower():
                fastapi_url = fastapi_output.split("your url is:")[-1].strip()
            
            logger.info(f"🎨 Streamlit Public URL: {streamlit_url}")
            logger.info(f"🚀 FastAPI Public URL: {fastapi_url}")
            
            # Display API documentation URL
            if "http" in fastapi_url and "localhost" not in fastapi_url:
                api_docs_url = f"{fastapi_url}/docs"
                logger.info(f"📚 API Documentation: {api_docs_url}")
            
            print("\n" + "="*80)
            print("🌍 PUBLIC ACCESS URLs (localtunnel)")
            print("="*80)
            print(f"🎨 Streamlit Dashboard: {streamlit_url}")
            print(f"🚀 FastAPI Backend:     {fastapi_url}")
            if "http" in fastapi_url and "localhost" not in fastapi_url:
                print(f"📚 API Documentation:   {api_docs_url}")
            print("="*80)
            print("🔐 JWT Authentication is ENABLED")
            print("💡 Share these URLs with anyone to access your application remotely")
            print("💡 Works on both laptops and mobile devices")
            print("="*80)
            
            # Open the Streamlit URL in browser (if we have a proper URL)
            if "http" in streamlit_url and "localhost" not in streamlit_url:
                logger.info(f"🌐 Opening {streamlit_url} in your browser...")
                try:
                    webbrowser.open(streamlit_url)
                except:
                    logger.warning("Could not open browser automatically")
            
            return streamlit_process, fastapi_process, streamlit_url, fastapi_url
            
        except Exception as e:
            logger.error(f"Error reading tunnel output: {e}")
            # Still return the processes
            return streamlit_process, fastapi_process, "Check terminal for URL", "Check terminal for URL"
        
    except Exception as e:
        logger.error(f"❌ Failed to create localtunnel: {e}")
        return None, None, None, None

def main():
    """Main function to create public URLs for the running application"""
    print("="*80)
    print("🔐 Resume AI Analyzer - Public Tunnel Creator")
    print("="*80)
    print("Application should already be running on:")
    print("  🎨 Streamlit Dashboard: http://localhost:8501")
    print("  🚀 FastAPI Backend:     http://localhost:8000")
    print("="*80)
    
    print("\nTunneling Options:")
    print("1. ngrok (requires account for persistent URLs)")
    print("2. localtunnel (no account required)")
    print("3. Exit")
    
    try:
        choice = input("\nSelect tunneling service (1, 2, or 3): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        return
    
    if choice == "3":
        print("👋 Exiting...")
        return
    
    if choice == "1":
        # Create ngrok tunnels
        logger.info("🔗 Creating secure tunnels with ngrok...")
        streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url = create_ngrok_tunnel()
        
        if not streamlit_tunnel or not fastapi_tunnel:
            logger.error("❌ Failed to create ngrok tunnels")
            return
            
        # Keep the tunnels alive
        try:
            print("\n🔄 Tunnels are active! Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down tunnels...")
            try:
                from pyngrok import ngrok
                ngrok.kill()
            except:
                pass
            logger.info("✅ Tunnels stopped")
            
    elif choice == "2":
        # Create localtunnel connections
        logger.info("🔗 Creating secure tunnels with localtunnel...")
        streamlit_tunnel, fastapi_tunnel, streamlit_url, fastapi_url = create_localtunnel()
        
        if not streamlit_tunnel or not fastapi_tunnel:
            logger.error("❌ Failed to create localtunnel connections")
            return
            
        # Keep the tunnels alive
        try:
            print("\n🔄 Tunnels are active! Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down tunnels...")
            if streamlit_tunnel:
                streamlit_tunnel.terminate()
            if fastapi_tunnel:
                fastapi_tunnel.terminate()
            logger.info("✅ Tunnels stopped")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()