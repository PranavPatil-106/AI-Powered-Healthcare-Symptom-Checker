import requests
import json

BASE_URL = "http://localhost:8000"

def test_flow():
    # 1. Signup
    print("1. Signup...")
    email = "test_user_api@example.com"
    password = "password123"
    
    # Try login first in case user exists
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        print("   Logged in existing user.")
    else:
        resp = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password})
        if resp.status_code != 200:
            print(f"   Signup failed: {resp.text}")
            return
        token = resp.json()["access_token"]
        print("   Signup successful.")

    # 2. Analyze
    print("2. Analyze Symptoms...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(f"{BASE_URL}/analyze", json={"symptoms": "I have a headache"}, headers=headers)
    
    print(f"STATUS: {resp.status_code}")
    with open("error.log", "w") as f:
        f.write(resp.text)
    print("Response written to error.log")
    import sys
    sys.stdout.flush()

if __name__ == "__main__":
    test_flow()
