import requests
import json

# API base URL
API_BASE_URL = "http://localhost:8000/api/v1"

def test_evaluation_endpoints():
    print("Testing Evaluation Endpoints with Authentication")
    print("=" * 50)
    
    # First, register and login to get a valid token
    print("\n1. Registering and logging in...")
    register_data = {
        "username": "evaluser",
        "email": "eval@example.com",
        "password": "evalpassword123"
    }
    
    try:
        # Register
        response = requests.post(f"{API_BASE_URL}/auth/register", json=register_data)
        if response.status_code != 200:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return
            
        # Login
        login_data = {
            "username": "evaluser",
            "password": "evalpassword123"
        }
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            print("✅ Login successful!")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # Test protected evaluation endpoint without token (should fail)
    print("\n2. Testing evaluation endpoint without authentication...")
    try:
        response = requests.get(f"{API_BASE_URL}/evaluations/")
        if response.status_code == 403:
            print("✅ Unauthenticated access correctly rejected!")
        else:
            print(f"⚠️  Unexpected response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    # Test protected evaluation endpoint with token (should succeed)
    print("\n3. Testing evaluation endpoint with authentication...")
    try:
        response = requests.get(f"{API_BASE_URL}/evaluations/", headers=headers)
        if response.status_code == 200:
            print("✅ Authenticated access successful!")
            evaluations = response.json()
            print(f"   Retrieved {len(evaluations)} evaluations")
        else:
            print(f"❌ Authenticated access failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("\n" + "=" * 50)
    print("Evaluation Endpoint Authentication Test Complete!")

if __name__ == "__main__":
    test_evaluation_endpoints()