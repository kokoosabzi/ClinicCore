from collections.abc import Generator
from pathlib import Path

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings
from app.services.datetime_service import format_current_datetime


class Base(DeclarativeBase):
    pass


database_url = make_url(settings.database_url)
connect_args = {}
if database_url.drivername.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    # File-backed SQLite databases need their parent directory to exist.
    if database_url.database and database_url.database != ":memory:":
        Path(database_url.database).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args=connect_args,
)
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
        request.state.app_primary_color = app_settings.get("app.primary_color") or "#176b67"
        clinic_settings = service.get_group("clinic")
        request.state.clinic_name = clinic_settings.get("clinic.name") or ""
        request.state.clinic_logo = clinic_settings.get("clinic.logo") or ""
        request.state.clinic_address = clinic_settings.get("clinic.address") or ""
        request.state.clinic_phone = clinic_settings.get("clinic.phone") or ""
        request.state.clinic_email = clinic_settings.get("clinic.email") or ""
        request.state.clinic_header_text = clinic_settings.get("clinic.header_text") or ""
        request.state.clinic_footer_text = clinic_settings.get("clinic.footer_text") or ""
        request.state.datetime_calendar = datetime_settings.get("datetime.calendar") or "jalali"
        request.state.datetime_timezone = datetime_settings.get("datetime.timezone") or "Asia/Tehran"
        request.state.datetime_date_format = datetime_settings.get("datetime.date_format") or "YYYY/MM/DD"
        request.state.datetime_time_format = datetime_settings.get("datetime.time_format") or "24"
        request.state.datetime_show_seconds = datetime_settings.get("datetime.show_seconds") or "false"
        request.state.current_datetime = format_current_datetime(
            request.state.datetime_timezone,
            request.state.datetime_calendar,
            request.state.datetime_date_format,
            request.state.datetime_time_format,
            request.state.datetime_show_seconds == "true",
        )
        request.state.reports_default_format = report_settings.get("reports.default_format") or "html"
        request.state.reports_include_timestamp = report_settings.get("reports.include_timestamp") or "true"
        request.state.messaging_enabled = messaging_settings.get("messaging.enabled") or "false"
        request.state.messaging_default_provider = messaging_settings.get("messaging.default_provider") or "sms"
        contact_settings = service.get_group("contacts")
        print_settings = service.get_group("print")
        request.state.contacts_enabled = contact_settings.get("contacts.enabled") or "true"
        request.state.contacts_require_phone = contact_settings.get("contacts.require_phone") or "false"
        request.state.print_paper_size = print_settings.get("print.paper_size") or "A4"
        request.state.print_margin_top = print_settings.get("print.margin_top") or "10"
        request.state.print_margin_right = print_settings.get("print.margin_right") or "10"
        request.state.print_margin_bottom = print_settings.get("print.margin_bottom") or "10"
        request.state.print_margin_left = print_settings.get("print.margin_left") or "10"
        request.state.print_show_logo = print_settings.get("print.show_logo") or "true"
        request.state.print_show_header = print_settings.get("print.show_header") or "true"
        request.state.print_show_footer = print_settings.get("print.show_footer") or "true"
        request.state.print_title = print_settings.get("print.title") or ""
        request.state.print_message = print_settings.get("print.message") or ""
        request.state.print_show_table_borders = print_settings.get("print.show_table_borders") or "true"
        request.state.print_show_lines = print_settings.get("print.show_lines") or "true"
        request.state.print_thermal_width = print_settings.get("print.thermal_width") or "80"
        system_settings = service.get_group("system")
        request.state.system_audit_enabled = system_settings.get("system.audit_enabled") or "true"
    except Exception:
        request.state.app_name = settings.app_name
        request.state.app_title = settings.app_name
        request.state.app_theme = "system"
        request.state.app_density = "comfortable"
        request.state.app_primary_color = "#176b67"
        request.state.clinic_name = ""
        request.state.clinic_logo = ""
        request.state.clinic_address = ""
        request.state.clinic_phone = ""
        request.state.clinic_email = ""
        request.state.clinic_header_text = ""
        request.state.clinic_footer_text = ""
        request.state.datetime_calendar = "jalali"
        request.state.datetime_timezone = "Asia/Tehran"
        request.state.datetime_date_format = "YYYY/MM/DD"
        request.state.datetime_time_format = "24"
        request.state.datetime_show_seconds = "false"
        request.state.current_datetime = format_current_datetime()
        request.state.reports_default_format = "html"
        request.state.reports_include_timestamp = "true"
        request.state.messaging_enabled = "false"
        request.state.messaging_default_provider = "sms"
        request.state.contacts_enabled = "true"
        request.state.contacts_require_phone = "false"
        request.state.print_paper_size = "A4"
        request.state.print_margin_top = "10"
        request.state.print_margin_right = "10"
        request.state.print_margin_bottom = "10"
        request.state.print_margin_left = "10"
        request.state.print_show_logo = "true"
        request.state.print_show_header = "true"
        request.state.print_show_footer = "true"
        request.state.print_title = ""
        request.state.print_message = ""
        request.state.print_show_table_borders = "true"
        request.state.print_show_lines = "true"
        request.state.print_thermal_width = "80"
        request.state.system_audit_enabled = "true"
    try:
        yield db
    finally:
        db.close()
