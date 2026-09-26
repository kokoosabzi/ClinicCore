# ClinicCore — Acceptance Tests

## 1. هدف

این سند معیار پذیرش فاز توسعه است. Testهای زیر باید در طول توسعه به تست خودکار یا manual checklist تبدیل شوند.

## 2. Baseline

### AT-001 — Application startup
- برنامه با configuration معتبر بالا می‌آید.
- `/health` پاسخ معتبر می‌دهد.
- خطای import/ASGI وجود ندارد.

### AT-002 — Python compilation
```text
python -m compileall app
```
باید موفق باشد.

### AT-003 — Existing core flows
مسیرهای اصلی موجود نباید شکسته شوند:
- login
- dashboard
- patients
- appointments
- financial
- messages
- print

## 3. Settings

### AT-101 — Open settings
Admin می‌تواند Settings را باز کند.

### AT-102 — Application title
Admin نام/عنوان سامانه را تغییر می‌دهد.
پس از save:
- header تغییر می‌کند.
- page title در صورت طراحی شدن تغییر می‌کند.
- restart برنامه مقدار حفظ شده را نشان می‌دهد.

### AT-103 — Clinic identity
نام کلینیک، تلفن و اطلاعات اصلی ذخیره و نمایش داده می‌شوند.

### AT-104 — Unauthorized settings
کاربر غیرمجاز نباید settings حساس را تغییر دهد.

## 4. Theme

### AT-201 — Theme selection
Admin theme را تغییر می‌دهد.
- صفحات اصلی theme جدید را نشان می‌دهند.
- نیاز به restart server نیست مگر implementation صراحتاً چنین قراردادی داشته باشد.

### AT-202 — Persistence
پس از refresh/restart، theme حفظ شود.

### AT-203 — Dark mode
Dark mode در صفحات اصلی readable باشد.

## 5. Navigation

### AT-301 — Back button
در صفحات داخلی دکمه بازگشت وجود دارد.

### AT-302 — Breadcrumb
صفحات nested breadcrumb دارند.

### AT-303 — Consistency
Back/Breadcrumb در صفحات:
- patients
- appointments
- financial
- messages
- settings
وجود دارد.

## 6. Calendar

### AT-401 — Jalali display
تاریخ فعلی در Header با تنظیم Jalali نمایش داده شود.

### AT-402 — Appointment date
کاربر می‌تواند تاریخ نوبت را از UI انتخاب کند.

### AT-403 — Persistence
تاریخ ذخیره‌شده پس از reload همان مقدار منطقی را نشان دهد.

### AT-404 — Gregorian boundary
تبدیل در روزهای مرزی سال و ماه بدون خطای off-by-one انجام شود.

## 7. Dashboard

### AT-501 — KPI
KPIهای اصلی از داده واقعی نمایش داده شوند.

### AT-502 — Charts
حداقل دو نمودار meaningful از داده واقعی نمایش داده شود.

### AT-503 — Empty state
اگر داده وجود ندارد، UI crash نکند و empty state نمایش دهد.

## 8. Messaging

### AT-601 — Contact CRUD
Admin می‌تواند contact ایجاد، مشاهده، ویرایش و حذف/غیرفعال کند.

### AT-602 — Provider abstraction
Routerهای domain-specific به provider concrete وابسته نباشند.

### AT-603 — Message result
ارسال موفق/ناموفق در history ثبت شود.

### AT-604 — Secret protection
credential پیام‌رسان در UI/log عمومی نمایش داده نشود.

## 9. Reporting

### AT-701 — Patient report
گزارش بیماران تولید شود.

### AT-702 — Appointment report
گزارش نوبت‌ها تولید شود.

### AT-703 — Financial report
گزارش مالی تولید شود.

### AT-704 — Print
گزارش از layout چاپ مناسب استفاده کند.

## 10. Printing

### AT-801 — Receipt
قبض دارای:
- clinic identity
- logo در صورت تنظیم
- patient
- amount
- date/time
- footer
باشد.

### AT-802 — Print CSS
navigation و عناصر غیرقابل چاپ در print ظاهر نشوند.

### AT-803 — Settings
تغییر logo/header/footer در print اعمال شود.

## 11. SQLite

### AT-901 — Local startup
با SQLite و بدون PostgreSQL/Docker، application در Local deployment بالا بیاید.

### AT-902 — CRUD
عملیات اصلی روی SQLite کار کنند:
- user
- patient
- appointment
- financial
- messaging

### AT-903 — Migration
database از حالت clean با migrationهای تعریف‌شده ساخته شود.

### AT-904 — Persistence
پس از restart، داده‌ها باقی بمانند.

### AT-905 — Backup
Backup قابل ایجاد باشد.

### AT-906 — Restore
Backup روی database test قابل restore باشد.

## 12. Security

### AT-1001 — Authentication
protected route بدون login قابل دسترسی نباشد.

### AT-1002 — Password
password به صورت plaintext ذخیره نشود.

### AT-1003 — CSRF
formهای حساس در صورت استفاده از session/form با CSRF محافظت شوند.

### AT-1004 — Audit
عملیات حساس audit شوند.

## 13. Regression

پس از هر phase حداقل smoke test:

```text
login
dashboard
patient create/view
appointment create/view
financial create/view
message create/view
print
settings
logout
```

## 14. Release Gate

Release زمانی قابل قبول است که:
- acceptance tests اصلی pass باشند.
- migrationها روی DB clean pass شوند.
- SQLite local flow pass شود.
- UI صفحات اصلی یکپارچه باشد.
- Settings persistence pass باشد.
- print output بررسی شده باشد.
- هیچ secret یا فایل موقت commit نشده باشد.
- `git status` و `git diff` بررسی شده باشند.
