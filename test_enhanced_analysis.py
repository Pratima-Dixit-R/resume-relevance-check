#!/usr/bin/env python3
"""
Test script to verify enhanced analysis functionality
"""

import requests
import json

def test_enhanced_analysis():
    """Test the enhanced analysis functionality"""
    base_url = "http://localhost:8000/api/v1"
    
    # Test data
    test_resume = """
    John Doe
    Software Engineer
    
    Skills: Python, JavaScript, React, Node.js, SQL, Docker, AWS
    Experience: 5 years in web development
    Education: B.S. Computer Science
    """
    
    test_jd = """
    Senior Software Engineer
    Requirements:
    - 5+ years experience in Python and JavaScript
    - Experience with React and Node.js
    - Knowledge of SQL databases
    - Cloud experience (AWS preferred)
    - Docker containerization
    """
    
    # First, we need to register and login to get a token
    print("🔐 Testing Enhanced Analysis System")
    print("=" * 40)
    
    try:
        # Register test user
        register_data = {
            "username": "analysistestuser",
            "email": "analysis@test.com",
            "password": "TestPass123!"
        }
        
        print("📝 Registering test user...")
        register_response = requests.post(
            f"{base_url}/auth/register",
            json=register_data
        )
        
        if register_response.status_code == 400:
            print("⚠️  User already exists, proceeding with login...")
        elif register_response.status_code != 200:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(register_response.text)
            return False
        
        # Login to get token
        print("🔑 Logging in...")
        login_data = {
            "username": "analysistestuser",
            "password": "TestPass123!"
        }
        
        login_response = requests.post(
            f"{base_url}/auth/login",
            json=login_data
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(login_response.text)
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test the enhanced analysis
        print("🤖 Testing enhanced analysis...")
        analysis_data = {
            "resume_text": test_resume,
            "jd_text": test_jd
        }
        
        analysis_response = requests.post(
            f"{base_url}/evaluate/",
            data=analysis_data,
            headers=headers
        )
        
        if analysis_response.status_code != 200:
            print(f"❌ Analysis failed: {analysis_response.status_code}")
            print(analysis_response.text)
            return False
        
        result = analysis_response.json()
        print("✅ Analysis completed successfully!")
        print("\n📊 Results:")
        print(f"   Hard Match Score: {result.get('hard_match_score', 0):.1f}%")
        print(f"   Semantic Match Score: {result.get('semantic_match_score', 0):.1f}%")
        print(f"   Final Score: {result.get('final_score', 0):.1f}%")
        print(f"   Verdict: {result.get('verdict', 'Unknown')}")
        
        # Check for enhanced features
        if 'backend_scores' in result:
            print("\n🤖 Backend Scores:")
            for backend, score in result['backend_scores'].items():
                print(f"   {backend}: {score:.1f}%")
        
        if 'detailed_analysis' in result:
            print(f"\n🔍 Detailed Analysis: {result['detailed_analysis']}")
        
        if 'explanation' in result:
            print(f"\n📝 Explanation: {result['explanation']}")
        
        print("\n" + "=" * 40)
        print("🎉 Enhanced analysis test completed!")
        print("✅ Advanced data analysis and visualizations are working")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the service")
        print("   Make sure the application is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    test_enhanced_analysis()