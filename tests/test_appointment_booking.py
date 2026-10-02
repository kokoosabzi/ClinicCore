from datetime import datetime

from app.core.auth import require_user
from app.models.appointment import Appointment
from app.models.patient import Patient


def _create_patient(db_session) -> Patient:
    patient = Patient(first_name="مینا", last_name="رضایی", phone="09120000001")
    db_session.add(patient)
    db_session.commit()
    return patient


def test_api_rejects_an_active_duplicate_appointment_slot(client, db_session) -> None:
    patient = _create_patient(db_session)
    client.app.dependency_overrides[require_user] = lambda: {"username": "test-admin", "role": "admin"}
    payload = {"patient_id": patient.id, "starts_at": "2026-10-02T09:30:00", "reason": "ویزیت"}

    first = client.post("/appointments/", json=payload)
    duplicate = client.post("/appointments/", json=payload)

    assert first.status_code == 201
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == "Appointment time is already booked"
    assert db_session.query(Appointment).filter_by(is_deleted=False).count() == 1


def test_api_allows_booking_a_slot_released_by_soft_delete(client, db_session) -> None:
    patient = _create_patient(db_session)
    released = Appointment(patient_id=patient.id, starts_at=datetime(2026, 10, 2, 10, 0), is_deleted=True)
    db_session.add(released)
    db_session.commit()
    client.app.dependency_overrides[require_user] = lambda: {"username": "test-admin", "role": "admin"}

    response = client.post(
        "/appointments/",
        json={"patient_id": patient.id, "starts_at": "2026-10-02T10:00:00"},
    )

    assert response.status_code == 201
