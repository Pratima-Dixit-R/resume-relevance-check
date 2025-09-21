#!/usr/bin/env python3
"""
App URLs Display Script
Shows the local URLs where the Resume Relevance Checker app is running.
"""

def display_app_urls():
    """Display the URLs for accessing the Resume Relevance Checker app."""
    print("=" * 60)
    print("🚀 RESUME RELEVANCE CHECKER - APP URLs")
    print("=" * 60)
    
    print("\n✅ BACKEND (FastAPI):")
    print("   Local URL: http://127.0.0.1:8000")
    print("   Network URL: http://10.13.251.5:8000")
    print("   Docs: http://127.0.0.1:8000/docs")
    print("   Health Check: http://127.0.0.1:8000/health")
    
    print("\n✅ FRONTEND (Streamlit):")
    print("   Local URL: http://localhost:8501")
    print("   Network URL: http://10.13.251.5:8501")
    
    print("\n💡 USAGE:")
    print("   1. Open the Streamlit frontend URL in your browser")
    print("   2. Upload a resume and job description")
    print("   3. Get AI-powered relevance analysis")
    
    print("\n🔒 HTTPS OPTIONS:")
    print("   For HTTPS access, you can use:")
    print("   - cloudflared tunnel --url http://localhost:8501")
    print("   - lt --port 8501 (localtunnel)")
    print("   - ngrok http 8501 (requires account)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    display_app_urls()
