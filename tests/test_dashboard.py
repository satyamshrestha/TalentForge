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
    data = response.json()

    assert "total_resumes" in data
    assert "total_interviews" in data
    assert "completed_interviews" in data
    assert "average_interview_score" in data
    assert "recent_interviews" in data