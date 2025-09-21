"""
HTTPS URL Generator for Streamlit App
Provides multiple options for creating HTTPS URLs for local applications
"""

import webbrowser
import time
import sys
import subprocess
import os

def print_https_options():
    """Print all available options for creating HTTPS URLs"""
    print("="*80)
    print("🔐 HTTPS URL OPTIONS FOR YOUR STREAMLIT APP")
    print("="*80)
    print()
    print("Your Streamlit app is currently running at: http://127.0.0.1:8501")
    print()
    print("Here are several options to create an HTTPS URL:")
    print()
    
    print("✅ OPTION 1: Use Ngrok (Recommended)")
    print("   1. Sign up for a free account at: https://dashboard.ngrok.com/signup")
    print("   2. Install ngrok: Download from https://ngrok.com/download")
    print("   3. Authenticate: ngrok config add-authtoken YOUR_AUTH_TOKEN")
    print("   4. Create tunnel: ngrok http 8501")
    print("   5. You'll get an HTTPS URL like: https://abcd-efgh-1234.ngrok.io")
    print()
    
    print("✅ OPTION 2: Use Cloudflared (Cloudflare Tunnel)")
    print("   1. Download cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/")
    print("   2. Run: cloudflared tunnel --url http://localhost:8501")
    print("   3. You'll get a temporary HTTPS URL")
    print()
    
    print("✅ OPTION 3: Use LocalTunnel (if npm is available)")
    print("   1. Install Node.js from: https://nodejs.org/")
    print("   2. Install localtunnel: npm install -g localtunnel")
    print("   3. Create tunnel: npx localtunnel --port 8501")
    print("   4. You'll get an HTTPS URL")
    print()
    
    print("📱 LOCAL ACCESS (works immediately):")
    print("   HTTP:  http://127.0.0.1:8501")
    print("   HTTP:  http://localhost:8501")
    print()
    
    print("💡 TIPS:")
    print("   • For immediate testing, use the local HTTP URLs above")
    print("   • For sharing with others, use one of the tunneling services")
    print("   • Ngrok is the most popular and reliable option")
    print("   • All tunneling services provide temporary HTTPS URLs")
    print()
    print("="*80)

def open_local_urls():
    """Open local URLs in browser"""
    urls = [
        "http://127.0.0.1:8501",
        "http://localhost:8501"
    ]
    
    print("Opening local URLs in your browser...")
    for url in urls:
        try:
            webbrowser.open(url)
            print(f"   🔗 Opened: {url}")
        except Exception as e:
            print(f"   ❌ Failed to open {url}: {e}")
    print()

def main():
    """Main function"""
    print_https_options()
    print()
    open_local_urls()
    
    print("📋 NEXT STEPS:")
    print("   1. For immediate access, use the local URLs opened in your browser")
    print("   2. For HTTPS, follow one of the tunneling options above")
    print("   3. Ngrok is recommended for the best experience")
    print()
    print("💡 Need help setting up ngrok? Visit: https://ngrok.com/docs/getting-started/")

if __name__ == "__main__":
    main()