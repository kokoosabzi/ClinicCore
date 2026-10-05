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

        app_settings = SettingsService(db).get_group("app")
        request.state.app_name = app_settings.get("app.name") or settings.app_name
        request.state.app_title = app_settings.get("app.title") or settings.app_name
        request.state.app_theme = app_settings.get("app.theme") or "system"
        request.state.app_density = app_settings.get("app.density") or "comfortable"
    except Exception:
        request.state.app_name = settings.app_name
        request.state.app_title = settings.app_name
        request.state.app_theme = "system"
        request.state.app_density = "comfortable"
    try:
        yield db
    finally:
        db.close()
