"""
Deployment Verification Script for Professional AI Resume Analyzer
This script verifies that all necessary files are in place for Streamlit Cloud deployment.
"""

import os
import sys
import subprocess
from pathlib import Path

def verify_files():
    """Verify that all required files exist for deployment"""
    print("🔍 Verifying deployment files...")
    
    # Required files for Streamlit Cloud deployment
    required_files = [
        "professional_resume_analyzer.py",
        "requirements_professional.txt",
        "README_PROFESSIONAL.md",
        "CUSTOM_DOMAIN_SETUP_GUIDE.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            print(f"❌ Missing file: {file}")
        else:
            print(f"✅ Found file: {file}")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("\n✅ All required files are present!")
    return True

def verify_python_dependencies():
    """Verify that all Python dependencies can be imported"""
    print("\n🔍 Verifying Python dependencies...")
    
    required_packages = [
        "streamlit",
        "plotly",
        "sklearn",
        "numpy",
        "pandas",
        "PyPDF2",
        "docx"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            missing_packages.append(package)
            print(f"❌ Failed to import {package}: {e}")
    
    if missing_packages:
        print(f"\n⚠️  Missing {len(missing_packages)} required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        return False
    
    print("\n✅ All Python dependencies are available!")
    return True

def verify_syntax():
    """Verify that Python files have correct syntax"""
    print("\n🔍 Verifying Python syntax...")
    
    python_files = [
        "professional_resume_analyzer.py"
    ]
    
    import ast
    
    syntax_errors = []
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            print(f"✅ {file} syntax is correct")
        except SyntaxError as e:
            syntax_errors.append((file, str(e)))
            print(f"❌ {file} has syntax error: {e}")
        except Exception as e:
            syntax_errors.append((file, str(e)))
            print(f"❌ {file} error: {e}")
    
    if syntax_errors:
        print(f"\n⚠️  Found {len(syntax_errors)} syntax errors:")
        for file, error in syntax_errors:
            print(f"  - {file}: {error}")
        return False
    
    print("\n✅ All Python files have correct syntax!")
    return True

def verify_requirements_file():
    """Verify that requirements file has correct format"""
    print("\n🔍 Verifying requirements file...")
    
    requirements_file = "requirements_professional.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found")
        return False
    
    try:
        with open(requirements_file, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            print(f"❌ {requirements_file} is empty")
            return False
        
        valid_lines = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Basic check for package format (package>=version or package==version)
                if '>=' in line or '==' in line or '.' in line:
                    valid_lines += 1
                    print(f"✅ Valid requirement: {line}")
                else:
                    # Allow packages without version specifiers
                    if line.replace('-', '').replace('_', '').isalnum() or '.' in line:
                        valid_lines += 1
                        print(f"✅ Valid requirement: {line}")
                    else:
                        print(f"⚠️  Questionable requirement: {line}")
        
        if valid_lines == 0:
            print(f"❌ No valid requirements found in {requirements_file}")
            return False
        
        print(f"\n✅ Requirements file verified with {valid_lines} valid entries!")
        return True
        
    except Exception as e:
        print(f"❌ Error reading {requirements_file}: {e}")
        return False

def verify_streamlit_config():
    """Verify Streamlit configuration"""
    print("\n🔍 Verifying Streamlit configuration...")
    
    # Check if the main app file has proper Streamlit setup
    main_file = "professional_resume_analyzer.py"
    
    if not os.path.exists(main_file):
        print(f"❌ {main_file} not found")
        return False
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required Streamlit elements
        required_elements = [
            "import streamlit as st",
            "st.set_page_config",
            "if __name__ == \"__main__\":",
            "main()"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element in content:
                print(f"✅ Found: {element}")
            else:
                missing_elements.append(element)
                print(f"❌ Missing: {element}")
        
        if missing_elements:
            print(f"\n⚠️  Missing {len(missing_elements)} required Streamlit elements")
            return False
        
        print("\n✅ Streamlit configuration verified!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking Streamlit configuration: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Professional AI Resume Analyzer - Deployment Verification")
    print("=" * 60)
    
    # Run all verification checks
    checks = [
        ("File Verification", verify_files),
        ("Python Dependencies", verify_python_dependencies),
        ("Syntax Verification", verify_syntax),
        ("Requirements File", verify_requirements_file),
        ("Streamlit Configuration", verify_streamlit_config)
    ]
    
    results = []
    for check_name, check_function in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        result = check_function()
        results.append((check_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"Total Checks: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All verification checks passed!")
        print("✅ Your application is ready for Streamlit Cloud deployment!")
        print("\n📋 Next steps:")
        print("1. Push all changes to GitHub")
        print("2. Deploy to Streamlit Cloud using professional_resume_analyzer.py")
        print("3. Configure custom domain using CUSTOM_DOMAIN_SETUP_GUIDE.md")
        return True
    else:
        print(f"\n⚠️  {failed} verification check(s) failed!")
        print("Please fix the issues before deploying to Streamlit Cloud.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)