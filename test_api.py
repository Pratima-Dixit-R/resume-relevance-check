#!/usr/bin/env python3
"""
Quick API test script for deployment verification
"""
import requests
import json

def test_api():
    try:
        # Test health endpoint
        print("🔍 Testing FastAPI health endpoint...")
        health_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        print(f"✅ Health check: {health_response.status_code} - {health_response.json()}")
        
        # Test root endpoint
        print("🔍 Testing root endpoint...")
        root_response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ Root endpoint: {root_response.status_code} - {root_response.json()}")
        
        print("🎉 FastAPI backend is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_streamlit():
    try:
        print("🔍 Testing Streamlit dashboard...")
        streamlit_response = requests.get("http://localhost:8501", timeout=5)
        print(f"✅ Streamlit dashboard: {streamlit_response.status_code} - Dashboard is accessible")
        print("🎉 Streamlit dashboard is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Resume Relevance Check Application")
    print("=" * 50)
    
    api_working = test_api()
    streamlit_working = test_streamlit()
    
    if api_working and streamlit_working:
        print("\n🎉 ALL SERVICES ARE WORKING PERFECTLY!")
        print("✅ Ready for deployment to GitHub!")
    else:
        print("\n⚠️ Some services need attention before deployment")