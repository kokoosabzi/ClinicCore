(() => {
  "use strict";
  const root = document.querySelector("[data-appointment-calendar]");
  if (!root) return;
  const calendar = root.querySelector("[data-calendar-grid]");
  const monthLabel = root.querySelector("[data-calendar-month]");
  const slots = root.querySelector("[data-time-slots]");
  const dateField = root.querySelector('input[name="starts_at_date"]');
  const timeField = root.querySelector('input[name="starts_at_time"]');
  const selectedDateLabel = root.querySelector("[data-selected-date]");
  const selectedTimeLabel = root.querySelector("[data-selected-time]");
  const slotMessage = root.querySelector("[data-slot-message]");
  const form = root.querySelector("form");
  const months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"];
  const weekdays = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"];
  const todayParts = (root.dataset.today || "1405/01/01").split("/").map(Number);
  let viewYear = todayParts[0], viewMonth = todayParts[1], selectedDate = "", requestSequence = 0;
  const pad = n => String(n).padStart(2, "0");
  const jalaliText = (y, m, d) => y + "/" + pad(m) + "/" + pad(d);
  const compareJalali = (a, b) => a.localeCompare(b);
  function jalaliToGregorian(year, month, day) {
    let jy = year, gy;
    if (jy > 979) { gy = 1600; jy -= 979; } else { gy = 621; }
    let days = 365 * jy + Math.floor(jy / 33) * 8 + Math.floor(((jy % 33) + 3) / 4) + 78 + day;
    days += month < 7 ? 31 * (month - 1) : 30 * (month - 7) + 186;
    gy += 400 * Math.floor(days / 146097); days %= 146097;
    if (days > 36524) {
      gy += 100 * Math.floor((days - 1) / 36524); days = (days - 1) % 36524;
      if (days >= 365) days += 1;
    }
    gy += 4 * Math.floor(days / 1461); days %= 1461;
    if (days > 365) { gy += Math.floor((days - 1) / 365); days = (days - 1) % 365; }
    let gd = days + 1;
    const leap = gy % 4 === 0 && (gy % 100 !== 0 || gy % 400 === 0);
    const lengths = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    let gm = 1;
    while (gd > lengths[gm - 1]) { gd -= lengths[gm - 1]; gm += 1; }
    return new Date(gy, gm - 1, gd, 12, 0, 0);
  }
  function gregorianToJalali(date) {
    let gy = date.getFullYear(), gm = date.getMonth() + 1, gd = date.getDate();
    const monthDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    let jy;
    if (gy > 1600) { jy = 979; gy -= 1600; } else { jy = 0; gy -= 621; }
    const gy2 = gm > 2 ? gy + 1 : gy;
    let days = 365 * gy + Math.floor((gy2 + 3) / 4) - Math.floor((gy2 + 99) / 100) + Math.floor((gy2 + 399) / 400) - 80 + gd + monthDays[gm - 1];
    jy += 33 * Math.floor(days / 12053); days %= 12053;
    jy += 4 * Math.floor(days / 1461); days %= 1461;
    if (days > 365) { jy += Math.floor((days - 1) / 365); days = (days - 1) % 365; }
    let jm, jd;
    if (days < 186) { jm = 1 + Math.floor(days / 31); jd = 1 + days % 31; }
    else { jm = 7 + Math.floor((days - 186) / 30); jd = 1 + (days - 186) % 30; }
    return [jy, jm, jd];
  }
  function monthLength(year, month) {
    if (month <= 6) return 31;
    if (month <= 11) return 30;
    const back = gregorianToJalali(jalaliToGregorian(year, 12, 30));
    return back[0] === year && back[1] === 12 && back[2] === 30 ? 30 : 29;
  }
  function formatPersianDigits(value) {
    return String(value).replace(/\d/g, digit => "۰۱۲۳۴۵۶۷۸۹"[Number(digit)]);
  }
  function renderCalendar() {
    monthLabel.textContent = months[viewMonth - 1] + " " + formatPersianDigits(viewYear);
    calendar.replaceChildren();
    weekdays.forEach(day => {
      const heading = document.createElement("span");
      heading.className = "calendar-weekday"; heading.textContent = day; calendar.append(heading);
    });
    const first = jalaliToGregorian(viewYear, viewMonth, 1);
    const offset = (first.getDay() + 1) % 7, length = monthLength(viewYear, viewMonth);
    for (let i = 0; i < offset; i += 1) {
      const blank = document.createElement("span"); blank.className = "calendar-blank"; calendar.append(blank);
    }
    for (let day = 1; day <= length; day += 1) {
      const value = jalaliText(viewYear, viewMonth, day);
      const button = document.createElement("button");
      button.type = "button"; button.className = "calendar-day";
      button.textContent = formatPersianDigits(day); button.dataset.date = value;
      button.disabled = compareJalali(value, jalaliText(...todayParts)) < 0;
      if (value === jalaliText(...todayParts)) button.classList.add("is-today");
      if (value === selectedDate) button.classList.add("is-selected");
      button.setAttribute("aria-label", day + " " + months[viewMonth - 1] + " " + viewYear);
      button.addEventListener("click", () => selectDate(value)); calendar.append(button);
    }
  }
  async function selectDate(value) {
    selectedDate = value; dateField.value = value; timeField.value = "";
    selectedDateLabel.textContent = formatPersianDigits(value.replaceAll("/", " / "));
    selectedTimeLabel.textContent = "هنوز ساعتی انتخاب نشده";
    renderCalendar(); slots.replaceChildren();
    slotMessage.textContent = "در حال دریافت ساعت‌های قابل رزرو…"; slotMessage.hidden = false;
    const sequence = ++requestSequence;
    try {
      const response = await fetch("/ui/appointments/availability?date=" + encodeURIComponent(value), { headers: { "Accept": "application/json" } });
      if (!response.ok) throw new Error("availability");
      const payload = await response.json();
      if (sequence !== requestSequence) return;
      slots.replaceChildren();
      payload.slots.forEach(slot => {
        const button = document.createElement("button");
        button.type = "button"; button.className = "time-slot is-" + slot.status;
        button.textContent = formatPersianDigits(slot.time); button.dataset.time = slot.time;
        button.disabled = slot.status !== "available";
        if (slot.status === "booked") {
          button.title = "این ساعت قبلاً رزرو شده است";
          button.setAttribute("aria-label", slot.time + "، رزرو شده");
        } else if (slot.status === "past") {
          button.title = "زمان گذشته است";
          button.setAttribute("aria-label", slot.time + "، زمان گذشته");
        } else {
          button.setAttribute("aria-label", slot.time + "، قابل رزرو");
          button.addEventListener("click", () => {
            timeField.value = slot.time;
            slots.querySelectorAll(".time-slot").forEach(item => item.classList.remove("is-selected"));
            button.classList.add("is-selected");
            selectedTimeLabel.textContent = formatPersianDigits(value) + "، ساعت " + formatPersianDigits(slot.time);
            slotMessage.hidden = true;
          });
        }
        slots.append(button);
      });
      slotMessage.textContent = payload.slots.some(slot => slot.status === "available")
        ? "یک ساعت آزاد را انتخاب کنید."
        : "برای این روز ساعت آزادی باقی نمانده است.";
      slotMessage.hidden = false;
    } catch {
      if (sequence !== requestSequence) return;
      slotMessage.textContent = "دریافت ساعت‌ها ناموفق بود. دوباره روز را انتخاب کنید.";
      slotMessage.hidden = false;
    }
  }
  root.querySelector("[data-month-prev]").addEventListener("click", () => {
    viewMonth -= 1; if (viewMonth < 1) { viewMonth = 12; viewYear -= 1; } renderCalendar();
  });
  root.querySelector("[data-month-next]").addEventListener("click", () => {
    viewMonth += 1; if (viewMonth > 12) { viewMonth = 1; viewYear += 1; } renderCalendar();
  });
  form.addEventListener("submit", event => {
    if (!dateField.value || !timeField.value) {
      event.preventDefault();
      slotMessage.textContent = "برای ثبت نوبت، ابتدا تاریخ و یک ساعت آزاد را انتخاب کنید.";
      slotMessage.hidden = false; slotMessage.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  });
  renderCalendar();
  selectDate(jalaliText(...todayParts));
})();
