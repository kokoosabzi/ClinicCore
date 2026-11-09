from pathlib import Path

from playwright.sync_api import expect


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "app/static/css/koko-ui.css"
THEME_PATH = ROOT / "app/static/js/koko-theme-engine.js"


def test_koko_dark_theme_covers_forms_tables_dialogs_and_legacy_surfaces(page):
    page.set_content("""<!doctype html>
    <html lang="fa" dir="rtl"><head><meta charset="utf-8"></head><body>
      <div class="metrics"><article id="metric">شاخص</article></div>
      <section id="form-section" class="koko-form-section">
        <input id="control" class="koko-control" type="text" value="نمونه">
      </section>
      <div id="table-wrap" class="koko-table-wrap">
        <table class="koko-table"><thead><tr><th id="table-head">عنوان</th></tr></thead>
        <tbody><tr><td>مقدار</td></tr></tbody></table>
      </div>
      <div class="koko-dialog-backdrop"><section id="dialog" class="koko-dialog">گفتگو</section></div>
      <button id="action" class="koko-action">عملیات</button>
      <div id="tab" class="koko-tab active"><button>صفحه فعال</button></div>
    </body></html>""")
    page.add_style_tag(path=str(CSS_PATH))
    page.add_script_tag(path=str(THEME_PATH))

    page.locator("#koko-theme-launcher").click()
    page.locator("#koko-theme-panel #kt-theme").select_option("dark")
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "dark")

    colors = page.evaluate("""() => {
      const read = id => {
        const el = document.getElementById(id);
        const style = getComputedStyle(el);
        return { background: style.backgroundColor, color: style.color, appearance: style.appearance };
      };
      return {
        body: getComputedStyle(document.body).backgroundColor,
        metric: read("metric"),
        form: read("form-section"),
        control: read("control"),
        table: read("table-wrap"),
        tableHead: read("table-head"),
        dialog: read("dialog"),
        action: read("action"),
        tab: read("tab")
      };
    }""")

    assert colors["body"] == "rgb(16, 25, 35)"
    for key in ("metric", "form", "control", "table", "dialog"):
        assert colors[key]["background"] == "rgb(25, 38, 51)", f"{key}: {colors[key]}"
    assert colors["control"]["appearance"] == "none"
    assert colors["tableHead"]["background"] == "rgb(34, 52, 66)"
    assert colors["action"]["color"] == "rgb(237, 244, 247)"
    assert colors["tab"]["background"] == "rgb(38, 59, 82)"

    page.locator("#koko-theme-panel #kt-theme").select_option("pastel")
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "pastel")
    restored = page.locator("#control").evaluate("(el) => ({background:getComputedStyle(el).backgroundColor,appearance:getComputedStyle(el).appearance})")
    assert restored["background"] == "rgb(255, 255, 255)"
    assert restored["appearance"] == "auto"
