import requests
import os

API_URL = "http://localhost:8000"

class APIClient:
    def __init__(self):
        self.base_url = API_URL
        self.token = None

    def set_token(self, token):
        self.token = token

    def login(self, email, password):
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data={"username": email, "password": password}
            )
            try:
                if response.status_code == 200:
                    return response.json()
                return {"error": response.json().get("detail", "Login failed")}
            except ValueError:
                return {"error": f"Server returned non-JSON response: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def signup(self, username, email, password):
        try:
            response = requests.post(
                f"{self.base_url}/auth/signup",
                json={"username": username, "email": email, "password": password}
            )
            try:
                if response.status_code == 200:
                    return response.json()
                return {"error": response.json().get("detail", "Signup failed")}
            except ValueError:
                return {"error": f"Server returned non-JSON response: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def analyze_symptoms(self, symptoms):
        if not self.token:
            return {"error": "Not authenticated"}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                json={"symptoms": symptoms},
                headers=headers
            )
            try:
                if response.status_code == 200:
                    return response.json()
                return {"error": response.json().get("detail", "Analysis failed")}
            except ValueError:
                return {"error": f"Server returned non-JSON response: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def get_history(self):
        if not self.token:
            return {"error": "Not authenticated"}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(
                f"{self.base_url}/history",
                headers=headers
            )
            try:
                if response.status_code == 200:
                    return response.json()
                return {"error": response.json().get("detail", "Failed to fetch history")}
            except ValueError:
                return {"error": f"Server returned non-JSON response: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
