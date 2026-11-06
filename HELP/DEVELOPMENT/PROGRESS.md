# ClinicCore — Development Progress

> این فایل وضعیت واقعی مخزن و شواهد تست را ثبت می‌کند. هیچ تست اجرا‌نشده‌ای Pass محسوب نمی‌شود.

Last updated: 2026-11-06
Last updated by: ChatGPT — consolidation of Windows/SQLite, RBAC and dynamic UI themes
Repository: `main`

## 1. وضعیت شاخه‌ها و ادغام‌ها

- PR #14 — Windows & SQLite runtime: ادغام‌شده در `main`.
- PR #15 — User Administration & RBAC: ادغام‌شده در `main`.
- PR #17 — Dynamic UI Themes: ادغام‌شده در `main`.
- PR #16 — نسخه قبلی تغییرات تم؛ به‌عنوان superseded بسته شد و تغییرات آن از مسیر PR #17 وارد `main` شدند.
- PRهای قبلی #1 تا #13 نیز طبق سوابق GitHub ادغام شده‌اند.
- شاخه `main` مبنای فعلی کد است. شاخه `development` در PR #17 ادغام شده و برای ادامه توسعه لازم نیست.
- چند شاخه قدیمی هنوز به‌صورت ref در GitHub وجود دارند؛ حذف آن‌ها به‌دلیل نبود عملیات حذف شاخه در اتصال فعلی انجام نشده است. پیش از حذف باید اطمینان حاصل شود که commit منحصربه‌فرد و کار ادغام‌نشده‌ای ندارند.
- فایل قدیمی `ClinicCore-Full-Structure.md` در شاخه `cliniccore-refactor` یک طرح اولیه و منسوخ است؛ معماری PostgreSQL/Docker و `create_all` آن با تصمیم فعلی SQLite-only و Alembic-only مغایرت دارد و وارد محصول نشده است.

## 2. وضعیت تحویل

| بخش | وضعیت پیاده‌سازی | شواهد / محدودیت |
|---|---|---|
| Windows + SQLite runtime | پیاده‌سازی ادغام‌شده | CI ویندوز موفق؛ پذیرش دستی روی رایانه کاربر باقی است |
| Login / User Administration / RBAC | پیاده‌سازی ادغام‌شده | CI ویندوز و تست‌های RBAC موفق؛ پذیرش دستی UI باقی است |
| Dynamic UI Themes | پیاده‌سازی ادغام‌شده | CI ویندوز روی شاخه ادغام‌شده موفق؛ بازبینی بصری دستی باقی است |
| Jalali calendar/date handling | تقویم اختصاصی رزرو نوبت و تبدیل تاریخ پیاده‌سازی شده | اعتبارسنجی strict ورودی تاریخ/زمان و آزمون مرز سال/کبیسه اضافه شده؛ یکپارچگی سایر فرم‌ها هنوز باقی است |
| Manual Windows installation | تأییدنشده | هنوز روی رایانه کاربر اجرا نشده است |

## 3. مبنای فنی فعلی

- FastAPI + SQLAlchemy 2 + Alembic + Jinja2، رابط فارسی RTL.
- اجرای محلی Windows با SQLite فایل‌محور در `data/cliniccore.db`.
- Alembic تنها مرجع ایجاد و تغییر schema است؛ از `Base.metadata.create_all` در مسیر نصب استفاده نمی‌شود.
- نصب و اجرا با `setup.bat`، `start.bat` و `stop.bat`.
- ماژول‌های موجود شامل بیماران، نوبت‌ها، اطلاعات مالی ثبت‌شده، پیام‌رسانی، تنظیمات، کاربران و صفحات چاپ.
- سامانه تراکنش مالی واقعی انجام نمی‌دهد؛ اطلاعات مالی صرفاً در حد ثبت سوابق تعریف‌شده در محصول است.

## 4. Sprint 0 — Windows & SQLite

- اسکریپت نصب اولیه و bootstrap فایل محلی `.env` اضافه شده است.
- فایل `.env` موجود بازنویسی نمی‌شود و دیتابیس موجود حذف یا reset نمی‌شود.
- اسکریپت‌های start/stop با PID tracking و بررسی هویت process اضافه شده‌اند.
- پشتیبانی timezone ویندوز با `tzdata` تکمیل شده است.
- CI ویندوز روی Windows Server 2025 / Python 3.12.10:
  - compileall: موفق
  - pytest: **29 passed, 0 failed**
  - مهاجرت SQLite تمیز تا revision `20261005_0005`: موفق
