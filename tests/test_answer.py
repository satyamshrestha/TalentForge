import uuid
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app import app
from models.interview import Interview
from models.question import Question
from models.user import User
from services.deps import get_answer_service
from tests.conftest import TestingSessionLocal


client = TestClient(app)


class FakeAnswerService:

    def submit_answer(
        self,
        db,
        question_id,
        answer_text
    ):
        return SimpleNamespace(
            id=str(uuid.uuid4()),
            answer_text=answer_text,
            feedback="Good answer",
            score=9,
            suggested_improvement="Add more examples",
            question_id=question_id,
        )


def create_authenticated_user():
    email = f"answer-{uuid.uuid4()}@example.com"

    signup_response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": email,
            "password": "password123",
        },
    )

    assert signup_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def create_question():
    db = TestingSessionLocal()

    try:
        user = User(
            id=str(uuid.uuid4()),
            email=f"seed-{uuid.uuid4()}@example.com",
            password="$2b$12$dummy",
            role="student",
        )

        interview = Interview(
            id=str(uuid.uuid4()),
            role_target="Backend Developer",
            status="IN_PROGRESS",
            user=user,
        )

        question = Question(
            id=str(uuid.uuid4()),
            question_text="What is Python?",
            interview=interview,
        )

        db.add(user)
        db.add(interview)
        db.add(question)
        db.commit()
        db.refresh(question)

        return question.id

    finally:
        db.close()


def test_submit_answer():
    original_override = app.dependency_overrides.get(
        get_answer_service
    )

    app.dependency_overrides[get_answer_service] = (
        lambda: FakeAnswerService()
    )

    try:
        question_id = create_question()
        token = create_authenticated_user()

        response = client.post(
            "/api/v1/answers",
            json={
                "question_id": question_id,
                "answer_text": (
                    "Python is a programming language."
                ),
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["answer_text"] == (
            "Python is a programming language."
        )
        assert data["feedback"] == "Good answer"
        assert data["score"] == 9
        assert data["suggested_improvement"] == (
            "Add more examples"
        )
        assert data["question_id"] == question_id
        assert "id" in data

    finally:
        if original_override is not None:
            app.dependency_overrides[get_answer_service] = (
                original_override
            )
        else:
            app.dependency_overrides.pop(
                get_answer_service,
                None,
            )


def test_submit_answer_requires_authentication():
    original_override = app.dependency_overrides.get(
        get_answer_service
    )

    app.dependency_overrides[get_answer_service] = (
        lambda: FakeAnswerService()
    )

    try:
        question_id = create_question()

        response = client.post(
            "/api/v1/answers",
            json={
                "question_id": question_id,
                "answer_text": "Python is a programming language.",
            },
        )

        assert response.status_code == 401

    finally:
        if original_override is not None:
            app.dependency_overrides[get_answer_service] = (
                original_override
            )
        else:
            app.dependency_overrides.pop(
                get_answer_service,
                None,
            )


def test_submit_answer_validates_required_fields():
    original_override = app.dependency_overrides.get(
        get_answer_service
    )

    app.dependency_overrides[get_answer_service] = (
        lambda: FakeAnswerService()
    )

    try:
        token = create_authenticated_user()

        response = client.post(
            "/api/v1/answers",
            json={},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 422

    finally:
        if original_override is not None:
            app.dependency_overrides[get_answer_service] = (
                original_override
            )
        else:
            app.dependency_overrides.pop(
                get_answer_service,
                None,
            )