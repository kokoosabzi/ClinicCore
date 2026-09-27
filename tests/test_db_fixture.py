"""Smoke tests for the Phase A1 database test fixture (tests/conftest.py).

These tests exist to prove the fixture actually works end-to-end — not
to cover patient/appointment business logic in depth (that is later
phase work, per HELP/DEVELOPMENT/PROGRESS.md Phase A1's scope).
"""

from app.core.auth import require_user
from app.models.patient import Patient


def test_db_session_fixture_persists_and_queries_a_model(db_session):
    """The db_session fixture can insert and query a real model, proving
    the schema was created correctly from Base.metadata (see conftest.py)."""
    patient = Patient(first_name="Sara", last_name="Ahmadi", phone="09120000000")
    db_session.add(patient)
    db_session.commit()

    fetched = db_session.query(Patient).filter_by(first_name="Sara").one()
    assert fetched.id is not None
    assert fetched.last_name == "Ahmadi"
    assert fetched.is_deleted is False


def test_client_fixture_isolated_database_per_test(client):
    """Each test gets its own empty database — this test would fail if
    fixture teardown/isolation were broken and a previous test's data
    (e.g. from the test above) leaked through."""
    client.app.dependency_overrides[require_user] = lambda: {"username": "test-admin", "role": "admin"}

    response = client.get("/patients/")
    assert response.status_code == 200
    assert response.json() == []


def test_client_fixture_supports_full_crud_round_trip_through_http(client):
    """Exercises the full stack the fixture is meant to unblock for later
    phases: HTTP request -> router -> service -> repository -> the
    isolated test database -> back out through the response model."""
    client.app.dependency_overrides[require_user] = lambda: {"username": "test-admin", "role": "admin"}

    create_response = client.post(
        "/patients/",
        json={"first_name": "Reza", "last_name": "Karimi", "phone": "09121234567"},
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["first_name"] == "Reza"
    assert created["id"] is not None

    list_response = client.get("/patients/")
    assert list_response.status_code == 200
    names = [p["first_name"] for p in list_response.json()]
    assert names == ["Reza"]


def test_client_fixture_still_enforces_authentication(client):
    """Confirms overriding get_db for the test database does not
    accidentally weaken existing auth guards (require_user)."""
    response = client.get("/patients/")
    assert response.status_code == 401
