from io import BytesIO
from unittest.mock import patch
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


@patch("services.resume_service.redis_client.delete")
@patch("services.resume_service.process_resume.delay")
def test_upload_resume(
    mock_delay,
    mock_redis_delete
):
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "resume@example.com",
            "password": "password123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "resume@example.com",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/api/v1/resumes/upload",
        files={
            "file": (
                "resume.pdf",
                BytesIO(b"%PDF-1.4 fake pdf content"),
                "application/pdf"
            )
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "PENDING"
    assert data["user_id"] is not None

    mock_delay.assert_called_once()
    mock_redis_delete.assert_called_once()