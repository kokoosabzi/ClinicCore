from fastapi.testclient import TestClient

from app.core.security import hash_password, verify_password
from app.main import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_is_persian_rtl() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    assert 'lang="fa"' in response.text
    assert 'dir="rtl"' in response.text


def test_password_hash_roundtrip() -> None:
    password_hash = hash_password("secure-pass-123")
    assert password_hash != "secure-pass-123"
    assert verify_password("secure-pass-123", password_hash)
    assert not verify_password("wrong-pass", password_hash)
