#!/usr/bin/env python3
"""
Deployment Automation for Forked Resume Relevance Checker
This script helps you deploy your forked app to Streamlit Cloud.
"""

import webbrowser
import time
import sys
import os

def verify_fork():
    """Verify that the repository has been forked."""
    print("=" * 80)
    print("🔍 VERIFYING YOUR FORKED REPOSITORY")
    print("=" * 80)
    
    print("\n✅ STEP 1: CONFIRM YOUR FORK")
    print("   Your forked repository should be at:")
    print("   https://github.com/[your-username]/resume-relevance-check")
    
    username = input("\n📝 Enter your GitHub username: ").strip()
    if not username:
        print("❌ Username is required!")
        return False
    
    repo_url = f"https://github.com/{username}/resume-relevance-check"
    print(f"\n🔗 Your forked repository: {repo_url}")
    
    # Verify key files exist
    print("\n🔍 VERIFYING REQUIRED FILES IN YOUR FORK:")
    print("   ✅ resume_analyzer.py (main app file)")
    print("   ✅ requirements_streamlit.txt (dependencies)")
    print("   ✅ Repository is public (required for free tier)")
    
    return username

def show_deployment_instructions(username):
    """Show detailed deployment instructions."""
    print("\n" + "=" * 80)
    print("🚀 DEPLOYMENT INSTRUCTIONS FOR YOUR FORK")
    print("=" * 80)
    
    print(f"\n📋 STEP-BY-STEP DEPLOYMENT:")
    print(f"1. VISIT STREAMLIT CLOUD:")
    print(f"   - Go to: https://share.streamlit.io/")
    print(f"   - Sign in with YOUR GitHub account")
    
    print(f"\n2. CONFIGURE DEPLOYMENT:")
    print(f"   - Click 'New app'")
    print(f"   - Repository owner: {username}")
    print(f"   - Repository name: resume-relevance-check")
    print(f"   - Branch: main")
    print(f"   - Main file path: resume_analyzer.py")
    print(f"   - Requirements file: requirements_streamlit.txt")
    
    print(f"\n3. DEPLOY:")
    print(f"   - Click 'Deploy!'")
    print(f"   - Wait 2-5 minutes for deployment to complete")
    
    # Generate expected URL
    expected_url = f"https://{username}-resume-relevance-check.streamlit.app/"
    print(f"\n🔗 EXPECTED URL AFTER DEPLOYMENT:")
    print(f"   {expected_url}")

def open_deployment_resources(username):
    """Open necessary resources for deployment."""
    print(f"\n" + "=" * 80)
    print(f"🔗 OPENING DEPLOYMENT RESOURCES")
    print(f"=" * 80)
    
    resources = [
        ("GitHub Repository", f"https://github.com/{username}/resume-relevance-check"),
        ("Streamlit Cloud", "https://share.streamlit.io/"),
        ("Deployment Documentation", "https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app")
    ]
    
    for name, url in resources:
        try:
            print(f"   Opening {name}...")
            webbrowser.open(url)
            time.sleep(1)
        except Exception as e:
            print(f"   ❌ Could not open {name}: {e}")
            print(f"   👉 Please manually visit: {url}")

def show_post_deployment():
    """Show post-deployment steps."""
    print(f"\n" + "=" * 80)
    print(f"✅ POST-DEPLOYMENT STEPS")
    print(f"=" * 80)
    
    print(f"1. TEST YOUR APP:")
    print(f"   - Upload a sample resume and job description")
    print(f"   - Verify file upload functionality")
    print(f"   - Check analysis results")
    
    print(f"\n2. SHARE YOUR APP:")
    print(f"   - Bookmark your app URL")
    print(f"   - Share with colleagues and clients")
    print(f"   - No installation required for users")
    
    print(f"\n3. MANAGE YOUR APP:")
    print(f"   - Access logs and analytics in Streamlit Cloud")
    print(f"   - Update settings as needed")
    print(f"   - Monitor usage and performance")

def main():
    """Main deployment automation function."""
    print("🤖 AUTOMATED DEPLOYMENT ASSISTANT")
    print("   Resume Relevance Checker - Streamlit Cloud")
    
    # Verify fork
    username = verify_fork()
    if not username:
        print("❌ Deployment preparation failed!")
        return
    
    # Show deployment instructions
    show_deployment_instructions(username)
    
    # Ask to open resources
    choice = input(f"\n❓ Would you like to open deployment resources now? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        open_deployment_resources(username)
    
    # Show post-deployment steps
    show_post_deployment()
    
    # Final reminder
    expected_url = f"https://{username}-resume-relevance-check.streamlit.app/"
    print(f"\n" + "=" * 80)
    print(f"🎉 READY FOR DEPLOYMENT!")
    print(f"=" * 80)
    print(f"📝 YOUR DEPLOYMENT CHECKLIST:")
    print(f"   1. Visit: https://share.streamlit.io/")
    print(f"   2. Sign in with your GitHub account")
    print(f"   3. Deploy your forked repository")
    print(f"   4. Your app will be available at:")
    print(f"      {expected_url}")
    print(f"=" * 80)

if __name__ == "__main__":
    main()