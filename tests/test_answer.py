import uuid

from fastapi.testclient import TestClient

from app import app
from models.interview import Interview
from models.question import Question
from models.user import User
from tests.conftest import TestingSessionLocal

client = TestClient(app)


def test_submit_answer():
    db = TestingSessionLocal()

    user = User(
        id=str(uuid.uuid4()),
        email="seed@example.com",
        password="$2b$12$dummy",
        role="student"
    )

    interview = Interview(
        id=str(uuid.uuid4()),
        role_target="Backend Developer",
        status="IN_PROGRESS",
        user=user
    )

    question = Question(
        id=str(uuid.uuid4()),
        question_text="What is Python?",
        interview=interview
    )

    db.add(user)
    db.commit()

    question_id = question.id
    db.close()

    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "answerlogin@example.com",
            "password": "password123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "answerlogin@example.com",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/api/v1/answers",
        json={
            "question_id": question_id,
            "answer_text": "Python is a programming language."
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer_text"] == "Python is a programming language."
    assert data["feedback"] is not None
    assert data["score"] is not None