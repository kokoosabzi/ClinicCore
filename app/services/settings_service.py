from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.system_setting import SystemSetting


DEFAULTS: dict[str, tuple[str, str, str]] = {
    "app.name": ("ClinicCore", "string", "نام داخلی سامانه"),
    "app.title": ("کلینیک‌کور", "string", "عنوان نمایشی سامانه"),
    "clinic.name": ("", "string", "نام کلینیک"),
    "clinic.address": ("", "string", "آدرس کلینیک"),
    "clinic.phone": ("", "string", "تلفن کلینیک"),
    "clinic.email": ("", "string", "ایمیل کلینیک"),
    "clinic.logo": ("", "string", "مسیر یا شناسه لوگوی کلینیک"),
    "clinic.header_text": ("", "string", "متن سربرگ"),
    "clinic.footer_text": ("", "string", "متن پاورقی"),
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
                is_public=key in {"app.name", "app.title", "clinic.name", "clinic.logo", "clinic.header_text", "clinic.footer_text"},
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
