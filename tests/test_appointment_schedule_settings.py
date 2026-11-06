import re

from app.core.auth import require_admin
from app.services.settings_service import SettingsService


def test_admin_can_save_clinic_working_days_and_slot_duration(client):
    client.app.dependency_overrides[require_admin] = lambda: {"username": "admin", "role": "admin"}
    form = client.get("/settings")
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', form.text).group(1)

    response = client.post(
        "/settings",
        data={
            "csrf_token": csrf,
            "app_name": "ClinicCore",
            "app_title": "کلینیک‌کور",
            "appointments_workday_start": "08:00",
            "appointments_workday_end": "16:00",
            "appointments_slot_minutes": "15",
            "appointments_working_days": ["6", "7", "1", "2", "3", "4"],
        },
        follow_redirects=False,
    )
    assert response.status_code == 303

    saved = client.get("/settings")
    assert 'value="08:00"' in saved.text
    assert 'value="16:00"' in saved.text
    assert 'option value="15" selected' in saved.text
    assert 'value="5" checked' not in saved.text
    assert 'value="6" checked' in saved.text


def test_incompatible_workday_and_slot_duration_are_rejected(client):
    client.app.dependency_overrides[require_admin] = lambda: {"username": "admin", "role": "admin"}
    form = client.get("/settings")
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', form.text).group(1)

    response = client.post(
        "/settings",
        data={
            "csrf_token": csrf,
            "app_name": "ClinicCore",
            "app_title": "کلینیک‌کور",
            "appointments_workday_start": "09:00",
            "appointments_workday_end": "17:00",
            "appointments_slot_minutes": "45",
            "appointments_working_days": ["6", "7", "1"],
        },
    )
    assert response.status_code == 200
    assert "بخش‌پذیر" in response.text


def test_availability_endpoint_uses_saved_clinic_schedule(admin_client, db_session):
    SettingsService(db_session).set_many({
        "appointments.workday_start": "08:00",
        "appointments.workday_end": "16:00",
        "appointments.slot_minutes": "15",
        "appointments.working_days": "1,2,3,4,6,7",
    })

    response = admin_client.get(
        "/ui/appointments/availability",
        params={"date": "1408/10/25"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["slot_minutes"] == 15
    assert len(payload["slots"]) == 32
    assert payload["slots"][0]["time"] == "08:00"
    assert payload["slots"][-1]["time"] == "15:45"


def test_availability_endpoint_returns_no_slots_on_closed_weekday(admin_client):
    response = admin_client.get(
        "/ui/appointments/availability",
        params={"date": "1408/10/29"},
    )
    assert response.status_code == 200
    assert response.json()["slots"] == []
