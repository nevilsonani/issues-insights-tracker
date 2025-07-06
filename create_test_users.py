import requests

BASE_URL = "http://localhost:8000/api"

users = [
    {"email": "admin@example.com", "password": "admin123", "role": "ADMIN"},
    {"email": "maintainer@example.com", "password": "maintainer123", "role": "MAINTAINER"},
    {"email": "reporter@example.com", "password": "reporter123", "role": "REPORTER"},
]

def create_user(user):
    response = requests.post(f"{BASE_URL}/auth/register", json=user)
    if response.status_code == 200:
        print(f"✅ Created {user['role']} user: {user['email']}")
    elif response.status_code == 400 and "already exists" in response.text:
        print(f"ℹ️  {user['role']} user already exists: {user['email']}")
    else:
        print(f"❌ Failed to create {user['role']} user: {user['email']} - {response.text}")

def main():
    for user in users:
        create_user(user)

if __name__ == "__main__":
    main() 