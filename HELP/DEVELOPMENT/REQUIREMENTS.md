# ClinicCore — Functional & Technical Requirements

## 1. اولویت‌ها

اولویت‌ها:

- P0 = ضروری برای release
- P1 = مهم
- P2 = بهبود تکمیلی

## 2. Settings

### P0
سیستم باید صفحه Settings داشته باشد.

تنظیمات عمومی:
- نام سامانه
- عنوان سامانه
- نام کلینیک
- آدرس
- تلفن
- ایمیل
- لوگو
- متن سربرگ/پاورقی

تنظیمات باید persistent باشند و restart برنامه آن‌ها را از بین نبرد.

### P0 — Application Identity

تمام UIهایی که اکنون نام ثابت `ClinicCore` یا عنوان ثابت دیگری دارند باید به تنظیمات مرکزی متصل شوند.

نام داخلی package/project می‌تواند `ClinicCore` باقی بماند؛ تغییر نام نمایشی با تغییر نام repository/package اشتباه نشود.

## 3. Theme

### P0
کاربر باید بتواند theme فعال را از Settings انتخاب کند.

حداقل:
- Light
- Dark
- یک یا چند preset گرافیکی

### P1
- رنگ اصلی
- رنگ ثانویه
- اندازه فونت
- density
- radius
- contrast

تغییر theme نباید نیازمند reload کامل server باشد.

## 4. Navigation

### P0
هر صفحه باید حداقل یک مسیر بازگشت قابل مشاهده داشته باشد.

### P0
صفحات تو در تو باید breadcrumb داشته باشند.

### P0
Header و navigation در تمام صفحات از layout مشترک استفاده کنند.

## 5. Dashboard

### P0
Dashboard باید KPIهای اصلی را نمایش دهد:
- تعداد بیماران
- نوبت‌های امروز
- وضعیت مالی
- پیام‌های اخیر/ناموفق

### P1
نمودار:
- روند نوبت‌ها
- درآمد
- فعالیت‌ها

نمودارها باید از داده واقعی service استفاده کنند، نه داده ساختگی production.

## 6. Calendar

### P0
تاریخ در UI قابلیت نمایش Jalali داشته باشد.

### P0
Appointment باید تاریخ/زمان را با Calendar Service پردازش کند.

### P0
Header تمام صفحات تاریخ و ساعت فعلی را نمایش دهد.

### P1
انتخاب تاریخ با DatePicker مناسب RTL/Jalali انجام شود.

## 7. Messaging

### P0
Messaging باید abstraction داشته باشد.

عملیات پایه:
- ارسال
- تست اتصال
- ثبت نتیجه ارسال

### P0
Contact قابل CRUD باشد.

### P1
- گروه مخاطبین
- template پیام
- تاریخچه
- وضعیت delivery

Provider نباید در routerهای domain-specific hard-code شود.

## 8. Reporting

### P0
گزارش‌های اصلی:
- بیماران
- نوبت‌ها
- مالی
- پیام‌ها
- audit

### P1
خروجی:
- Print
- PDF
- CSV/Excel در صورت وجود dependency و نیاز

## 9. Printing

### P0
قالب چاپ قبض و گزارش از layout مشترک استفاده کند.

قابل تنظیم:
- logo
- clinic name
- header
- footer
- margins
- paper size

### P1
قالب‌های چاپ قابل توسعه باشند بدون copy/paste گسترده.

## 10. Database

### P0
database configuration باید از application logic جدا باشد.

### P0
SQLite باید به‌صورت واقعی روی کل application تست شود.

### P1
backup/restore برای Local deployment.

## 11. Security

### P0
- secretها در env/config باشند.
- passwordها hash شوند.
- CSRF برای formهای حساس حفظ شود.
- session/auth موجود بدون دلیل شکسته نشود.
- audit برای عملیات حساس حفظ شود.

## 12. Accessibility و RTL

### P1
- تمام صفحات RTL باشند.
- keyboard navigation برای عناصر اصلی ممکن باشد.
- contrast قابل قبول باشد.
- formها label واضح داشته باشند.

## 13. Performance

با توجه به حجم پایین داده، پیچیدگی غیرضروری ممنوع است.

از:
- caching پیچیده
- queue infrastructure خارجی
- microservice
- frontend build pipeline سنگین

بدون نیاز واقعی استفاده نشود.

## 14. Compatibility

تغییرات جدید باید قابلیت‌های موجود را حفظ کنند:
- authentication
- patients
- appointments
- financial
- messaging
- users
- health
- print routes

هر تغییر breaking باید مستند و با migration/test همراه باشد.
