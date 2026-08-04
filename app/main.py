from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.audit import audit_request_middleware
from app.routers import appointments, auth, financial, health, messaging, pages, patients, users


templates = Jinja2Templates(directory="app/templates")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, same_site="lax", https_only=False)
    app.middleware("http")(audit_request_middleware)
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
    def home(request: Request):
        return templates.TemplateResponse("home.html", {"request": request, "app_name": settings.app_name})

    return app


app = create_app()
