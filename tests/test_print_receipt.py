from datetime import datetime

from app.core.auth import require_user
from app.models.appointment import Appointment, AppointmentStatus
from app.models.patient import Patient


def test_appointment_receipt_uses_light_theme_and_persian_fields(client, db_session_factory):
    client.app.dependency_overrides[require_user] = lambda: {"username": "tester", "role": "admin"}
    with db_session_factory() as db:
        patient = Patient(first_name="آزمایش", last_name="بیمار")
        db.add(patient)
        db.flush()
        appointment = Appointment(
            patient_id=patient.id,
            starts_at=datetime(2026, 10, 14, 13, 30),
            status=AppointmentStatus.booked,
        )
        db.add(appointment)
        db.commit()
        appointment_id = appointment.id

    response = client.get(f"/print/appointments/{appointment_id}")

    assert response.status_code == 200
    assert 'data-print-view="true"' in response.text
    assert "۱۴۰۵/۰۷/۲۲ ۱۳:۳۰" in response.text
    assert "ثبت شده" in response.text
    assert "2026-10-14 13:30:00" not in response.text
    assert ">booked<" not in response.text
