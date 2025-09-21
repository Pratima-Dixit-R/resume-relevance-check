#!/usr/bin/env python3
"""
Deployment Verification Script
This script verifies that all files needed for Streamlit Cloud deployment are in the correct location.
"""

import os
from pathlib import Path

def verify_deployment_files():
    """Verify that all required files for Streamlit Cloud deployment exist."""
    print("=" * 70)
    print("🔍 VERIFYING STREAMLIT CLOUD DEPLOYMENT FILES")
    print("=" * 70)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Required files for Streamlit Cloud deployment
    required_files = [
        "resume_analyzer.py",
        "requirements_streamlit.txt"
    ]
    
    # Check if files exist
    all_files_exist = True
    for file_name in required_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name} - FOUND")
        else:
            print(f"❌ {file_name} - NOT FOUND")
            all_files_exist = False
    
    # Check repository URL
    print(f"\n🔗 Repository URL: https://github.com/Pratima-Dixit-R/resume-relevance-check")
    
    # Correct deployment settings
    print(f"\n📋 CORRECT DEPLOYMENT SETTINGS FOR STREAMLIT CLOUD:")
    print(f"   Repository: Pratima-Dixit-R/resume-relevance-check")
    print(f"   Branch: main")
    print(f"   Main file path: resume_analyzer.py")
    print(f"   Requirements file: requirements_streamlit.txt")
    
    if all_files_exist:
        print(f"\n🎉 ALL FILES VERIFIED SUCCESSFULLY!")
        print(f"   You can now deploy to Streamlit Cloud with confidence.")
    else:
        print(f"\n❌ SOME FILES ARE MISSING!")
        print(f"   Please check the repository and ensure all files are present.")
    
    print("=" * 70)

def show_troubleshooting():
    """Show troubleshooting steps if deployment fails."""
    print("\n🔧 TROUBLESHOOTING DEPLOYMENT ISSUES:")
    print("1. If 'main file path doesn't exist' error occurs:")
    print("   - Ensure you're using 'resume_analyzer.py' (not in src folder)")
    print("   - Verify the file exists in your repository root")
    print("   - Check that you've pushed all changes to GitHub")
    
    print("\n2. If requirements file issues occur:")
    print("   - Use 'requirements_streamlit.txt' as requirements file")
    print("   - Ensure it's in the repository root directory")
    
    print("\n3. If deployment still fails:")
    print("   - Check repository visibility (must be public for free tier)")
    print("   - Verify GitHub account is connected to Streamlit Cloud")
    print("   - Try refreshing the repository list in Streamlit Cloud")

if __name__ == "__main__":
    verify_deployment_files()
    show_troubleshooting()