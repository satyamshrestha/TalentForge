import uuid
from fastapi.testclient import TestClient
from app import app

from models.user import User
from tests.conftest import TestingSessionLocal

client = TestClient(app)

def test_signup():
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data


def test_duplicate_email_signup():
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 409


def test_login():
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password():
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "wrong@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "incorrect"
        }
    )

    assert response.status_code == 401


def test_me_endpoint():
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
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["Email"] == "me@example.com"
    assert response.json()["Role"] == "student"


def test_me_without_token():
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401

def test_refresh_token():
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "refresh@example.com",
            "password": "password123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "refresh@example.com",
            "password": "password123"
        }
    )

    refresh_token = login.json()["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_google_user_cannot_login_with_password():
    db = TestingSessionLocal()

    google_user = User(
        id=str(uuid.uuid4()),
        email="google@example.com",
        password=None,
        provider="google",
        google_id="google123",
        role="student"
    )

    db.add(google_user)
    db.commit()
    db.close()

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "google@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please sign in with Google."