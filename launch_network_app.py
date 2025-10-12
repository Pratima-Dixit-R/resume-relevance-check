import subprocess
import threading
import time
import webbrowser
import socket
from pathlib import Path

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback to ipconfig parsing
        try:
            import subprocess
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'IPv4 Address' in line and '192.168.' in line:
                    return line.split(':')[-1].strip()
        except Exception:
            return "127.0.0.1"

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    backend_process = subprocess.Popen([
        "python", "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])
    print("✅ FastAPI backend started on http://0.0.0.0:8000")
    return backend_process

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    frontend_process = subprocess.Popen([
        "streamlit", "run", 
        "src/dashboard/streamlit_app.py", 
        "--server.address", "0.0.0.0",
        "--server.port", "8501"
    ])
    print("✅ Streamlit frontend started on http://0.0.0.0:8501")
    return frontend_process

def main():
    print("🔐 Resume Relevance Checker - Network Launcher")
    print("=" * 50)
    
    # Get local IP for network access
    local_ip = get_local_ip()
    print(f"🌐 Local IP Address: {local_ip}")
    
    # Start backend and frontend
    try:
        backend_process = start_backend()
        time.sleep(3)  # Give backend time to start
        
        frontend_process = start_frontend()
        time.sleep(5)  # Give frontend time to start
        
        print("\n" + "=" * 50)
        print("🏆 RESUME RELEVANCE CHECKER - NETWORK ACCESS")
        print("=" * 50)
        print("💻 LOCAL ACCESS (This computer only):")
        print(f"   🎨 Streamlit Dashboard: http://localhost:8501")
        print(f"   🚀 FastAPI Backend:    http://localhost:8000")
        print(f"   📚 API Documentation:  http://localhost:8000/docs")
        print("\n📱 NETWORK ACCESS (Same WiFi/LAN):")
        print(f"   🎨 Streamlit Dashboard: http://{local_ip}:8501")
        print(f"   🚀 FastAPI Backend:    http://{local_ip}:8000")
        print(f"   📚 API Documentation:  http://{local_ip}:8000/docs")
        print("\n🌍 PUBLIC ACCESS INFORMATION:")
        print("   🔧 To access from the internet, you need to:")
        print("      1. Configure port forwarding on your router for ports 8501 and 8000")
        print("      2. Or use a tunneling service like ngrok or localtunnel")
        print("\n💡 TIPS FOR SHARING:")
        print("   • For local sharing (same WiFi): Use the NETWORK ACCESS URLs")
        print("   • For internet sharing: Use a tunneling service or configure port forwarding")
        print("   • Make sure your firewall allows connections on ports 8501 and 8000")
        print("=" * 50)
        
        # Open local URL in browser
        print("\n🌐 Opening local URL in your browser...")
        webbrowser.open(f"http://localhost:8501")
        
        print("\n🔄 Application is running! Press Ctrl+C to stop.")
        
        # Wait for processes
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down services...")
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
            print("✅ All services stopped")
            
    except Exception as e:
        print(f"❌ Error starting services: {e}")

if __name__ == "__main__":
    main()