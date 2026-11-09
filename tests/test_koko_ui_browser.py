from pathlib import Path

from playwright.sync_api import expect


ROOT = Path(__file__).resolve().parents[1]
THEME_SCRIPT = (ROOT / "app/static/js/koko-theme-engine.js").read_text(encoding="utf-8")
TABS_SCRIPT = (ROOT / "app/static/js/koko-workspace-tabs.js").read_text(encoding="utf-8")

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
