from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_dashboard():
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200