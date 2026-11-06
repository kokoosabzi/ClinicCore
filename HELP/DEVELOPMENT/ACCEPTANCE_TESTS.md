# ClinicCore — Acceptance Tests

این چک‌لیست معیار پذیرش نسخه محلی ClinicCore است. تستی که اجرا نشده نباید Pass علامت بخورد.

## AT-001 — Startup and health
- برنامه با تنظیمات معتبر بالا بیاید.
- `/health` پاسخ `{"status":"ok"}` بدهد.

## AT-002 — Python checks
```powershell
python -m compileall app tests main.py alembic scripts
python -m pytest -q
```
هر دو دستور باید موفق باشند.

## AT-003 — Core regression
- ورود و خروج
- داشبورد
- ایجاد/مشاهده بیمار
- ایجاد/مشاهده نوبت
- صفحات مالی
- پیام‌ها
- چاپ رسید
- تنظیمات

## AT-004 — Migration
- یک فایل SQLite تازه با `alembic upgrade head` ساخته شود.
- revision نهایی `20261005_0005` باشد.
- index یکتای نوبت فعال موجود باشد.
- downgrade/upgrade فقط در دیتابیس آزمایشی و پس از بررسی اثر داده انجام شود.

## AT-005 — Authentication
- مسیر محافظت‌شده بدون login قابل دسترسی نباشد.
- رمز plaintext ذخیره نشود.
- مدیر تازه در اولین ورود مجبور به تغییر رمز باشد.
- فرم حساس CSRF داشته باشد.

## AT-006 — Persian date and print
- تاریخ شمسی در ورودی/نمایش نوبت درست باشد.
- چاپ رسید در تم روشن باشد.
- تاریخ و وضعیت رسید فارسی و قابل خواندن باشند.

## AT-007 — Windows fresh installation
1. روی clone تازه `setup.bat` اجرا شود.
2. `.venv` ساخته و وابستگی‌ها نصب شوند.
3. `.env` جدید با secret و رمز مدیر تصادفی ساخته شود.
4. migrationها اجرا و مدیر اولیه ایجاد شود.
5. رمز اولیه فقط در خروجی setup نمایش داده شود و در اولین ورود تغییر کند.

## AT-008 — Windows start/stop
- `start.bat` سرور را روی `127.0.0.1:8000` اجرا کند.
- درخواست به `/health` موفق باشد.
- اجرای دوباره start باعث اجرای سرور دوم روی همان پورت نشود.
- `stop.bat` فقط فرایند متعلق به ClinicCore را متوقف کند.
- فرایندهای Python/Uvicorn نامرتبط دست‌نخورده بمانند.

## AT-009 — Persistence and data safety
- بعد از restart داده‌های ثبت‌شده باقی بمانند.
- setup/start دیتابیس موجود را حذف یا جایگزین نکنند.
- فایل `.env`، دیتابیس، PID و آپلودهای runtime در Git نباشند.
- پیش از restore یا migration روی داده واقعی، backup مستقل تهیه شود.

## Release gate
انتشار فقط پس از اجرای تست‌های خودکار، تست واقعی Windows، بررسی مرورگر، مسیرهای اصلی و backup/restore قابل قبول است.
