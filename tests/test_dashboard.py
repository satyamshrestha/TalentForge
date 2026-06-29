from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_dashboard():
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "me@example.com",
            "password": "password123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "me@example.com",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200