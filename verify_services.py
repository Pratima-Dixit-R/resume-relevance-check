#!/usr/bin/env python3
"""
Simple verification script to check if services are running
"""

import requests
import time

def verify_services():
    """Verify that the required services are running"""
    print("🔍 Verifying Resume AI Analyzer Services")
    print("=" * 40)
    
    # Check FastAPI backend
    print("🔧 Checking FastAPI backend (port 8000)...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ FastAPI is running - {data}")
        else:
            print(f"   ❌ FastAPI returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ FastAPI is not accessible (make sure it's running)")
    except Exception as e:
        print(f"   ❌ Error checking FastAPI: {e}")
    
    # Check Streamlit frontend
    print("\n🎨 Checking Streamlit frontend (port 8501)...")
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("   ✅ Streamlit is running")
        else:
            print(f"   ❌ Streamlit returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Streamlit is not accessible (make sure it's running)")
    except Exception as e:
        print(f"   ❌ Error checking Streamlit: {e}")
    
    print("\n" + "=" * 40)
    print("Verification complete!")

if __name__ == "__main__":
    verify_services()