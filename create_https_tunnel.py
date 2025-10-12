#!/usr/bin/env python3
"""
Script to create HTTPS tunnels for the Resume AI Analyzer application.
This script provides options to use either ngrok or localtunnel for creating public HTTPS URLs.
"""

import subprocess
import sys
import time
import requests
import threading
from pathlib import Path

def check_ngrok_installed():
    """Check if ngrok is installed."""
    try:
        result = subprocess.run(['ngrok', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_localtunnel_installed():
    """Check if localtunnel is installed."""
    try:
        result = subprocess.run(['npx', 'localtunnel', '--help'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok():
    """Install ngrok using pip."""
    print("Installing ngrok...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyngrok'], check=True)
        print("✅ ngrok installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install ngrok")
        return False

def install_localtunnel():
    """Install localtunnel using npm."""
    print("Installing localtunnel...")
    try:
        subprocess.run(['npm', 'install', '-g', 'localtunnel'], check=True)
        print("✅ localtunnel installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install localtunnel")
        return False

def start_ngrok_tunnel(port):
    """Start ngrok tunnel for the specified port."""
    try:
        # Try to import pyngrok
        from pyngrok import ngrok
    except ImportError:
        print("ngrok library not found. Installing...")
        if not install_ngrok():
            return None
        from pyngrok import ngrok
    
    try:
        # Set auth token if available (optional)
        # ngrok.set_auth_token("your_auth_token_here")
        
        # Start tunnel
        public_url = ngrok.connect(port, "http")
        print(f"✅ ngrok tunnel started!")
        print(f"🌐 Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Failed to start ngrok tunnel: {e}")
        return None

def start_localtunnel(port):
    """Start localtunnel for the specified port."""
    try:
        # Start localtunnel
        result = subprocess.Popen([
            'npx', 'localtunnel', '--port', str(port)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for tunnel to start
        time.sleep(3)
        
        # Try to get the public URL
        try:
            # Read the output to find the URL
            output_lines = []
            for line in iter(result.stdout.readline, ''):
                output_lines.append(line.strip())
                if 'your url is:' in line.lower():
                    public_url = line.split('your url is:')[-1].strip()
                    print(f"✅ localtunnel started!")
                    print(f"🌐 Public URL: {public_url}")
                    return public_url, result
                if len(output_lines) > 10:  # Stop after 10 lines if no URL found
                    break
        except Exception:
            pass
            
        # If we couldn't parse the URL, just return the process
        print("✅ localtunnel started! Check the output for the public URL.")
        return f"http://localhost:{port} (localtunnel running)", result
        
    except Exception as e:
        print(f"❌ Failed to start localtunnel: {e}")
        return None, None

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

def main():
    """Main function to create HTTPS tunnels."""
    print("🔐 Resume AI Analyzer - HTTPS Tunnel Creator")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"🌐 Local IP Address: {local_ip}")
    
    print("\nAvailable services:")
    print("1. Streamlit Frontend (port 8501)")
    print("2. FastAPI Backend (port 8000)")
    
    try:
        choice = input("\nSelect service to expose (1 or 2): ").strip()
        if choice == "1":
            port = 8501
            service_name = "Streamlit Frontend"
        elif choice == "2":
            port = 8000
            service_name = "FastAPI Backend"
        else:
            print("❌ Invalid choice")
            return
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        return
    
    print(f"\nSelected: {service_name} on port {port}")
    
    print("\nTunneling options:")
    print("1. ngrok (requires account for persistent URLs)")
    print("2. localtunnel (no account required)")
    
    try:
        tunnel_choice = input("\nSelect tunneling service (1 or 2): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        return
    
    if tunnel_choice == "1":
        # ngrok
        print("\n🚀 Starting ngrok tunnel...")
        if not check_ngrok_installed():
            print("ngrok not found. Would you like to install it? (y/n): ", end="")
            if input().lower() == 'y':
                if not install_ngrok():
                    return
            else:
                print("❌ ngrok is required for this option")
                return
        
        public_url = start_ngrok_tunnel(port)
        if public_url:
            print(f"\n🎉 Success! Your {service_name} is now accessible at:")
            print(f"   🔗 {public_url}")
            print(f"\n💡 Local access:")
            print(f"   🖥️  http://localhost:{port}")
            print(f"   📱 http://{local_ip}:{port}")
            print(f"\nPress Ctrl+C to stop the tunnel...")
            try:
                # Keep the tunnel alive
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Stopping tunnel...")
                try:
                    from pyngrok import ngrok
                    ngrok.kill()
                except:
                    pass
        else:
            print("❌ Failed to create ngrok tunnel")
            
    elif tunnel_choice == "2":
        # localtunnel
        print("\n🚀 Starting localtunnel...")
        if not check_localtunnel_installed():
            print("localtunnel not found. Would you like to install it? (y/n): ", end="")
            if input().lower() == 'y':
                if not install_localtunnel():
                    return
            else:
                print("❌ localtunnel is required for this option")
                return
        
        public_url, process = start_localtunnel(port)
        if public_url:
            print(f"\n🎉 Success! Your {service_name} is now accessible!")
            print(f"   🔗 {public_url}")
            print(f"\n💡 Local access:")
            print(f"   🖥️  http://localhost:{port}")
            print(f"   📱 http://{local_ip}:{port}")
            print(f"\nPress Ctrl+C to stop the tunnel...")
            try:
                # Keep the tunnel alive
                if process:
                    process.wait()
                else:
                    while True:
                        time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Stopping tunnel...")
                if process:
                    process.terminate()
        else:
            print("❌ Failed to create localtunnel")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()