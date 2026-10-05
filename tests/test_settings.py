import re

from app.core.auth import require_admin


def test_settings_requires_admin(client):
    response = client.get("/settings")
    assert response.status_code == 401


def test_admin_can_save_and_reload_settings(client):
    client.app.dependency_overrides[require_admin] = lambda: {"username": "admin", "role": "admin"}

    form = client.get("/settings")
    assert form.status_code == 200
    csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', form.text).group(1)

    response = client.post(
        "/settings",
        data={
            "csrf_token": csrf_token,
            "app_name": "ClinicCore Test",
            "app_title": "سامانه آزمایشی",
            "clinic_name": "کلینیک نمونه",
            "clinic_address": "تهران",
            "clinic_phone": "02112345678",
            "clinic_email": "test@example.com",
            "clinic_logo": "",
            "clinic_header_text": "سربرگ",
            "clinic_footer_text": "پاورقی",
            "app_theme": "light",
            "app_density": "compact",
            "datetime_calendar": "jalali",
            "datetime_timezone": "Asia/Tehran",
            "datetime_date_format": "DD/MM/YYYY",
            "datetime_time_format": "24",
            "datetime_show_seconds": "true",
            "reports_logo": "",
            "reports_header": "گزارش کلینیک",
            "reports_footer": "پایان گزارش",
            "reports_default_format": "pdf",
            "reports_include_timestamp": "false",
            "messaging_enabled": "true",
            "messaging_default_provider": "email",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303

    saved = client.get("/settings")
    assert saved.status_code == 200
    assert "ClinicCore Test" in saved.text
    assert "کلینیک نمونه" in saved.text
    assert 'value="Asia/Tehran"' in saved.text
    assert 'option value="DD/MM/YYYY" selected' in saved.text
    assert 'option value="true" selected' in saved.text
    assert 'option value="pdf" selected' in saved.text
    assert "گزارش کلینیک" in saved.text
    assert 'option value="email" selected' in saved.text


def test_invalid_timezone_is_rejected(client):
    client.app.dependency_overrides[require_admin] = lambda: {"username": "admin", "role": "admin"}

    form = client.get("/settings")
    csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', form.text).group(1)

    response = client.post(
        "/settings",
        data={
            "csrf_token": csrf_token,
            "app_name": "ClinicCore",
            "app_title": "کلینیک‌کور",
            "datetime_calendar": "jalali",
            "datetime_timezone": "Invalid/Timezone",
            "datetime_date_format": "YYYY/MM/DD",
            "datetime_time_format": "24",
            "datetime_show_seconds": "false",
        },
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert "معتبر نیست" in response.text


def test_invalid_messaging_provider_is_rejected(client):
    client.app.dependency_overrides[require_admin] = lambda: {"username": "admin", "role": "admin"}

    form = client.get("/settings")
    csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', form.text).group(1)

    response = client.post(
        "/settings",
        data={
            "csrf_token": csrf_token,
            "app_name": "ClinicCore",
            "app_title": "کلینیک‌کور",
            "messaging_enabled": "true",
            "messaging_default_provider": "invalid-provider",
        },
    )
    assert response.status_code == 200
    assert "معتبر نیست" in response.text
