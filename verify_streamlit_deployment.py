#!/usr/bin/env python3
"""
Verification script for Streamlit Cloud deployment of Professional AI Resume Analyzer
"""

import os
import sys
import ast
import subprocess
from pathlib import Path

def verify_files():
    """Verify that all required files exist"""
    print("🔍 Verifying required files...")
    
    required_files = [
        "professional_resume_analyzer.py",
        "requirements_professional.txt",
        "README_PROFESSIONAL.md",
        "STREAMLIT_CLOUD_DEPLOYMENT_GUIDE.md"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        return False
    
    return True

def verify_syntax():
    """Verify Python syntax"""
    print("\n🔍 Verifying Python syntax...")
    
    files_to_check = ["professional_resume_analyzer.py", "launch_professional_analyzer.py"]
    
    for file in files_to_check:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            print(f"✅ {file} - Syntax OK")
        except SyntaxError as e:
            print(f"❌ {file} - Syntax Error: {e}")
            return False
        except Exception as e:
            print(f"❌ {file} - Error: {e}")
            return False
    
    return True

def verify_dependencies():
    """Verify that dependencies can be imported"""
    print("\n🔍 Verifying dependencies...")
    
    required_imports = [
        "streamlit",
        "pandas",
        "plotly",
        "sklearn",
        "PyPDF2",
        "docx"
    ]
    
    missing_imports = []
    for module in required_imports:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_imports.append(module)
            print(f"❌ {module}")
    
    if missing_imports:
        print(f"\n⚠️  Missing imports: {missing_imports}")
        return False
    
    return True

def verify_requirements_file():
    """Verify requirements file format"""
    print("\n🔍 Verifying requirements file...")
    
    req_file = "requirements_professional.txt"
    if not os.path.exists(req_file):
        print(f"❌ {req_file} not found")
        return False
    
    try:
        with open(req_file, 'r') as f:
            content = f.read().strip()
        
        if not content:
            print(f"❌ {req_file} is empty")
            return False
        
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        
        if not lines:
            print(f"❌ {req_file} has no valid requirements")
            return False
        
        print(f"✅ {req_file} - {len(lines)} requirements found")
        for line in lines:
            print(f"   • {line}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading {req_file}: {e}")
        return False

def verify_readme():
    """Verify README contains essential information"""
    print("\n🔍 Verifying README...")
    
    readme_file = "README_PROFESSIONAL.md"
    if not os.path.exists(readme_file):
        print(f"❌ {readme_file} not found")
        return False
    
    try:
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            "Deployment Instructions",
            "File Structure",
            "Dependencies",
            "Features"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section in content:
                print(f"✅ {section}")
            else:
                missing_sections.append(section)
                print(f"❌ {section}")
        
        if missing_sections:
            print(f"\n⚠️  Missing sections: {missing_sections}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error reading {readme_file}: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Professional AI Resume Analyzer - Streamlit Cloud Deployment Verification")
    print("=" * 80)
    
    checks = [
        ("File Verification", verify_files),
        ("Syntax Verification", verify_syntax),
        ("Dependency Verification", verify_dependencies),
        ("Requirements File", verify_requirements_file),
        ("README Verification", verify_readme)
    ]
    
    results = []
    for check_name, check_function in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        result = check_function()
        results.append((check_name, result))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<35} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 80)
    print(f"Total Checks: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All verification checks passed!")
        print("✅ Your application is ready for Streamlit Cloud deployment!")
        print("\n📋 Next steps:")
        print("1. Push all changes to GitHub")
        print("2. Deploy to Streamlit Cloud using professional_resume_analyzer.py")
        print("3. Configure custom domain using the provided guide")
        return True
    else:
        print(f"\n⚠️  {failed} verification check(s) failed!")
        print("Please fix the issues before deploying to Streamlit Cloud.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)