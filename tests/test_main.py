# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "환영합니다" in response.json().get("message", "")
