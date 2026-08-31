from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app import app
from services.deps import get_answer_service
import routers.websocket_router as websocket_router


client = TestClient(app)


@pytest.fixture
def mock_answer_service():
    service = MagicMock()

    app.dependency_overrides[get_answer_service] = (
        lambda: service
    )

    yield service

    app.dependency_overrides.pop(
        get_answer_service,
        None,
    )


def test_websocket_rejects_missing_authentication():
    with pytest.raises(Exception) as exc_info:
        with client.websocket_connect(
            "/api/v1/ws/interview/interview-123"
        ):
            pass

    assert exc_info.value.code == 1008


def test_websocket_rejects_unauthorized_interview(
    monkeypatch,
):
    async def mock_authenticate(websocket):
        return "user-123"

    monkeypatch.setattr(
        websocket_router,
        "authenticate_websocket",
        mock_authenticate,
    )

    monkeypatch.setattr(
        websocket_router,
        "can_access_interview",
        lambda db, user_id, interview_id: False,
    )

    with pytest.raises(Exception) as exc_info:
        with client.websocket_connect(
            "/api/v1/ws/interview/interview-123"
            "?token=test-token"
        ):
            pass

    assert exc_info.value.code == 1008


def test_websocket_rejects_invalid_message(
    monkeypatch,
):
    async def mock_authenticate(websocket):
        return "user-123"

    monkeypatch.setattr(
        websocket_router,
        "authenticate_websocket",
        mock_authenticate,
    )

    monkeypatch.setattr(
        websocket_router,
        "can_access_interview",
        lambda db, user_id, interview_id: True,
    )

    with client.websocket_connect(
        "/api/v1/ws/interview/interview-123"
        "?token=test-token"
    ) as websocket:

        started = websocket.receive_json()

        assert started["event"] == "interview.started"

        websocket.send_text(
            '{"invalid": "message"}'
        )

        response = websocket.receive_json()

        assert response["event"] == "error"
        assert response["data"]["message"] == (
            "Invalid answer message."
        )


def test_websocket_submits_answer_and_broadcasts_events(
    monkeypatch,
    mock_answer_service,
):
    async def mock_authenticate(websocket):
        return "user-123"

    monkeypatch.setattr(
        websocket_router,
        "authenticate_websocket",
        mock_authenticate,
    )

    monkeypatch.setattr(
        websocket_router,
        "can_access_interview",
        lambda db, user_id, interview_id: True,
    )

    monkeypatch.setattr(
        websocket_router,
        "can_access_question",
        lambda db, user_id, interview_id, question_id: True,
    )

    answer = SimpleNamespace(
        id="answer-123",
        score=8,
        feedback="Good answer.",
        suggested_improvement="Add more detail.",
        question=SimpleNamespace(
            interview=SimpleNamespace(
                status="IN_PROGRESS",
            )
        ),
    )

    mock_answer_service.submit_answer.return_value = answer

    with client.websocket_connect(
        "/api/v1/ws/interview/interview-123"
        "?token=test-token"
    ) as websocket:

        started = websocket.receive_json()

        assert started["event"] == "interview.started"

        websocket.send_json(
            {
                "question_id": "question-123",
                "answer": "My answer",
            }
        )

        submitted = websocket.receive_json()
        evaluated = websocket.receive_json()

        assert submitted["event"] == "answer.submitted"
        assert submitted["data"]["answer_id"] == (
            "answer-123"
        )

        assert evaluated["event"] == "answer.evaluated"
        assert evaluated["data"]["score"] == 8

        mock_answer_service.submit_answer.assert_called_once()


def test_websocket_disconnect_cleans_connection(
    monkeypatch,
):
    async def mock_authenticate(websocket):
        return "user-123"

    monkeypatch.setattr(
        websocket_router,
        "authenticate_websocket",
        mock_authenticate,
    )

    monkeypatch.setattr(
        websocket_router,
        "can_access_interview",
        lambda db, user_id, interview_id: True,
    )

    with client.websocket_connect(
        "/api/v1/ws/interview/interview-123"
        "?token=test-token"
    ) as websocket:

        websocket.receive_json()

        assert (
            websocket_router.manager.get_connection_count(
                "interview-123"
            )
            == 1
        )

    assert (
        websocket_router.manager.get_connection_count(
            "interview-123"
        )
        == 0
    )