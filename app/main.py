from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core import audit as audit_module
from app.core.audit import audit_request_middleware
from app.core.database import get_db
from app.core.auth import current_user
from app.services.settings_service import SettingsService
from app.routers import appointments, auth, financial, health, messaging, pages, patients, users


templates = Jinja2Templates(directory="app/templates")



async def load_app_settings(request: Request, call_next):
    # Load persisted branding and UI settings for every page request.
    if request.url.path.startswith(("/static/", "/health")):
        return await call_next(request)

    db = audit_module.SessionLocal()
    try:
        service = SettingsService(db)
        keys = {}
        for category in ("app", "clinic", "datetime", "reports", "messaging", "contacts", "print", "system"):
            keys.update(service.get_group(category))

        state_mapping = {
            "app_name": "app.name",
            "app_title": "app.title",
            "app_theme": "app.theme",
            "app_density": "app.density",
            "app_primary_color": "app.primary_color",
            "clinic_name": "clinic.name",
            "clinic_logo": "clinic.logo",
            "clinic_address": "clinic.address",
            "clinic_phone": "clinic.phone",
            "clinic_email": "clinic.email",
            "clinic_header_text": "clinic.header_text",
            "clinic_footer_text": "clinic.footer_text",
            "datetime_calendar": "datetime.calendar",
            "datetime_timezone": "datetime.timezone",
            "datetime_date_format": "datetime.date_format",
            "datetime_time_format": "datetime.time_format",
            "datetime_show_seconds": "datetime.show_seconds",
            "reports_default_format": "reports.default_format",
            "reports_include_timestamp": "reports.include_timestamp",
            "messaging_enabled": "messaging.enabled",
            "messaging_default_provider": "messaging.default_provider",
            "contacts_enabled": "contacts.enabled",
            "contacts_require_phone": "contacts.require_phone",
            "print_paper_size": "print.paper_size",
            "print_margin_top": "print.margin_top",
            "print_margin_right": "print.margin_right",
            "print_margin_bottom": "print.margin_bottom",
            "print_margin_left": "print.margin_left",
            "print_show_logo": "print.show_logo",
            "print_show_header": "print.show_header",
            "print_show_footer": "print.show_footer",
            "print_title": "print.title",
            "print_message": "print.message",
            "print_show_table_borders": "print.show_table_borders",
            "print_show_lines": "print.show_lines",
            "print_thermal_width": "print.thermal_width",
            "system_audit_enabled": "system.audit_enabled",
        }
        for attribute, key in state_mapping.items():
            setattr(request.state, attribute, keys.get(key))
    finally:
        db.close()

    return await call_next(request)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, same_site="lax", https_only=False)
    app.middleware("http")(audit_request_middleware)
    app.middleware("http")(load_app_settings)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(patients.router)
    app.include_router(appointments.router)
    app.include_router(financial.router)
    app.include_router(messaging.router)
    app.include_router(users.router)
    app.include_router(pages.router)

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request, db=__import__("fastapi").Depends(get_db)):
        app_name = getattr(request.state, "app_name", settings.app_name)
        app_title = getattr(request.state, "app_title", settings.app_name)
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={
                "request": request,
                "app_name": app_name,
                "app_title": app_title,
                "app_primary_color": getattr(request.state, "app_primary_color", "#176b67"),
                "clinic_logo": getattr(request.state, "clinic_logo", ""),
                "user": current_user(request),
            },
        )

    return app


app = create_app()
