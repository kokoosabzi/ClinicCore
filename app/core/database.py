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

        request.state.app_name = SettingsService(db).get("app.name", settings.app_name)
        request.state.app_title = SettingsService(db).get("app.title", settings.app_name)
    except Exception:
        request.state.app_name = settings.app_name
        request.state.app_title = settings.app_name
    try:
        yield db
    finally:
        db.close()
