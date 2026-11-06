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

### AT-204 — Visual presets and live preview
- Administrator can select Clinical Light, Modern Dark, Soft Neutral, or High Contrast.
- Settings form updates its preview immediately without submitting.
- Invalid preset/font-scale values are rejected server-side.
- Selected preset, accent color, font scale, and density persist after refresh/restart.
- Print views remain light and readable regardless of the selected application preset.

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


## 15. Windows Local Installation & Runtime (Sprint 0)

### AT-1101 — Fresh setup
- On a clean Windows clone, `setup.bat` creates `.venv`, installs dependencies, bootstraps a private `.env`, applies Alembic migrations, and creates the initial admin.
- The generated admin password is unique and printed once; first login requires a password change.
- An existing `.env` is never overwritten.

### AT-1102 — SQLite-only configuration
- A fresh file-backed SQLite database is created at `data/cliniccore.db`.
- Non-SQLite `DATABASE_URL` values fail with a clear error.
- No PostgreSQL database, Docker container, or volume is deleted or modified.

### AT-1103 — Start and stop
- `start.bat` starts the application on `127.0.0.1:8000` and verifies `/health`.
- A second start does not create a duplicate server.
- `stop.bat` stops only the process recorded by the ClinicCore PID file and verifies its executable/command line.
- Unrelated Python/Uvicorn processes remain running.

### AT-1104 — Persistence
- Create a patient and appointment, stop the app, restart it, and verify that records remain.
- No setup/start operation replaces or deletes an existing database file.

### AT-1105 — Windows regression
- Login, mandatory password change, dashboard, patient workflow, appointment workflow, financial pages, settings, receipt print, and logout are manually checked in a browser.
- Record the Windows version, Python version, test result, and any failure in PROGRESS.md.


## 16. User Administration & RBAC (Sprint 1)

### AT-1201 — Additive role migration
- Upgrade an existing 0005 database to the RBAC head revision without deleting users or changing existing password hashes.
- Built-in roles and permission grants are seeded exactly once.
- Alembic remains the only schema creation/migration path.

### AT-1202 — User lifecycle
- System administrator can create, edit, deactivate/reactivate and reset passwords for user accounts.
- New users receive only a password hash and must change the initial password at first login.
- Duplicate usernames are rejected.
- Inactive users cannot authenticate; an already-open session is rejected on the next protected request.
- User responses never include password hashes or plaintext passwords except the one-time reset result.

### AT-1203 — Role permissions
- Default roles are system administrator, clinic manager, doctor, secretary and accountant.
- The administrator can edit built-in non-admin role permissions.
- Administrator permissions are immutable and always include all permission codes.
- A non-administrator cannot grant the role-management permission to itself or another role.
- A clinic manager cannot create/promote, modify, deactivate or reset the password of a system administrator.

### AT-1204 — Server-side route enforcement
- Unauthenticated access to protected HTML/API routes is rejected.
- Authenticated users lacking a permission receive HTTP 403.
- Permissions are reloaded from the database, so role/permission changes take effect without a server restart.
- Hiding a menu item is not considered sufficient authorization.

### AT-1205 — Least-privilege data visibility
- Doctors and receptionists cannot access financial pages, API endpoints, or financial dashboard totals by default.
- Accountants cannot access clinical patient charts by default.
- Patient detail pages show appointments and payment history only when the corresponding permissions are present.
- Dashboard cards and create shortcuts are filtered by effective permissions.

### AT-1206 — Forced password change and session behavior
- A user marked for password change cannot access dashboard or domain pages until changing the password.
- Successful login rotates the session.
- Deactivated users and changed role permissions take effect on the next request.

### AT-1207 — CSRF protection
- Login, logout, password-change, user-management, and role-permission browser forms reject missing or invalid CSRF tokens.

### AT-1208 — Administrator safety
- The last active system administrator cannot be deactivated or demoted.
- A user cannot deactivate their own account.
- Password reset secrets are never written to audit details or ordinary user listings.



### AT-405 — Strict Jalali date/time parsing
- Valid Jalali leap-day and year-boundary values convert to the expected Gregorian date.
- Persian digits are accepted in date/time values.
- Malformed values, trailing text, seconds when minute precision is expected, invalid times, invalid calendar names and out-of-range dates are rejected.


### AT-406 — Jalali date picker in financial forms
- When the configured calendar is Jalali, payment and expense forms display a calendar picker with Persian month/day labels and no free-text date entry.
- Selecting a Jalali date writes its equivalent Gregorian ISO date to the form payload.
- When the configured calendar is Gregorian, the browser-native date picker remains available.
- Payment and expense POST handlers persist the selected Gregorian date without shifting the calendar day.
- Keyboard focus, open/close state and small-screen layout remain usable.
