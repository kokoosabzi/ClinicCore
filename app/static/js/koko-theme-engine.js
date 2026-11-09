(() => {
  'use strict';

  const KEY = 'koko-ui-preferences-v1';
  const defaults = {
    theme: 'pastel',
    accent: '#496cf0',
    density: 'comfortable',
    radius: 18,
    font: 'normal'
  };
  const palettes = {
    pastel: ['#eef1ff', '#ffffff', '#263653', '#7886a2', '#e3e8f4', '0 8px 26px rgba(53,76,130,.075)'],
    dark: ['#101923', '#192633', '#edf4f7', '#a5b5c1', '#354957', '0 8px 26px rgba(0,0,0,.22)'],
    minimal: ['#f5f6f7', '#ffffff', '#202a35', '#687482', '#e2e6ea', '0 2px 8px rgba(20,30,40,.045)'],
    glass: ['#edf3fa', 'rgba(255,255,255,.78)', '#263653', '#718096', 'rgba(255,255,255,.72)', '0 12px 34px rgba(55,85,125,.12)']
  };
  const root = document.documentElement;
  let stored = null;
  try {
    stored = JSON.parse(localStorage.getItem(KEY) || 'null');
  } catch (_) {}

  const followsDarkApp = root.dataset.style === 'modern-dark' || root.dataset.theme === 'dark';
  const initial = { ...defaults, theme: followsDarkApp ? 'dark' : 'pastel' };
  let prefs = stored && typeof stored === 'object' && !Array.isArray(stored)
    ? { ...initial, ...stored }
    : initial;

  const normalize = () => {
    if (!palettes[prefs.theme]) prefs.theme = defaults.theme;
    if (!/^#[0-9a-f]{6}$/i.test(prefs.accent || '')) prefs.accent = defaults.accent;
    if (!['compact', 'comfortable'].includes(prefs.density)) prefs.density = defaults.density;
    prefs.radius = Math.max(8, Math.min(28, Number(prefs.radius) || defaults.radius));
    if (!['small', 'normal', 'large'].includes(prefs.font)) prefs.font = defaults.font;
  };
  normalize();

  const css = [
    ':root{--koko-radius:var(--kt-radius,18px)}',
    'body{background:var(--kt-bg)!important;color:var(--kt-text)}',
    '.panel,.card,.metric,.hero,.metrics article,.metrics .card,.koko-shortcut,.quick-action{background:var(--kt-surface);border-color:var(--kt-border);border-radius:var(--kt-radius);box-shadow:var(--kt-shadow)}',
    'input,select,textarea{border-radius:max(8px,calc(var(--kt-radius)*.58));border-color:var(--kt-border);color:var(--kt-text)}',
    'button,.btn,.button,.primary{border-radius:max(8px,calc(var(--kt-radius)*.58))}',
    ':focus-visible{outline-color:color-mix(in srgb,var(--kt-accent) 38%,transparent)}',
    ':root[data-koko-density="compact"] .panel,:root[data-koko-density="compact"] .card,:root[data-koko-density="compact"] .metric,:root[data-koko-density="compact"] .metrics article{padding:12px}',
    ':root[data-koko-font="large"] body{font-size:1.08em}:root[data-koko-font="small"] body{font-size:.94em}',
    ':root[data-koko-theme="dark"]{color-scheme:dark}',
    ':root[data-koko-theme="dark"] .sidebar,:root[data-koko-theme="dark"] .topbar,:root[data-koko-theme="dark"] .layout>nav,:root[data-koko-theme="dark"] .app-shell>.sidebar,:root[data-koko-theme="dark"] .app-shell header,:root[data-koko-theme="dark"] .toolbar,:root[data-koko-theme="dark"] .table-wrap,:root[data-koko-theme="dark"] header.topbar #main-nav{background:var(--kt-surface)!important;color:var(--kt-text)!important;border-color:var(--kt-border)!important}',
    ':root[data-koko-theme="dark"] .sidebar nav button,:root[data-koko-theme="dark"] .sidebar button,:root[data-koko-theme="dark"] .layout>nav button,:root[data-koko-theme="dark"] header.topbar #main-nav a,:root[data-koko-theme="dark"] header.topbar #main-nav button{color:var(--kt-muted)!important}',
    ':root[data-koko-theme="dark"] .sidebar nav button.active,:root[data-koko-theme="dark"] .sidebar nav button:hover,:root[data-koko-theme="dark"] .layout>nav button.active,:root[data-koko-theme="dark"] .layout>nav button:hover,:root[data-koko-theme="dark"] header.topbar #main-nav a.active,:root[data-koko-theme="dark"] header.topbar #main-nav a:hover{background:#263b52!important;color:#edf4f7!important}',
    ':root[data-koko-theme="dark"] th{background:#223442!important;color:#a5b5c1!important}',
    ':root[data-koko-theme="dark"] td,:root[data-koko-theme="dark"] th{border-color:var(--kt-border)}',
    ':root[data-koko-theme="dark"] input,:root[data-koko-theme="dark"] select,:root[data-koko-theme="dark"] textarea{background:#192633;color:#edf4f7}',
    ':root[data-koko-theme="dark"] .koko-tab,:root[data-koko-theme="dark"] .koko-page-tabs a,:root[data-koko-theme="dark"] .koko-page-tabs button{background:#192633;color:#edf4f7;border-color:#354957}',
    ':root[data-koko-theme="dark"] .koko-tab.active,:root[data-koko-theme="dark"] .koko-page-tabs .active{background:#263b52;color:#edf4f7;border-color:#496cf0}',
    ':root[data-koko-theme="dark"] .koko-tab-close:hover{background:#51313d!important;color:#ffdce5!important}',
    ':root[data-koko-theme="dark"] .koko-card-blue,:root[data-koko-theme="dark"] .koko-card-mint,:root[data-koko-theme="dark"] .koko-card-lilac,:root[data-koko-theme="dark"] .koko-card-pink,:root[data-koko-theme="dark"] .koko-card-peach,:root[data-koko-theme="dark"] .koko-card-yellow{background:linear-gradient(135deg,#192633,#263b52)!important;color:var(--kt-text)!important}',
    ':root[data-koko-theme="dark"] .koko-welcome{background:linear-gradient(115deg,#192633,#243548 55%,#1c3b39)!important}',
    ':root[data-koko-theme="dark"] .koko-action{color:var(--kt-text)!important}',
    ':root[data-koko-theme="glass"] .panel,:root[data-koko-theme="glass"] .card,:root[data-koko-theme="glass"] .metrics article{backdrop-filter:blur(14px)}',
    '#koko-theme-launcher{position:fixed;z-index:9998;left:18px;bottom:18px;border:0;border-radius:999px;padding:12px 16px;background:var(--kt-accent);color:white;box-shadow:0 8px 24px #243b5340;font:inherit;cursor:pointer}',
    '#koko-theme-panel{position:fixed;z-index:9999;left:18px;bottom:72px;width:min(320px,calc(100vw - 36px));max-height:calc(100vh - 100px);overflow:auto;padding:16px;background:var(--kt-surface);color:var(--kt-text);border:1px solid var(--kt-border);border-radius:18px;box-shadow:0 14px 42px #172b4d30;display:none;direction:rtl;font:14px/1.7 Tahoma,sans-serif}',
    '#koko-theme-panel.open{display:grid;gap:11px}#koko-theme-panel label{display:grid;gap:4px;color:var(--kt-muted);font-size:12px}',
    '#koko-theme-panel select,#koko-theme-panel input{width:100%;min-height:36px;padding:6px 9px;background:var(--kt-bg);color:var(--kt-text);border:1px solid var(--kt-border);border-radius:9px}',
    '#koko-theme-panel .kt-row{display:grid;grid-template-columns:1fr 1fr;gap:9px}#koko-theme-panel .kt-actions{display:flex;justify-content:space-between;gap:8px}',
    '#koko-theme-panel button{padding:7px 12px;border:0;border-radius:9px;background:var(--kt-accent);color:#fff;cursor:pointer}#koko-theme-panel button.kt-reset{background:var(--kt-bg);color:var(--kt-text);border:1px solid var(--kt-border)}',
    '@media(max-width:480px){#koko-theme-panel{left:12px;bottom:68px;width:calc(100vw - 24px);max-height:calc(100vh - 88px)}}',
    '@media print{#koko-theme-launcher,#koko-theme-panel{display:none!important}}'
  ].join('\n');

  const style = document.createElement('style');
  style.id = 'koko-theme-engine-styles';
  style.textContent = css;
  document.head.appendChild(style);

  function apply(save = true) {
    normalize();
    const palette = palettes[prefs.theme];
    const [bg, surface, text, muted, border, shadow] = palette;
    const variables = {
      '--kt-bg': bg, '--kt-surface': surface, '--kt-text': text, '--kt-muted': muted,
      '--kt-border': border, '--kt-shadow': shadow,
      '--koko-bg': bg, '--koko-surface': surface, '--koko-text': text,
      '--koko-muted': muted, '--koko-border': border, '--koko-shadow': shadow
    };
    root.dataset.kokoTheme = prefs.theme;
    root.dataset.kokoDensity = prefs.density;
    root.dataset.kokoFont = prefs.font;
    Object.entries(variables).forEach(([name, value]) => root.style.setProperty(name, value));
    root.style.setProperty('--kt-accent', prefs.accent);
    root.style.setProperty('--koko-primary', prefs.accent);
    root.style.setProperty('--kt-radius', prefs.radius + 'px');
    root.style.setProperty('--koko-radius', prefs.radius + 'px');
    if (save) {
      try { localStorage.setItem(KEY, JSON.stringify(prefs)); } catch (_) {}
    }
  }

  apply(false);
  if (document.getElementById('koko-theme-launcher')) return;

  const launcher = document.createElement('button');
  launcher.id = 'koko-theme-launcher';
  launcher.type = 'button';
  launcher.textContent = '◐ پوسته و نمایش';
  launcher.setAttribute('aria-label', 'باز کردن تنظیمات پوسته و نمایش');
  launcher.setAttribute('aria-controls', 'koko-theme-panel');
  launcher.setAttribute('aria-expanded', 'false');

  const panel = document.createElement('section');
  panel.id = 'koko-theme-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'false');
  panel.setAttribute('aria-hidden', 'true');
  panel.setAttribute('aria-label', 'تنظیمات پوسته');
  panel.innerHTML = '<strong>شخصی‌سازی محیط</strong><label>قالب رنگی<select id="kt-theme"><option value="pastel">Pastel Light</option><option value="dark">Modern Dark</option><option value="minimal">Minimal</option><option value="glass">Glass</option></select></label><div class="kt-row"><label>رنگ اصلی<input id="kt-accent" type="color"></label><label>گردی گوشه‌ها<input id="kt-radius" type="range" min="8" max="28" step="2"></label></div><div class="kt-row"><label>تراکم نمایش<select id="kt-density"><option value="comfortable">راحت</option><option value="compact">فشرده</option></select></label><label>اندازه قلم<select id="kt-font"><option value="normal">عادی</option><option value="small">کوچک</option><option value="large">بزرگ</option></select></label></div><div class="kt-actions"><button type="button" id="kt-reset" class="kt-reset">بازنشانی</button><button type="button" id="kt-close">بستن</button></div>';

  document.body.appendChild(launcher);
  document.body.appendChild(panel);
  const $ = id => panel.querySelector('#' + id);

  function sync() {
    $('kt-theme').value = prefs.theme;
    $('kt-accent').value = prefs.accent;
    $('kt-radius').value = prefs.radius;
    $('kt-density').value = prefs.density;
    $('kt-font').value = prefs.font;
  }

  function setOpen(open, returnFocus = true) {
    panel.classList.toggle('open', open);
    panel.setAttribute('aria-hidden', String(!open));
    launcher.setAttribute('aria-expanded', String(open));
    if (open) $('kt-theme').focus();
    else if (returnFocus) launcher.focus();
  }

  function change() {
    prefs = {
      theme: $('kt-theme').value,
      accent: $('kt-accent').value,
      radius: Number($('kt-radius').value),
      density: $('kt-density').value,
      font: $('kt-font').value
    };
    apply();
  }

  ['kt-theme', 'kt-accent', 'kt-radius', 'kt-density', 'kt-font'].forEach(id => {
    $(id).addEventListener('input', change);
    $(id).addEventListener('change', change);
  });
  launcher.addEventListener('click', () => setOpen(panel.getAttribute('aria-hidden') === 'true'));
  $('kt-close').addEventListener('click', () => setOpen(false));
  $('kt-reset').addEventListener('click', () => {
    prefs = { ...defaults };
    sync();
    apply();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && panel.classList.contains('open')) setOpen(false);
  });
  document.addEventListener('pointerdown', event => {
    if (!panel.classList.contains('open')) return;
    if (panel.contains(event.target) || launcher.contains(event.target)) return;
    setOpen(false, false);
  });

  sync();
})();