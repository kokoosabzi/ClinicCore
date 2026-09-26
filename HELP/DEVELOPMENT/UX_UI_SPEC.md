# ClinicCore — UX/UI & Design System Specification

## 1. هدف

رابط کاربری باید یکپارچه، RTL، خوانا، پویا و مناسب استفاده روزانه در محیط کلینیک باشد.

## 2. Global Layout

تمام صفحات باید از layout مشترک استفاده کنند:

```text
┌──────────────────────────────────────────┐
│ Logo | Application Title | Date | Time  │
├────────────┬─────────────────────────────┤
│ Navigation │ Breadcrumb / Back           │
│            │ Page Header                 │
│            │                             │
│            │ Content                     │
└────────────┴─────────────────────────────┘
```

## 3. Header

Header شامل:
- logo
- نام سامانه
- نام کلینیک در صورت تنظیم
- تاریخ
- ساعت
- user menu
- Settings
- logout

نام‌ها باید از Settings Service بیایند.

## 4. Back Button

هر صفحه غیرریشه:
- دکمه «بازگشت» داشته باشد.
- ترجیحاً breadcrumb نیز داشته باشد.

در صورت وجود history:
```text
history.back()
```

اما برای navigation قابل پیش‌بینی، parent route نیز باید تعریف شود.

## 5. Breadcrumb

نمونه:

```text
خانه ← بیماران ← پرونده بیمار
```

هر بخش قابل کلیک باشد، مگر آخرین بخش.

## 6. Design Tokens

تمام componentها باید از tokenها استفاده کنند:

```css
--color-primary
--color-secondary
--color-background
--color-surface
--color-text
--color-muted
--color-border
--color-danger
--color-success

--font-family
--font-size-base
--radius-sm
--radius-md
--radius-lg

--space-1
--space-2
--space-3
--space-4
```

مقدار tokenها از theme تعیین شود.

## 7. Themes

حداقل preset:
- Classic
- Modern
- Dark

نام‌ها نمونه‌اند و Agent می‌تواند با طراحی موجود هماهنگ کند.

Theme باید با CSS variables پیاده شود.

## 8. Typography

فونت فارسی مناسب استفاده شود؛ انتخاب دقیق فونت باید با availability و licensing سازگار باشد.

از hard-code کردن font در هر template پرهیز شود.

## 9. Components

حداقل componentهای مشترک:

```text
PageHeader
BackButton
Breadcrumb
Card
Button
Input
Select
DatePicker
Modal
Alert
Table
Pagination
EmptyState
LoadingState
ConfirmDialog
```

## 10. Tables

جدول‌ها باید:
- responsive باشند.
- empty state داشته باشند.
- actionها را واضح نشان دهند.
- در صفحات طولانی pagination/filter داشته باشند.

## 11. Forms

هر field:
- label
- validation
- error message
- مناسب RTL

را داشته باشد.

## 12. Responsive

حداقل desktop و tablet باید usable باشند. اگر موبایل پشتیبانی می‌شود، navigation باید collapse شود.

## 13. Dashboard UX

Dashboard باید:
- اطلاعات مهم را در نگاه اول نشان دهد.
- نمودارها title و legend واضح داشته باشند.
- empty state داشته باشد.
- داده ساختگی production نداشته باشد.

## 14. Date/Time UI

Header:
```text
شنبه ۵ مهر ۱۴۰۵
14:35
```

فرمت دقیق از Settings می‌آید.

## 15. Feedback

برای عملیات:
- success message
- error message
- confirmation برای destructive actions

وجود داشته باشد.

## 16. Print UX

صفحه print نباید UI معمول navigation را چاپ کند.

از print-specific stylesheet استفاده شود:

```css
@media print {
    ...
}
```

## 17. Rule برای Agent

Agent نباید برای هر صفحه یک CSS مستقل و تکراری بسازد.

ابتدا component مشترک بساز، سپس صفحات را migrate کن.

## 18. Visual Acceptance

صفحات اصلی:
- login
- dashboard
- patients
- appointments
- financial
- messages
- settings

باید از layout و component system مشترک استفاده کنند.
