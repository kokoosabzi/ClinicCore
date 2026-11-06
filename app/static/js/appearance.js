(() => {
  "use strict";
  const root = document.documentElement;
  const applyPreview = () => {
    const form = document.querySelector('form[action="/settings"]');
    if (!form) return;
    const style = form.querySelector('[name="app_style"]')?.value || "clinical-light";
    const theme = form.querySelector('[name="app_theme"]')?.value || "system";
    const density = form.querySelector('[name="app_density"]')?.value || "comfortable";
    const fontScale = form.querySelector('[name="app_font_scale"]')?.value || "normal";
    const color = form.querySelector('[name="app_primary_color"]')?.value || "#176b67";
    root.dataset.style = style;
    root.dataset.theme = style === "modern-dark" ? "dark" : theme;
    root.dataset.density = density;
    root.dataset.fontScale = fontScale;
    root.style.setProperty("--color-primary", color);
  };
  document.addEventListener("input", event => {
    if (event.target.closest('form[action="/settings"]')) applyPreview();
  });
  document.addEventListener("change", event => {
    if (event.target.closest('form[action="/settings"]')) applyPreview();
  });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", applyPreview);
  else applyPreview();
})();
