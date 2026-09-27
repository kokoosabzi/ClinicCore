"""Shared pytest fixtures for database-backed tests.

Phase A1 (see HELP/DEVELOPMENT/PROGRESS.md): provides an isolated,
throwaway database for tests so that CRUD/auth-flow tests can be
written in later phases without touching the real PostgreSQL
development database.

Design notes (read before extending):

- Uses an in-memory SQLite database created via ``Base.metadata.create_all``.
  This intentionally bypasses Alembic migrations. Verifying the Alembic
  migration chain itself against SQLite is a separate, later concern
  (Gap Analysis Phase H / "Local Database"), not part of this fixture.
- The engine/session are created fresh, are not related to the
  application's module-level ``app.core.database.engine`` /
  ``SessionLocal`` (which stay bound to the real PostgreSQL URL from
  ``app.core.config.settings`` and are left untouched), and are torn
  down after each test.
- Two integration points exist for redirecting the app to the test
  database:
    1. ``app.core.database.get_db`` — a FastAPI dependency, used by
       every router via ``Depends(get_db)``. Overridden per-test via
       ``app.dependency_overrides``.
    2. ``app.core.audit.audit_request_middleware`` — imports
       ``SessionLocal`` directly (``from app.core.database import
       SessionLocal``) instead of using the ``get_db`` dependency, so
       it does not pick up a ``get_db`` override. It is monkeypatched
       separately in the ``client`` fixture below so audit writes land
       in the same test database rather than attempting a real
       PostgreSQL connection. This split exists in the application
       today; changing the middleware to use dependency injection
       instead is an application-code change outside Phase A1's scope
       and is not done here.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.core.audit as audit_module
import app.models  # noqa: F401  (registers all model tables on Base.metadata)
from app.core.database import Base, get_db
from app.main import create_app


@pytest.fixture()
def db_engine():
    """A fresh in-memory SQLite engine with the full schema created."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def db_session_factory(db_engine):
    """A sessionmaker bound to the per-test SQLite engine."""
    return sessionmaker(bind=db_engine, autoflush=False, autocommit=False, expire_on_commit=False)


@pytest.fixture()
def db_session(db_session_factory) -> Generator[Session, None, None]:
    """A single SQLAlchemy session for tests that talk to repositories/
    services directly, without going through the HTTP layer."""
    session = db_session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session_factory, monkeypatch) -> Generator[TestClient, None, None]:
    """A FastAPI TestClient wired to the isolated test database.

    Overrides the ``get_db`` dependency for every router, and
    monkeypatches the audit middleware's directly-imported
    ``SessionLocal`` (see module docstring) so a request made through
    this client never touches the real PostgreSQL database configured
    in ``app.core.config.settings``.
    """

    def override_get_db() -> Generator[Session, None, None]:
        session = db_session_factory()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(audit_module, "SessionLocal", db_session_factory)

    test_app = create_app()
    test_app.dependency_overrides[get_db] = override_get_db
    with TestClient(test_app) as test_client:
        yield test_client
    test_app.dependency_overrides.clear()
