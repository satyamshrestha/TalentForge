from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app
from models.resume import Resume
from tests.conftest import TestingSessionLocal

client = TestClient(app)


@patch("services.resume_service.redis_client.delete")
@patch("services.resume_service.process_resume.delay")
def test_create_interview_from_processing_resume(
    mock_delay,
    mock_redis_delete
):
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "interview_processing@example.com",
            "password": "password123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "interview_processing@example.com",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    upload_response = client.post(
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

    assert upload_response.status_code == 200

    resume_id = upload_response.json()["id"]

    db = TestingSessionLocal()

    try:
        resume = (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

        assert resume is not None

        resume.status = "PROCESSING"
        db.commit()

    finally:
        db.close()

    response = client.post(
        f"/api/v1/interviews/from-resume/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Resume is still being processed. Please try again later."
    )

    mock_delay.assert_called_once()
    mock_redis_delete.assert_called_once()