- PR #14 ادغام شده است.
- نصب، اجرا، توقف و حفظ داده روی رایانه Windows کاربر: **هنوز دستی تأیید نشده است**.

## 5. Sprint 1 — User Administration & RBAC

- مدل‌های Role، Permission و RolePermission و migration شماره `20261106_0006` اضافه شده‌اند.
- پنج نقش پایه: admin، clinic_manager، doctor، secretary و accountant.
- کنترل دسترسی در سمت سرور و به‌روزرسانی permissionهای کاربر در هر درخواست.
- مدیریت کاربران، فعال/غیرفعال‌سازی، تغییر اطلاعات و reset رمز یک‌بارمصرف.
- ماتریس مجوزها برای نقش‌های غیرمدیر سیستم؛ مجوزهای admin غیرقابل‌تغییر.
- جلوگیری از حذف/تنزل آخرین مدیر فعال و محدودیت مدیر کلینیک در مدیریت حساب مدیر سیستم.
- CSRF برای فرم‌های حساس و چرخش session پس از ورود.
- CI ویندوز run #93:
  - compileall: موفق
  - pytest: **40 passed, 0 failed**
  - مهاجرت SQLite تمیز تا `20261106_0006`: موفق
  - آزمون ارتقای دیتابیس دارای داده قبلی و حفظ username، role و password hash: موفق
- PR #15 ادغام شده است.
- پذیرش دستی نقش‌ها و فرم‌ها روی رایانه کاربر: **هنوز انجام نشده است**.

## 6. Dynamic UI Themes — پیاده‌سازی ادغام‌شده

- چهار preset بصری: Clinical Light، Modern Dark، Soft Neutral و High Contrast.
- تنظیمات اعتبارسنجی‌شده `app.style` و `app.font_scale`؛ تنظیمات قبلی حالت نمایش، رنگ اصلی و تراکم حفظ شده‌اند.
- پیش‌نمایش زنده در صفحه تنظیمات مدیر، بدون ذخیره تا زمان submit.
- stylesheet مجزا برای تم‌ها و کنترل‌گر preview.
- صفحه‌های چاپ باید مستقل از تم برنامه، با پالت روشن و مناسب کاغذ باقی بمانند.
- تنظیم ظاهر فعلاً پیش‌فرض سراسری و تحت مدیریت مدیر سیستم است؛ override مستقل برای هر کاربر در این مرحله وجود ندارد.
- PR #17 ادغام شده است.
- CI روی شاخه یکپارچه‌شده، run #105:
  - نصب وابستگی‌ها: موفق
  - compileall: موفق
  - pytest: موفق
  - مهاجرت SQLite تمیز: موفق
- پذیرش بصری دستی روی مرورگر و Windows کاربر: **هنوز انجام نشده است**.
- پس از ادغام، اتصال اندازه فونت به مقیاس ریشه CSS اصلاح شد؛ CI ویندوز run #109 این اصلاح را تأیید کرد.

## 7. شواهد CI

