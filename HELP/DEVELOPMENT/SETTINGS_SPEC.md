# ClinicCore — Settings Specification

## 1. هدف

Settings باید یک subsystem مستقل باشد که configuration قابل تغییر از UI را مدیریت کند.

## 2. دسته‌بندی

```text
Settings
├── General
├── Clinic Identity
├── Appearance
├── Date & Time
├── Messaging
├── Contacts
├── Reporting
├── Printing
└── System
```

## 3. مدل پیشنهادی

Agent ابتدا مدل‌های فعلی را بررسی کند. در صورت نبود ساختار مناسب، یک مدل مرکزی مانند زیر ایجاد شود:

```text
system_settings
----------------
id
key
value
value_type
category
description
is_public
updated_at
updated_by
```

یا مدل typed/grouped مناسب دیگری که با معماری موجود سازگارتر باشد.

**قبل از ایجاد مدل جدید، مدل‌های موجود بررسی شوند.**

## 4. Typed Values

مقادیر نباید همگی string بدون قرارداد باشند.

حداقل typeها:
- string
- integer
- boolean
- json

مثلاً:

```text
appearance.theme = "modern"
appearance.dark_mode = true
appearance.font_size = 15
```

## 5. Settings Service

یک service مرکزی مانند:

```python
get(key, default=None)
set(key, value, user=None)
get_group(category)
```

در صورت نیاز cache سبک داشته باشد.

هیچ template نباید مستقیماً به DB وصل شود.

## 6. Application Identity

کلیدهای پیشنهادی:

```text
app.name
app.title
clinic.name
clinic.address
clinic.phone
clinic.email
clinic.logo
clinic.header_text
clinic.footer_text
```

## 7. Appearance

```text
appearance.theme
appearance.mode
appearance.primary_color
appearance.secondary_color
appearance.font_family
appearance.font_size
appearance.density
```

مقادیر باید validation داشته باشند.

## 8. Date & Time

```text
datetime.calendar = jalali|gregorian
datetime.timezone
datetime.date_format
datetime.time_format
datetime.show_seconds
```

timezone باید از تنظیمات معتبر سیستم/کتابخانه استفاده کند و در business data با presentation format اشتباه نشود.

## 9. Messaging

Credentials حساس:
- API key
- token
- secret

نباید در HTML یا log نمایش داده شوند.

کلیدهای منطقی:

```text
messaging.enabled
messaging.default_provider
messaging.sender
messaging.provider.<name>....
```

Secretها باید در secret/config mechanism مناسب نگهداری شوند؛ Settings UI فقط در صورت نیاز مقدار masked نشان دهد.

## 10. Reporting

```text
reports.logo
reports.header
reports.footer
reports.default_format
reports.include_timestamp
```

## 11. Printing

```text
print.paper_size
print.margin_top
print.margin_right
print.margin_bottom
print.margin_left
print.show_logo
print.show_header
print.show_footer
```

## 12. API/Routes

Routeهای پیشنهادی:

```text
GET  /settings
POST /settings
POST /settings/test-messaging
POST /settings/reset-theme
```

این نام‌ها قطعی نیستند؛ Agent باید با routing conventions فعلی هماهنگ شود.

## 13. Permission

Settings حساس فقط برای نقش مجاز قابل تغییر باشد.

حداقل:
- appearance: administrator
- identity: administrator
- messaging credentials: administrator
- system/database: administrator

## 14. Validation

هر setting:
- type validation
- range validation
- enum validation در موارد لازم
- sanitization برای متن‌های قابل نمایش

## 15. UI

صفحه Settings باید:
- sidebar/tab داشته باشد
- save feedback بدهد
- خطاها را inline نشان دهد
- تغییرات unsaved را مشخص کند
- برای secretها مقدار را mask کند
- reset به default داشته باشد

## 16. Acceptance

- تغییر نام سامانه در UI قابل مشاهده باشد.
- تغییر theme روی صفحات اصلی اعمال شود.
- restart برنامه settings را حفظ کند.
- کاربر غیرمجاز نتواند settings حساس را تغییر دهد.
- secret در source/template/log ظاهر نشود.
