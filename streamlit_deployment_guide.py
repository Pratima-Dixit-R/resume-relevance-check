#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Guide
This script provides step-by-step instructions for deploying to your own Streamlit Cloud account.
"""

import webbrowser
import time

def show_deployment_guide():
    """Show step-by-step deployment guide."""
    print("=" * 80)
    print("🚀 STREAMLIT CLOUD DEPLOYMENT GUIDE")
    print("=" * 80)
    
    print("\n📋 DEPLOYMENT STEPS:")
    print("1. Visit Streamlit Cloud: https://share.streamlit.io/")
    print("2. Sign in with YOUR GitHub account")
    print("3. Click 'New app'")
    print("4. Select your repository: Pratima-Dixit-R/resume-relevance-check")
    print("5. Set these options:")
    print("   - Branch: main")
    print("   - Main file path: resume_analyzer.py")
    print("   - Requirements file: requirements_streamlit.txt")
    print("6. Click 'Deploy!'")
    
    print("\n⚠️ IMPORTANT:")
    print("   The app must be deployed under YOUR Streamlit Cloud account")
    print("   to grant you full access and control.")
    
    print("\n📂 VERIFICATION:")
    print("   Confirm these files exist in your repository:")
    print("   ✅ resume_analyzer.py (main app file)")
    print("   ✅ requirements_streamlit.txt (dependencies)")
    print("   ✅ Repository is public (required for free tier)")
    
    print("\n" + "=" * 80)
    return True

def open_streamlit_cloud():
    """Open Streamlit Cloud in browser."""
    try:
        print("\n🚀 Opening Streamlit Cloud...")
        webbrowser.open("https://share.streamlit.io/")
        time.sleep(2)
        print("✅ Streamlit Cloud opened successfully!")
        print("   Please sign in with your GitHub account to deploy.")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("👉 Please manually visit: https://share.streamlit.io/")

def show_troubleshooting():
    """Show troubleshooting steps."""
    print("\n🔧 TROUBLESHOOTING ACCESS ISSUES:")
    print("1. If you see 'Access Denied':")
    print("   - The app was deployed under a different account")
    print("   - You need to deploy it under your own account")
    
    print("\n2. If repository not found:")
    print("   - Check that you've forked the repository to your account")
    print("   - Visit: https://github.com/Pratima-Dixit-R/resume-relevance-check")
    print("   - Click 'Fork' to create a copy under your account")
    
    print("\n3. If deployment fails:")
    print("   - Ensure repository is public")
    print("   - Verify file paths are correct")
    print("   - Check that all changes are pushed to GitHub")

def show_expected_result():
    """Show what to expect after successful deployment."""
    print("\n🎉 EXPECTED RESULT:")
    print("   After deploying under your account, you will get a URL like:")
    print("   https://[your-username]-resume-relevance-check.streamlit.app/")
    print("   Example: https://pratima-dixit-resume-relevance-check.streamlit.app/")
    
    print("\n✅ BENEFITS OF DEPLOYING UNDER YOUR ACCOUNT:")
    print("   - Full access and control")
    print("   - Ability to manage settings")
    print("   - Custom subdomain options")
    print("   - Analytics and monitoring")
    print("   - No access restrictions")

if __name__ == "__main__":
    show_deployment_guide()
    choice = input("\n❓ Would you like to open Streamlit Cloud now? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        open_streamlit_cloud()
    
    show_troubleshooting()
    show_expected_result()
    
    print(f"\n💡 REMEMBER: You must deploy under your own Streamlit Cloud account to have full access!")