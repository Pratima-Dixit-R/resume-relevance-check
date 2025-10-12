#!/usr/bin/env python3
"""
Complete Deployment Guide for Resume Relevance Checker
This script provides detailed instructions to deploy your forked app to Streamlit Cloud.
"""

import webbrowser
import time
import os
import subprocess

def show_deployment_steps():
    """Show detailed deployment steps."""
    print("=" * 80)
    print("🚀 COMPLETE DEPLOYMENT GUIDE FOR YOUR FORKED REPOSITORY")
    print("=" * 80)
    
    print("\n✅ STEP 1: VERIFY YOUR FORK")
    print("   Your forked repository should be at:")
    print("   https://github.com/[your-username]/resume-relevance-check")
    
    print("\n✅ STEP 2: ACCESS STREAMLIT CLOUD")
    print("   1. Visit: https://share.streamlit.io/")
    print("   2. Sign in with YOUR GitHub account (important!)")
    print("   3. If prompted, authorize Streamlit Cloud to access your GitHub")
    
    print("\n✅ STEP 3: DEPLOY YOUR APP")
    print("   1. Click 'New app'")
    print("   2. Select your repository:")
    print("      - Owner: [your-username]")
    print("      - Repository: resume-relevance-check")
    print("      - Branch: main")
    print("   3. Set these deployment options:")
    print("      - Main file path: resume_analyzer.py")
    print("      - Requirements file: requirements_streamlit.txt")
    print("   4. Click 'Deploy!'")
    
    print("\n✅ STEP 4: WAIT FOR DEPLOYMENT")
    print("   1. Deployment takes 2-5 minutes")
    print("   2. Watch the build logs for progress")
    print("   3. You'll get your unique URL when complete")
    
    print("\n" + "=" * 80)
    return True

def show_troubleshooting():
    """Show troubleshooting steps."""
    print("\n🔧 TROUBLESHOOTING COMMON ISSUES:")
    print("1. If 'Repository not found':")
    print("   - Ensure you forked to your account")
    print("   - Check that you're signed in with the correct GitHub account")
    
    print("\n2. If 'File not found' errors:")
    print("   - Verify resume_analyzer.py exists in repository root")
    print("   - Check that requirements_streamlit.txt exists")
    
    print("\n3. If deployment fails:")
    print("   - Ensure repository is public (required for free tier)")
    print("   - Check that all files are pushed to GitHub")

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

def show_expected_result():
    """Show what to expect after successful deployment."""
    print("\n🎉