from collections.abc import Generator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db(request: Request) -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        from app.services.settings_service import SettingsService

        service = SettingsService(db)
        app_settings = service.get_group("app")
        datetime_settings = service.get_group("datetime")
        report_settings = service.get_group("reports")
        messaging_settings = service.get_group("messaging")
        request.state.app_name = app_settings.get("app.name") or settings.app_name
        request.state.app_title = app_settings.get("app.title") or settings.app_name
        request.state.app_theme = app_settings.get("app.theme") or "system"
        request.state.app_density = app_settings.get("app.density") or "comfortable"
        request.state.datetime_calendar = datetime_settings.get("datetime.calendar") or "jalali"
        request.state.datetime_timezone = datetime_settings.get("datetime.timezone") or "Asia/Tehran"
        request.state.datetime_date_format = datetime_settings.get("datetime.date_format") or "YYYY/MM/DD"
        request.state.datetime_time_format = datetime_settings.get("datetime.time_format") or "24"
        request.state.datetime_show_seconds = datetime_settings.get("datetime.show_seconds") or "false"
        request.state.reports_default_format = report_settings.get("reports.default_format") or "html"
        request.state.reports_include_timestamp = report_settings.get("reports.include_timestamp") or "true"
        request.state.messaging_enabled = messaging_settings.get("messaging.enabled") or "false"
        request.state.messaging_default_provider = messaging_settings.get("messaging.default_provider") or "sms"
    except Exception:
        request.state.app_name = settings.app_name
        request.state.app_title = settings.app_name
        request.state.app_theme = "system"
        request.state.app_density = "comfortable"
        request.state.datetime_calendar = "jalali"
        request.state.datetime_timezone = "Asia/Tehran"
        request.state.datetime_date_format = "YYYY/MM/DD"
        request.state.datetime_time_format = "24"
        request.state.datetime_show_seconds = "false"
        request.state.reports_default_format = "html"
        request.state.reports_include_timestamp = "true"
        request.state.messaging_enabled = "false"
        request.state.messaging_default_provider = "sms"
    try:
        yield db
    finally:
        db.close()
