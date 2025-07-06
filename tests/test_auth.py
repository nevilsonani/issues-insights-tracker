from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_login():
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "role": "REPORTER"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    login = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    assert login.status_code == 200
