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
}

ALLOWED_VALUES: dict[str, set[str]] = {
    "app.theme": {"light", "dark", "system"},
    "app.density": {"comfortable", "compact"},
    "datetime.calendar": {"jalali", "gregorian"},
    "datetime.date_format": {"YYYY/MM/DD", "YYYY-MM-DD", "DD/MM/YYYY", "DD-MM-YYYY"},
    "datetime.time_format": {"12", "24"},
    "datetime.show_seconds": {"true", "false"},
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

    def set(self, key: str, value: str | None, user_id: int | None = None) -> SystemSetting:
        if key not in DEFAULTS:
            raise ValueError(f"Unknown setting: {key}")
        if key in ALLOWED_VALUES and value not in ALLOWED_VALUES[key]:
            raise ValueError(f"Invalid value for setting: {key}")
        if key == "datetime.timezone":
            if not value or value not in available_timezones():
                raise ValueError("Invalid timezone")
            ZoneInfo(value)
        if value is not None and len(value) > 4000:
            raise ValueError("Setting value is too long")
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
            self.set(key, value, user_id=user_id)
