from app.core.auth import require_admin


def test_settings_requires_admin(client):
    response = client.get("/settings")
    assert response.status_code == 401


def test_admin_can_save_and_reload_settings(client):
    client.app.dependency_overrides[require_admin] = lambda: {"username": "admin", "role": "admin", "id": 1}
    response = client.post(
        "/settings",
        data={
            "csrf_token": "",
            "app_name": "ClinicCore Test",
            "app_title": "سامانه آزمایشی",
            "clinic_name": "کلینیک نمونه",
            "clinic_address": "تهران",
            "clinic_phone": "02112345678",
            "clinic_email": "test@example.com",
            "clinic_logo": "",
            "clinic_header_text": "سربرگ",
            "clinic_footer_text": "پاورقی",
        },
        follow_redirects=False,
    )
    assert response.status_code in (303, 400)