- Jalali date/time hardening: [Windows CI run #116](https://github.com/kokoosabzi/ClinicCore/actions/runs/42286509958) — **50 passed, 0 failed**, SQLite migration موفق.

- Sprint 0: [Windows CI run #103](https://github.com/kokoosabzi/ClinicCore/actions/runs/42192657181) — بعد از ادغام PR #14 روی main
- Sprint 1: [Windows CI run #93](https://github.com/kokoosabzi/ClinicCore/actions/runs/42190638528)
- Dynamic UI Themes (consolidated): [Windows CI run #105](https://github.com/kokoosabzi/ClinicCore/actions/runs/42192980523)

- اعتبارسنجی strict ورودی تاریخ/زمان و آزمون تاریخ‌های مرزی جلالی به `datetime_service` اضافه شد؛ Windows CI run #116 موفق شد: **50 passed, 0 failed** و مهاجرت SQLite نیز موفق بود. CI تعداد 85 warning گزارش کرد که باید جداگانه triage شود.

## 8. کارهای باقیمانده و دروازه انتشار

1. اجرای `setup.bat` روی Windows هدف و بررسی نصب اولیه، ساخت admin، start/stop و حفظ دیتابیس موجود؛ بدون حذف `.env` یا `data`.
2. بررسی دستی Login، تغییر اجباری رمز، مدیریت کاربران، ماتریس نقش‌ها و مسیرهای مجاز/غیرمجاز.
3. بررسی بصری هر چهار تم، رنگ اصلی، اندازه فونت، تراکم و واکنش‌گرایی صفحه‌ها.
4. بررسی چاپ در حالت‌های روشن و تیره و اطمینان از خروجی کاغذی مستقل از تم برنامه.
5. بررسی و اولویت‌بندی هشدارهای dependency/deprecation ثبت‌شده در CI.
6. بررسی دامنه دسترسی رکوردی؛ محدودیت فعلی عمدتاً در سطح ماژول/عملیات است و مالکیت رکوردی پزشک به‌صورت کامل پیاده‌سازی نشده است.
7. بررسی نیاز به توسعه بعدی در تقویم/ورودی جلالی و جریان نوبت‌دهی پس از پذیرش دستی نسخه فعلی.

- README و `docs/ARCHITECTURE.md` نیز با وضعیت واقعی RBAC، تقویم جلالی، محدودیت‌های دسترسی رکوردی و قابلیت‌های باقی‌مانده هماهنگ شدند.

## 9. قاعده ادامه توسعه

- ادامه کار از `main` انجام شود تا وقتی کاربر ساخت شاخه فعال دیگری را صریحاً تأیید کند.
- هر مرحله شامل تغییر محدود، تست مرتبط، به‌روزرسانی مستندات و گزارش commit باشد.
- ادغام یا حذف شاخه در آینده بدون مجوز صریح کاربر انجام نشود.
- هیچ‌یک از دروازه‌های پذیرش دستی تا زمان اجرای واقعی روی Windows کاربر Pass اعلام نشود.


### 2026-11-06 — Shared date picker for financial forms
- Added a reusable Jalali calendar widget for date-only form fields.
- Payment and expense forms now honor the configured calendar: Jalali picker for Jalali mode, native browser date picker for Gregorian mode.
- Picker selection submits a Gregorian ISO date; persistence remains Gregorian `date` and does not depend on browser locale.
- Added integration tests for picker rendering and persisted payment/expense dates.
- Windows CI run #128 passed: **53 passed, 0 failed**, compileall passed and clean SQLite migration reached `20261106_0006`. Manual browser acceptance remains outstanding.

- Evidence: [Windows CI run #128](https://github.com/kokoosabzi/ClinicCore/actions/runs/42287251826) — **53 passed, 0 failed**.


### 2026-11-07 — Appointment lifecycle and rescheduling
- Added server-side appointment transition rules for booked, rescheduled, waiting, completed, no-show and cancelled states.
- Added status update, cancellation and rescheduling API/form routes with permission checks and CSRF on browser forms.
- Cancellation keeps the historical appointment row but releases its slot; the availability endpoint and partial unique index both exclude cancelled appointments.
- Rescheduling reuses the Jalali booking calendar, preserves the patient and other booking details, checks slot conflicts and records an audit event.
- Status transitions and rescheduling record actor and before/after values in the existing audit log.
- Added lifecycle integration tests for valid/invalid transitions, cancellation slot reuse, reschedule conflict and audit events.
- Windows CI run #150 passed: **58 passed, 0 failed**, compileall, JavaScript syntax validation and clean SQLite migration to \`20261107_0007\` all passed.
- Manual Windows/browser acceptance remains outstanding; practitioner-specific schedules and configurable slot duration are not implemented yet.


### 2026-11-07 — Configurable clinic-wide appointment schedule
- Added administrator settings for clinic opening/closing time, slot duration (15/20/30/45/60 minutes) and working weekdays.
- Defaults preserve the prior 09:00–17:00, 30-minute schedule and six-day week with Friday closed.
- Availability generation now reads persisted settings, excludes non-working weekdays, marks occupied/past slots and returns the configured slot duration.
- The booking UI displays configured hours/duration and explains when the clinic is closed on the selected day.
- Added validation for time format, weekday values, at least one working day and exact divisibility of workday duration by slot duration.
- No schema migration was required; settings use the existing key/value settings store.
- Windows CI run #171 passed: **71 passed, 0 failed**, compileall, JavaScript syntax validation and clean SQLite migration passed.
- Manual browser acceptance remains outstanding. Schedule settings are currently clinic-wide; practitioner-specific hours, leave/holiday exceptions and room/resource allocation remain future work.
