from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app
from models.resume import Resume
from models.interview import Interview
from models.question import Question
from models.user import User
from tests.conftest import TestingSessionLocal


client = TestClient(app)


@patch("services.resume_service.cache_delete")
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


def test_retake_interview():
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "retake@example.com",
            "password": "password123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "retake@example.com",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == "retake@example.com")
            .first()
        )

        assert user is not None

        user_id = user.id

        original_interview = Interview(
            id="original-interview-id",
            role_target="Backend Engineer",
            status="COMPLETED",
            user_id=user_id
        )

        db.add(original_interview)
        db.commit()
        db.refresh(original_interview)

        question = Question(
            id="original-question-id",
            question_text="Explain dependency injection in FastAPI.",
            interview_id=original_interview.id
        )

        db.add(question)
        db.commit()

        interview_id = original_interview.id

    finally:
        db.close()

    response = client.post(
        f"/api/v1/interviews/{interview_id}/retake",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] != interview_id
    assert data["role_target"] == "Backend Engineer"
    assert data["status"] == "CREATED"

    assert len(data["questions"]) == 1
    assert (
        data["questions"][0]["question_text"]
        == "Explain dependency injection in FastAPI."
    )

    db = TestingSessionLocal()

    try:
        interviews = (
            db.query(Interview)
            .filter(Interview.user_id == user_id)
            .all()
        )

        assert len(interviews) == 2

    finally:
        db.close()