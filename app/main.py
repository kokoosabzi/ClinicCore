from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.audit import audit_request_middleware
from app.core.database import get_db
from app.core.auth import current_user
from app.core.database import SessionLocal
from app.routers import appointments, auth, financial, health, messaging, pages, patients, users
from sqlalchemy import select


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
                "user": current_user(request),
            },
        )

    return app


app = create_app()
