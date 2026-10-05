from zoneinfo import ZoneInfo, available_timezones

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.system_setting import SystemSetting


DEFAULTS: dict[str, tuple[str, str, str]] = {
    "app.name": ("ClinicCore", "string", "نام داخلی سامانه"),
    "app.title": ("کلینیک‌کور", "string", "عنوان نمایشی سامانه"),
    "app.theme": ("system", "enum", "حالت نمایش: روشن، تاریک یا سیستم"),
    "app.density": ("comfortable", "enum", "تراکم نمایش: راحت یا فشرده"),
    "clinic.name": ("", "string", "نام کلینیک"),
    "clinic.address": ("", "string", "آدرس کلینیک"),
    "clinic.phone": ("", "string", "تلفن کلینیک"),
    "clinic.email": ("", "string", "ایمیل کلینیک"),
    "clinic.logo": ("", "string", "مسیر یا شناسه لوگوی کلینیک"),
    "clinic.header_text": ("", "string", "متن سربرگ"),
    "clinic.footer_text": ("", "string", "متن پاورقی"),
    "datetime.calendar": ("jalali", "enum", "تقویم نمایشی: جلالی یا میلادی"),
    "datetime.timezone": ("Asia/Tehran", "timezone", "منطقه زمانی سامانه"),
    "datetime.date_format": ("YYYY/MM/DD", "enum", "قالب نمایش تاریخ"),
    "datetime.time_format": ("24", "enum", "قالب نمایش ساعت: ۱۲ یا ۲۴ ساعته"),
    "datetime.show_seconds": ("false", "boolean", "نمایش ثانیه در ساعت"),
    "reports.logo": ("", "string", "لوگوی گزارش"),
    "reports.header": ("", "string", "سربرگ گزارش"),
    "reports.footer": ("", "string", "پاورقی گزارش"),
    "reports.default_format": ("html", "enum", "قالب پیش‌فرض گزارش"),
    "reports.include_timestamp": ("true", "boolean", "نمایش زمان تولید گزارش"),
    "messaging.enabled": ("false", "boolean", "فعال بودن سامانه پیام‌رسانی"),
    "messaging.default_provider": ("sms", "enum", "ارائه‌دهنده پیش‌فرض پیام"),
    "contacts.enabled": ("true", "boolean", "فعال بودن مدیریت اطلاعات تماس"),
    "contacts.require_phone": ("false", "boolean", "الزام ثبت شماره تماس"),
    "print.paper_size": ("A4", "enum", "اندازه کاغذ چاپ"),
    "print.margin_top": ("10", "integer", "حاشیه بالای چاپ بر حسب میلی‌متر"),
    "print.margin_right": ("10", "integer", "حاشیه راست چاپ بر حسب میلی‌متر"),
    "print.margin_bottom": ("10", "integer", "حاشیه پایین چاپ بر حسب میلی‌متر"),
    "print.margin_left": ("10", "integer", "حاشیه چپ چاپ بر حسب میلی‌متر"),
    "print.show_logo": ("true", "boolean", "نمایش لوگو در چاپ"),
    "print.show_header": ("true", "boolean", "نمایش سربرگ در چاپ"),
    "print.show_footer": ("true", "boolean", "نمایش پاورقی در چاپ"),
    "system.audit_enabled": ("true", "boolean", "فعال بودن ثبت رویدادهای سامانه"),
}

ALLOWED_VALUES: dict[str, set[str]] = {
    "app.theme": {"light", "dark", "system"},
    "app.density": {"comfortable", "compact"},
    "datetime.calendar": {"jalali", "gregorian"},
    "datetime.date_format": {"YYYY/MM/DD", "YYYY-MM-DD", "DD/MM/YYYY", "DD-MM-YYYY"},
    "datetime.time_format": {"12", "24"},
    "datetime.show_seconds": {"true", "false"},
    "reports.default_format": {"html", "csv", "pdf"},
    "reports.include_timestamp": {"true", "false"},
    "messaging.enabled": {"true", "false"},
    "messaging.default_provider": {"sms", "email", "telegram", "whatsapp", "iranian_messenger"},
    "contacts.enabled": {"true", "false"},
    "contacts.require_phone": {"true", "false"},
    "print.paper_size": {"A4", "A5", "thermal"},
    "print.show_logo": {"true", "false"},
    "print.show_header": {"true", "false"},
    "print.show_footer": {"true", "false"},
    "system.audit_enabled": {"true", "false"},
}


class SettingsService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, key: str, default=None):
        setting = self.db.scalar(select(SystemSetting).where(SystemSetting.key == key))
        if setting is None:
            return DEFAULTS.get(key, (default, "string", ""))[0]
        return setting.value

    def get_group(self, category: str) -> dict[str, str | None]:
        prefix = f"{category}."
        result = {key: value[0] for key, value in DEFAULTS.items() if key.startswith(prefix)}
        rows = self.db.scalars(select(SystemSetting).where(SystemSetting.category == category)).all()
        for row in rows:
            result[row.key] = row.value
        return result

    def _validate(self, key: str, value: str | None) -> None:
        if key not in DEFAULTS:
            raise ValueError(f"Unknown setting: {key}")
        if key in ALLOWED_VALUES and value not in ALLOWED_VALUES[key]:
            raise ValueError(f"Invalid value for setting: {key}")
        if key.startswith("print.margin_"):
            try:
                margin = int(value or "")
            except (TypeError, ValueError) as error:
                raise ValueError("Invalid print margin") from error
            if margin < 0 or margin > 100:
                raise ValueError("Invalid print margin")
        if key == "datetime.timezone":
            if not value or value not in available_timezones():
                raise ValueError("Invalid timezone")
            ZoneInfo(value)
        if value is not None and len(value) > 4000:
            raise ValueError("Setting value is too long")

    def set(self, key: str, value: str | None, user_id: int | None = None) -> SystemSetting:
        self._validate(key, value)
        setting = self.db.scalar(select(SystemSetting).where(SystemSetting.key == key))
        default_value, value_type, description = DEFAULTS[key]
        if setting is None:
            setting = SystemSetting(
                key=key,
                value=value,
                value_type=value_type,
                category=key.split(".", 1)[0],
                description=description,
                is_public=key in {
                    "app.name", "app.title", "app.theme", "app.density",
                    "clinic.name", "clinic.logo", "clinic.header_text", "clinic.footer_text",
                    "datetime.calendar", "datetime.timezone", "datetime.date_format",
                    "datetime.time_format", "datetime.show_seconds",
                    "reports.logo", "reports.header", "reports.footer",
                    "reports.default_format", "reports.include_timestamp",
                    "messaging.enabled", "messaging.default_provider",
                    "contacts.enabled", "contacts.require_phone",
                    "print.paper_size", "print.margin_top", "print.margin_right",
                    "print.margin_bottom", "print.margin_left", "print.show_logo",
                    "print.show_header", "print.show_footer",
                    "system.audit_enabled",
                },
                updated_by=user_id,
            )
            self.db.add(setting)
        else:
            setting.value = value
            setting.updated_by = user_id
        self.db.commit()
        self.db.refresh(setting)
        return setting

    def set_many(self, values: dict[str, str | None], user_id: int | None = None) -> None:
        for key, value in values.items():
            self._validate(key, value)
        for key, value in values.items():
            self.set(key, value, user_id=user_id)
