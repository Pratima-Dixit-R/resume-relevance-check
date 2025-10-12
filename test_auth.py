import requests
import json

# API base URL
API_BASE_URL = "http://localhost:8000/api/v1"

def test_authentication():
    print("Testing JWT Authentication System")
    print("=" * 40)
    
    # Test registration
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   Username: {user_data['username']}")
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test login
    print("\n2. Testing User Login...")
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   Token type: {token_data['token_type']}")
            print(f"   Token length: {len(access_token)} characters")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test protected endpoint with token
    print("\n3. Testing Protected Endpoint Access...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/auth/users/me", headers=headers)
        if response.status_code == 200:
            print("✅ Protected endpoint access successful!")
            user_info = response.json()
            print(f"   Authenticated user: {user_info['username']}")
        else:
            print(f"❌ Protected endpoint access failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Protected endpoint access error: {e}")
    
    # Test invalid token
    print("\n4. Testing Invalid Token Rejection...")
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/auth/users/me", headers=invalid_headers)
        if response.status_code == 401:
            print("✅ Invalid token correctly rejected!")
        else:
            print(f"⚠️  Unexpected response for invalid token: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid token test error: {e}")
    
    print("\n" + "=" * 40)
    print("Authentication System Test Complete!")

if __name__ == "__main__":
    test_authentication()