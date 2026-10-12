from datetime import datetime

from app.core.auth import require_user
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.services.datetime_service import format_jalali


def test_appointment_availability_marks_occupied_slots(client, db_session) -> None:
    patient = Patient(first_name="مینا", last_name="رضایی", phone="09120000001")
    db_session.add(patient)
    db_session.flush()
    db_session.add(
        Appointment(
            patient_id=patient.id,
            starts_at=datetime(2030, 1, 15, 9, 30),
        )
    )
    db_session.commit()
    client.app.dependency_overrides[require_user] = lambda: {"username": "test-admin", "role": "admin"}

    selected_date = format_jalali(datetime(2030, 1, 15))
    response = client.get("/ui/appointments/availability", params={"date": selected_date})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["slots"]) == 16
    slots = {slot["time"]: slot["status"] for slot in payload["slots"]}
    assert slots["09:00"] == "available"
    assert slots["09:30"] == "booked"


def test_appointment_availability_rejects_invalid_jalali_date(client) -> None:
    client.app.dependency_overrides[require_user] = lambda: {"username": "test-admin", "role": "admin"}

    response = client.get("/ui/appointments/availability", params={"date": "1405/13/01"})

    assert response.status_code == 400
