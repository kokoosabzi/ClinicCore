from pathlib import Path

from playwright.sync_api import expect


ROOT = Path(__file__).resolve().parents[1]
THEME_SCRIPT = (ROOT / "app/static/js/koko-theme-engine.js").read_text(encoding="utf-8")
TABS_SCRIPT = (ROOT / "app/static/js/koko-workspace-tabs.js").read_text(encoding="utf-8")
BASE_TEMPLATE = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
NAV_SCRIPT = "function toggleClinicNav" + BASE_TEMPLATE.split("function toggleClinicNav", 1)[1].split("</script>", 1)[0]

HARNESS = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 16px; font-family: Tahoma, sans-serif; }}
  nav {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  nav a {{ padding: 10px 14px; border-radius: 10px; background: #eef1ff; }}
  main {{ min-height: 60vh; padding: 16px; }}
  #koko-workspace-tabs {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }}
  .koko-tab {{ display: flex; gap: 6px; padding: 6px; border: 1px solid #ddd; border-radius: 10px; }}
  .koko-tab.active {{ border-color: #496cf0; }}
</style>
</head>
<body>
<nav>
  <a href="/dashboard">داشبورد</a>
  <a href="/patients">بیماران</a>
  <a href="/appointments">نوبت‌ها</a>
  <a href="/settings">تنظیمات</a>
</nav>
<div id="koko-workspace-tabs" role="tablist" aria-label="صفحه‌های باز"></div>
<main><h1>آزمایش رابط کاربری</h1><section class="panel">محتوای آزمایشی</section></main>
<script>{THEME_SCRIPT}</script>
<script>{TABS_SCRIPT}</script>
</body>
</html>"""


def test_koko_theme_and_workspace_tabs_in_browser(page):
    page.route("http://clinic.test/**", lambda route: route.fulfill(
        status=200, content_type="text/html; charset=utf-8", body=HARNESS
    ))
    page.goto("http://clinic.test/dashboard")

    launcher = page.locator("#koko-theme-launcher")
    expect(launcher).to_be_visible()
    launcher.click()
    panel = page.locator("#koko-theme-panel")
    panel.locator("#kt-theme").select_option("dark")
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "dark")
    expect(panel).to_have_attribute("aria-hidden", "false")
    expect(launcher).to_have_attribute("aria-expanded", "true")
    assert page.locator("html").evaluate(
        "(el) => getComputedStyle(el).getPropertyValue('--koko-bg').trim() === '#101923'"
    )
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    expect(launcher).to_have_attribute("aria-expanded", "false")

    page.reload()
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "dark")
    page.locator("#koko-theme-launcher").click()
    page.locator("#kt-reset").click()
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "pastel")

    page.get_by_role("link", name="بیماران").click()
    expect(page).to_have_url("http://clinic.test/patients")
    expect(page.locator("#koko-workspace-tabs .koko-tab.active")).to_contain_text("بیماران")
    page.get_by_role("button", name="بستن بیماران").click()
    expect(page).to_have_url("http://clinic.test/dashboard")

    page.set_viewport_size({"width": 390, "height": 844})
    expect(page.locator("#koko-theme-launcher")).to_be_visible()
    assert page.locator("body").evaluate("(el) => el.scrollWidth <= window.innerWidth")


def test_clinic_mobile_navigation_drawer_and_keyboard_dismissal(page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.set_content("""<!doctype html>
    <html lang="fa" dir="rtl"><head><meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
      body{margin:0}header.topbar{height:70px;display:flex;align-items:center}
      .nav-toggle{display:inline-flex}
      #main-nav{display:none;position:fixed;top:70px;right:0;width:280px;height:calc(100vh - 70px);background:white}
      #main-nav.is-open{display:flex;flex-direction:column}
    </style></head><body><header class="topbar">
      <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" onclick="toggleClinicNav()">منو</button>
      <nav id="main-nav"><a href="#patients">بیماران</a><a href="#appointments">نوبت‌ها</a></nav>
    </header></body></html>""")
    page.add_script_tag(content=NAV_SCRIPT)

    toggle = page.locator(".nav-toggle")
    nav = page.locator("#main-nav")
    expect(toggle).to_be_visible()
    expect(nav).to_be_hidden()

    toggle.click()
    expect(nav).to_be_visible()
    expect(toggle).to_have_attribute("aria-expanded", "true")
    expect(page.locator("body")).to_have_class("koko-nav-open")

    page.keyboard.press("Escape")
    expect(nav).to_be_hidden()
    expect(toggle).to_have_attribute("aria-expanded", "false")
    expect(page.locator("body")).not_to_have_class("koko-nav-open")

    toggle.click()
    page.get_by_role("link", name="بیماران").click()
    expect(nav).to_be_hidden()
    expect(toggle).to_have_attribute("aria-expanded", "false")


def test_patient_pages_adopt_koko_ui_kit_without_changing_form_contracts():
    form = (ROOT / "app/templates/patients/form.html").read_text(encoding="utf-8")
    listing = (ROOT / "app/templates/patients/index.html").read_text(encoding="utf-8")
    detail = (ROOT / "app/templates/patients/detail.html").read_text(encoding="utf-8")

    assert 'class="form koko-form"' in form
    for field in ("first_name", "last_name", "national_code", "phone", "notes"):
        assert f'name="{field}"' in form
    assert 'name="csrf_token"' in form
    assert 'action="{{ action }}"' in form
    assert "koko-form-grid" in form and "koko-form-actions" in form

    assert 'class="koko-table-wrap"' in listing
    assert 'class="koko-table"' in listing
    assert 'name="q"' in listing
    assert "/patients/{{ patient.id }}" in listing

    assert detail.count('class="koko-table-wrap"') == 2
    assert detail.count('class="koko-table"') == 2
    assert 'action="/ui/patients/{{ patient.id }}/delete"' in detail
    assert 'name="csrf_token"' in detail


def test_appointment_pages_adopt_koko_ui_kit_and_keep_calendar_hooks():
    form = (ROOT / "app/templates/appointments/form.html").read_text(encoding="utf-8")
    listing = (ROOT / "app/templates/appointments/index.html").read_text(encoding="utf-8")

    assert 'class="form appointment-form koko-form"' in form
    for hook in ("data-appointment-calendar", "data-calendar-grid", "data-time-slots",
                 "data-selected-date", "data-selected-time", "data-month-prev",
                 "data-month-next"):
        assert hook in form
    for field in ("patient_id", "reason", "notes", "starts_at_date", "starts_at_time"):
        assert f'name="{field}"' in form
    assert 'name="csrf_token"' in form
    assert "koko-form-section" in form and "koko-form-actions" in form

    assert 'class="table-wrap koko-table-wrap"' in listing
    assert 'class="koko-table"' in listing
    assert 'class="appointment-actions koko-table-actions"' in listing
    for endpoint in ("/reschedule", "/status", "/cancel", "/print/appointments/"):
        assert endpoint in listing
    assert 'name="csrf_token"' in listing
    assert "appointments.update" in listing and "appointments.cancel" in listing


def test_message_pages_adopt_koko_ui_kit_without_changing_post_contracts():
    listing = (ROOT / "app/templates/messages/index.html").read_text(encoding="utf-8")
    form = (ROOT / "app/templates/messages/form.html").read_text(encoding="utf-8")

    assert 'class="koko-table-wrap"' in listing
    assert 'class="koko-table"' in listing
    for column in ("recipient", "provider", "status", "body"):
        assert f"item.{column}" in listing

    assert 'method="post" action="/ui/messages"' in form
    assert 'class="form koko-form"' in form
    assert 'name="csrf_token"' in form
    for field in ("recipient", "provider", "body"):
        assert f'name="{field}"' in form
    assert 'class="koko-form-section"' in form
    assert 'class="koko-form-actions is-sticky"' in form


def test_financial_pages_adopt_koko_ui_kit_and_keep_form_and_calendar_contracts():
    listing = (ROOT / "app/templates/financial/index.html").read_text(encoding="utf-8")
    payment = (ROOT / "app/templates/financial/payment_form.html").read_text(encoding="utf-8")
    expense = (ROOT / "app/templates/financial/expense_form.html").read_text(encoding="utf-8")

    assert listing.count('class="koko-table-wrap"') == 2
    assert listing.count('class="koko-table"') == 2
    assert "/print/payments/{{ item.id }}" in listing
    assert "/financial/expenses/new" in listing

    assert 'method="post" action="/ui/financial/payments"' in payment
    assert 'method="post" action="/ui/financial/expenses"' in expense
    for template, fields, date_name in (
        (payment, ("patient_id", "amount", "paid_at", "description"), "paid_at"),
        (expense, ("title", "amount", "spent_at", "category", "description"), "spent_at"),
    ):
        assert 'class="form koko-form"' in template
        assert 'name="csrf_token"' in template
        assert 'class="koko-form-section"' in template
        assert 'class="koko-form-actions is-sticky"' in template
        for field in fields:
            assert f'name="{field}"' in template
        assert f'name="{date_name}"' in template
        assert "data-jalali-picker" in template
        assert "data-jalali-trigger" in template
        assert "data-jalali-value" in template


def test_user_management_and_roles_adopt_koko_ui_without_changing_permissions():
    manage = (ROOT / "app/templates/users/manage.html").read_text(encoding="utf-8")
    roles = (ROOT / "app/templates/users/roles.html").read_text(encoding="utf-8")
    for endpoint in ("/users/ui/create", "/users/ui/{{ item.id }}/update",
                     "/users/ui/{{ item.id }}/reset-password",
                     "/users/ui/{{ item.id }}/deactivate",
                     "/users/ui/{{ item.id }}/reactivate"):
        assert endpoint in manage
    assert 'name="csrf_token"' in manage
    for field in ("full_name", "username", "password", "role"):
        assert f'name="{field}"' in manage
    for permission in ("can_create", "can_update", "can_assign_role",
                       "can_reset_password", "can_deactivate", "actor_id"):
        assert permission in manage
    assert 'koko-form' in manage
    assert 'class="koko-table-wrap"' in manage
    assert 'class="koko-table"' in manage
    for state in ("is-success", "is-warning", "is-danger"):
        assert f"koko-badge {state}" in manage
    assert "temporary_password" in manage

    assert 'action="/users/roles/{{ entry.role.key }}"' in roles
    assert 'name="permissions"' in roles
    assert 'name="csrf_token"' in roles
    assert "entry.granted" in roles
    assert "entry.role.key == 'admin'" in roles
    assert "koko-form-section" in roles and "koko-form-actions" in roles


def test_settings_form_keeps_existing_configuration_fields_and_file_upload():
    settings = (ROOT / "app/templates/settings.html").read_text(encoding="utf-8")
    assert 'method="post" action="/settings"' in settings
    assert 'enctype="multipart/form-data"' in settings
    assert 'name="csrf_token"' in settings
    assert 'class="form koko-form"' in settings
    assert 'name="clinic_logo_file"' in settings
    for field in ("app_name", "app_theme", "app_style", "datetime_calendar",
                  "datetime_timezone", "appointments_workday_start",
                  "appointments_workday_end", "appointments_working_days",
                  "reports_default_format", "messaging_enabled",
                  "contacts_enabled", "print_paper_size", "system_audit_enabled",
                  "clinic_name", "clinic_email", "clinic_logo"):
        assert f'name="{field}"' in settings
    assert 'class="koko-form-actions is-sticky"' in settings
