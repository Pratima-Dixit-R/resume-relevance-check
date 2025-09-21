#!/usr/bin/env python3
"""
Deployment Script for Streamlit Cloud
This script provides instructions and automation for deploying the Resume Analyzer to Streamlit Cloud.
"""

import webbrowser
import sys
import os

def deploy_instructions():
    """Display deployment instructions for Streamlit Cloud."""
    print("=" * 70)
    print("🚀 DEPLOY RESUME ANALYZER TO STREAMLIT CLOUD")
    print("=" * 70)
    
    print("\n📋 STEP-BY-STEP DEPLOYMENT INSTRUCTIONS:")
    print("1. Fork this repository to your GitHub account:")
    print("   - Go to: https://github.com/Pratima-Dixit-R/resume-relevance-check")
    print("   - Click the 'Fork' button in the top-right corner")
    
    print("\n2. Sign in to Streamlit Cloud:")
    print("   - Visit: https://share.streamlit.io/")
    print("   - Sign in with your GitHub account")
    
    print("\n3. Deploy the app:")
    print("   - Click 'New app'")
    print("   - Select your forked repository")
    print("   - Branch: main")
    print("   - Main file path: resume_analyzer.py")
    print("   - Click 'Deploy!'")
    
    print("\n4. Configure settings (if needed):")
    print("   - App URL: Choose a custom subdomain or use the generated one")
    print("   - Secrets: Not required for this app")
    
    print("\n✅ WHAT TO EXPECT:")
    print("- Deployment takes 1-5 minutes")
    print("- You'll get a public URL for your app")
    print("- The app will have file upload capabilities")
    print("- All processing happens in real-time (no data storage)")
    
    print("\n🔒 PRIVACY:")
    print("- No personal data is stored")
    print("- Files are processed in-memory only")
    print("- Sessions are not persisted between visits")
    
    print("\n" + "=" * 70)

def open_streamlit_cloud():
    """Open Streamlit Cloud in the default browser."""
    try:
        webbrowser.open("https://share.streamlit.io/")
        print("✅ Opening Streamlit Cloud in your browser...")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("Please manually visit: https://share.streamlit.io/")

def main():
    """Main function to guide deployment."""
    print("Resume Relevance Checker - Streamlit Cloud Deployment")
    
    deploy_instructions()
    
    choice = input("\n❓ Would you like to open Streamlit Cloud now? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        open_streamlit_cloud()
    
    print("\n💡 TIP: Make sure your GitHub repository is public for free deployment!")
    print("For private repositories, you'll need a Streamlit Cloud subscription.")

if __name__ == "__main__":
    main()