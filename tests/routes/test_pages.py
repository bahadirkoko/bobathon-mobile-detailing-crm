"""HTTP smoke tests for public pages."""

from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_healthcheck_smoke() -> None:
    """Health endpoint returns a successful response."""
    response = client.get("/health")
    assert response.status_code == 200


def test_login_page_smoke() -> None:
    """Login page renders successfully."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "Demo Login" in response.text
