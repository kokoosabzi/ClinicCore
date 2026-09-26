# ClinicCore — Master Development Plan

## 1. هدف

این سند برنامه مرجع فاز بازطراحی و توسعه ClinicCore است. هدف، تبدیل وضعیت فعلی پروژه به یک سامانه مدیریت کلینیک با:

- تنظیمات مرکزی و قابل مدیریت از UI
- نام و هویت قابل تنظیم سامانه/کلینیک
- Design System و Theme پویا
- UX یکپارچه و RTL
- تقویم و نمایش تاریخ/زمان هجری شمسی
- Dashboard و Reporting
- Messaging و Contacts
- Print Layout قابل تنظیم
- اجرای Local با SQLite به‌عنوان گزینه deployment نهایی
- معماری قابل نگهداری و مناسب برای توسعه توسط AI Agent

این سند برای Codex/AI Agent نوشته شده و باید همراه با `REQUIREMENTS.md`، `SETTINGS_SPEC.md`، `UX_UI_SPEC.md`، `AGENT_WORKFLOW.md` و `ACCEPTANCE_TESTS.md` خوانده شود.

## 2. وضعیت مبنا

Repository فعلی یک پروژه Python/FastAPI است و ساختار فعلی شامل بخش‌های زیر است:

- `app/core`
- `app/models`
- `app/plugins`
- `app/providers`
- `app/repositories`
- `app/routers`
- `app/schemas`
- `app/services`
- `app/static`
- `app/templates`
- `alembic`
- `tests`
- `HELP`

در فاز فعلی، برنامه اجرا شده و مسیرهای اصلی UI تست شده‌اند. اصلاحات اخیر شامل سازگار کردن `TemplateResponse` با نسخه فعلی Starlette و اضافه شدن `start.bat` بوده است.

**اصل مهم:** Agent باید کد فعلی را قبل از تغییر بررسی کند و قابلیت‌های سالم را بدون دلیل بازنویسی نکند.

## 3. اصول معماری

### 3.1 لایه‌بندی

الگوی فعلی لایه‌ای حفظ شود:

```text
Router -> Service -> Repository -> Model/DB
              |
            Schema
```

قواعد:

- Router محل منطق تجاری اصلی نیست.
- Service محل منطق دامنه است.
- Repository مسئول دسترسی داده است.
- Template نباید منطق تجاری داشته باشد.
- تنظیمات از یک Settings Service مرکزی خوانده شوند.
- قابلیت‌های cross-cutting مانند تاریخ، theme، print و messaging سرویس/abstraction مستقل داشته باشند.

### 3.2 سازگاری با آینده

هر قابلیت جدید باید تا حد امکان مستقل از provider و database باشد.

نمونه:

```text
MessagingService
    -> MessagingProvider
        -> SMSProvider
        -> TelegramProvider
        -> ...
```

و:

```text
Application
    -> SQLAlchemy
        -> SQLite
        -> PostgreSQL
```

## 4. ترتیب فازها

### Phase 0 — Baseline & Specification
- تثبیت تست‌ها
- تعریف قراردادهای معماری
- ایجاد اسناد توسعه
- ایجاد Acceptance Tests

### Phase 1 — Settings & Application Identity
- مدل Settings
- Settings Service/Repository
- UI تنظیمات
- نام سامانه، عنوان، اطلاعات کلینیک، لوگو

### Phase 2 — Design System & UX
- Layout مشترک
- Header/Sidebar
- Back
- Breadcrumb
- Theme
- Typography
- Light/Dark
- responsive behavior

### Phase 3 — Calendar & Date/Time
- Calendar Service
- Jalali/Gregorian conversion
- timezone
- نمایش تاریخ/زمان در Header
- DatePicker مناسب نوبت‌گذاری

### Phase 4 — Dashboard & Reporting
- KPI cards
- Charts
- گزارش‌های اصلی
- export/print

### Phase 5 — Messaging & Contacts
- provider abstraction
- contacts
- templates
- message history
- delivery status

### Phase 6 — Printing
- print design system
- قبض
- گزارش
- سربرگ/پاورقی
- تنظیمات چاپ

### Phase 7 — Local Database
- database abstraction verification
- SQLite deployment
- migration strategy
- backup/restore

### Phase 8 — Final QA
- regression
- security
- permissions
- accessibility
- print
- backup
- deployment

## 5. معیارهای معماری

قبل از تکمیل هر فاز:

1. تست‌های مرتبط سبز باشند.
2. هیچ secret در repository قرار نگیرد.
3. migrationها قابل تکرار باشند.
4. UI از hard-code کردن نام/عنوان سامانه پرهیز کند.
5. تنظیمات در یک نقطه مدیریت شوند.
6. تغییر Theme نیازمند تغییر templateهای متعدد نباشد.
7. قابلیت‌های provider-specific در abstraction پنهان شوند.
8. قابلیت جدید مستند شود.

## 6. تصمیم پایگاه داده

حجم مورد انتظار داده پایین است؛ حدود ۱۰۰۰ رکورد در سال.

هدف نهایی نسخه Local:
- حذف نیاز کاربر عادی به Docker/PostgreSQL
- استفاده از SQLite به‌عنوان گزینه پیش‌فرض Local
- حفظ امکان PostgreSQL برای deploymentهای server/multi-user

بنابراین **فعلاً PostgreSQL را کورکورانه حذف نکنید**. ابتدا وابستگی‌های مستقیم را کم کنید و SQLite را با تست واقعی وارد کنید.

## 7. خروجی مورد انتظار

در پایان فاز:

- Settings کامل و قابل استفاده
- UI/UX یکپارچه
- Theme پویا
- Jalali
- Dashboard
- Reports
- Messaging
- Contacts
- Print
- Local SQLite
- Backup/Restore
- تست‌های پذیرش
- مستندات به‌روز

## 8. قانون مهم برای Agent

هیچ فاز بزرگی در یک commit انجام نشود.

هر قابلیت منطقی:
1. plan
2. implementation
3. test
4. manual verification
5. documentation
6. commit

باشد.
