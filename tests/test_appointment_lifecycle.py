from datetime import datetime

from app.models.appointment import Appointment, AppointmentStatus
from app.models.audit import AuditLog
from app.models.patient import Patient


def _patient(db_session):
    patient = Patient(first_name="سارا", last_name="احمدی", phone="09120000002")
    db_session.add(patient)
    db_session.commit()
    return patient


def _appointment(db_session, patient, starts_at=datetime(2031, 5, 10, 9, 0)):
    item = Appointment(patient_id=patient.id, starts_at=starts_at)
    db_session.add(item)
    db_session.commit()
    return item


def test_cancelled_appointment_releases_slot_and_is_audited(admin_client, db_session):
    patient = _patient(db_session)
    appointment = _appointment(db_session, patient)

    cancelled = admin_client.post(f"/appointments/{appointment.id}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"

    replacement = admin_client.post(
        "/appointments/",
        json={"patient_id": patient.id, "starts_at": "2031-05-10T09:00:00"},
    )
    assert replacement.status_code == 201
    assert db_session.query(Appointment).filter_by(starts_at=datetime(2031, 5, 10, 9, 0), status=AppointmentStatus.cancelled).count() == 1
    event = db_session.query(AuditLog).filter_by(action="appointment.status_changed", entity_id=str(appointment.id)).one()
    assert '"to": "cancelled"' in event.details


def test_appointment_state_machine_rejects_terminal_transition(admin_client, db_session):
    patient = _patient(db_session)
    appointment = _appointment(db_session, patient)
    completed = admin_client.patch(
        f"/appointments/{appointment.id}/status",
        json={"status": "completed"},
    )
    assert completed.status_code == 200
    invalid = admin_client.patch(
        f"/appointments/{appointment.id}/status",
        json={"status": "waiting"},
    )
    assert invalid.status_code == 422
    db_session.expire_all()
    assert db_session.get(Appointment, appointment.id).status == AppointmentStatus.completed


def test_appointment_can_move_from_booked_to_waiting_then_completed(admin_client, db_session):
    patient = _patient(db_session)
    appointment = _appointment(db_session, patient)
    waiting = admin_client.patch(
        f"/appointments/{appointment.id}/status",
        json={"status": "waiting"},
    )
    assert waiting.status_code == 200
    assert waiting.json()["status"] == "waiting"
    completed = admin_client.patch(
        f"/appointments/{appointment.id}/status",
        json={"status": "completed"},
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"


def test_reschedule_changes_time_and_blocks_duplicate_slot(admin_client, db_session):
    patient = _patient(db_session)
    first = _appointment(db_session, patient, datetime(2031, 5, 10, 9, 0))
    second = _appointment(db_session, patient, datetime(2031, 5, 10, 9, 30))

    conflict = admin_client.patch(
        f"/appointments/{first.id}/reschedule",
        json={"starts_at": "2031-05-10T09:30:00"},
    )
    assert conflict.status_code == 409
    assert db_session.get(Appointment, first.id).starts_at == datetime(2031, 5, 10, 9, 0)

    moved = admin_client.patch(
        f"/appointments/{first.id}/reschedule",
        json={"starts_at": "2031-05-10T10:00:00"},
    )
    assert moved.status_code == 200
    assert moved.json()["status"] == "rescheduled"
    assert moved.json()["starts_at"].startswith("2031-05-10T10:00:00")
    event = db_session.query(AuditLog).filter_by(action="appointment.rescheduled", entity_id=str(first.id)).one()
    assert '"to": "2031-05-10T10:00"' in event.details


def test_reschedule_page_uses_existing_jalali_booking_picker(admin_client, db_session):
    patient = _patient(db_session)
    appointment = _appointment(db_session, patient)

    response = admin_client.get(f"/appointments/{appointment.id}/reschedule")

    assert response.status_code == 200
    assert 'data-appointment-calendar' in response.text
    assert f"/ui/appointments/{appointment.id}/reschedule" in response.text
    assert "زمان فعلی" in response.text
