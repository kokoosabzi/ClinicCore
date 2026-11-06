(() => {
  "use strict";
  const roots = document.querySelectorAll("[data-jalali-picker]");
  if (!roots.length) return;
  const months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"];
  const weekdays = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"];
  const pad = value => String(value).padStart(2, "0");
  const toPersian = value => String(value).replace(/\d/g, digit => "۰۱۲۳۴۵۶۷۸۹"[Number(digit)]);
  const jalaliText = (year, month, day) => year + "/" + pad(month) + "/" + pad(day);
  function jalaliToGregorian(year, month, day) {
    let jy = year, gy;
    if (jy > 979) { gy = 1600; jy -= 979; } else { gy = 621; }
    let days = 365 * jy + Math.floor(jy / 33) * 8 + Math.floor(((jy % 33) + 3) / 4) + 78 + day;
    days += month < 7 ? 31 * (month - 1) : 30 * (month - 7) + 186;
    gy += 400 * Math.floor(days / 146097); days %= 146097;
    if (days > 36524) { gy += 100 * Math.floor((days - 1) / 36524); days = (days - 1) % 36524; if (days >= 365) days += 1; }
    gy += 4 * Math.floor(days / 1461); days %= 1461;
    if (days > 365) { gy += Math.floor((days - 1) / 365); days = (days - 1) % 365; }
    let gd = days + 1;
    const leap = gy % 4 === 0 && (gy % 100 !== 0 || gy % 400 === 0);
    const lengths = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    let gm = 1;
    while (gd > lengths[gm - 1]) { gd -= lengths[gm - 1]; gm += 1; }
    return new Date(gy, gm - 1, gd, 12, 0, 0);
  }
  function gregorianToJalali(value) {
    let gy = value.getFullYear(), gm = value.getMonth() + 1, gd = value.getDate();
    const monthDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    let jy;
    if (gy > 1600) { jy = 979; gy -= 1600; } else { jy = 0; gy -= 621; }
    const gy2 = gm > 2 ? gy + 1 : gy;
    let days = 365 * gy + Math.floor((gy2 + 3) / 4) - Math.floor((gy2 + 99) / 100) + Math.floor((gy2 + 399) / 400) - 80 + gd + monthDays[gm - 1];
    jy += 33 * Math.floor(days / 12053); days %= 12053;
    jy += 4 * Math.floor(days / 1461); days %= 1461;
    if (days > 365) { jy += Math.floor((days - 1) / 365); days = (days - 1) % 365; }
    if (days < 186) return [jy, 1 + Math.floor(days / 31), 1 + days % 31];
    return [jy, 7 + Math.floor((days - 186) / 30), 1 + (days - 186) % 30];
  }
  function monthLength(year, month) {
    if (month <= 6) return 31;
    if (month <= 11) return 30;
    const back = gregorianToJalali(jalaliToGregorian(year, 12, 30));
    return back[0] === year && back[1] === 12 && back[2] === 30 ? 30 : 29;
  }
  function init(root) {
    const input = root.querySelector("[data-jalali-value]");
    const trigger = root.querySelector("[data-jalali-trigger]");
    const panel = root.querySelector("[data-jalali-panel]");
    const label = root.querySelector("[data-jalali-label]");
    const monthLabel = root.querySelector("[data-jalali-month]");
    const grid = root.querySelector("[data-jalali-grid]");
    const today = (root.dataset.today || "1405/01/01").split("/").map(Number);
    const initial = (root.dataset.initial || root.dataset.today || "1405/01/01").split("/").map(Number);
    let viewYear = initial[0], viewMonth = initial[1], selected = jalaliText(...initial);
    function setValue(value) {
      const [year, month, day] = value.split("/").map(Number);
      const gregorian = jalaliToGregorian(year, month, day);
      input.value = gregorian.getFullYear() + "-" + pad(gregorian.getMonth() + 1) + "-" + pad(gregorian.getDate());
      label.textContent = toPersian(value);
      selected = value;
      trigger.setAttribute("aria-label", "تاریخ انتخاب‌شده " + label.textContent + "؛ برای تغییر انتخاب کنید");
    }
    function render() {
      monthLabel.textContent = months[viewMonth - 1] + " " + toPersian(viewYear);
      grid.replaceChildren();
      weekdays.forEach(day => { const el = document.createElement("span"); el.className = "calendar-weekday"; el.textContent = day; grid.append(el); });
      const first = jalaliToGregorian(viewYear, viewMonth, 1);
      const offset = (first.getDay() + 1) % 7;
      for (let i = 0; i < offset; i += 1) { const blank = document.createElement("span"); blank.className = "calendar-blank"; grid.append(blank); }
      for (let day = 1; day <= monthLength(viewYear, viewMonth); day += 1) {
        const value = jalaliText(viewYear, viewMonth, day);
        const button = document.createElement("button");
        button.type = "button"; button.className = "calendar-day"; button.textContent = toPersian(day);
        if (value === jalaliText(...today)) button.classList.add("is-today");
        if (value === selected) button.classList.add("is-selected");
        button.setAttribute("aria-label", day + " " + months[viewMonth - 1] + " " + viewYear);
        button.addEventListener("click", () => { setValue(value); panel.hidden = true; trigger.setAttribute("aria-expanded", "false"); });
        grid.append(button);
      }
    }
    root.querySelector("[data-jalali-prev]").addEventListener("click", () => { viewMonth -= 1; if (viewMonth < 1) { viewMonth = 12; viewYear -= 1; } render(); });
    root.querySelector("[data-jalali-next]").addEventListener("click", () => { viewMonth += 1; if (viewMonth > 12) { viewMonth = 1; viewYear += 1; } render(); });
    trigger.addEventListener("click", () => { panel.hidden = !panel.hidden; trigger.setAttribute("aria-expanded", String(!panel.hidden)); if (!panel.hidden) render(); });
    root.querySelector("[data-jalali-close]").addEventListener("click", () => { panel.hidden = true; trigger.setAttribute("aria-expanded", "false"); trigger.focus(); });
    setValue(jalaliText(...initial)); render();
  }
  roots.forEach(init);
})();