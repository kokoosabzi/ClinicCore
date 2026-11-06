"""Shared pytest fixtures for isolated database-backed tests.

All HTTP integration tests use a throwaway in-memory SQLite database. The
fixture creates the complete ORM schema for fast test isolation; the Alembic
migration chain is verified separately by the file-backed SQLite migration
test and the Windows CI migration step.

The application database dependency is overridden for each test client.
The audit middleware currently imports SessionLocal directly, so that
reference is monkeypatched as well to keep all test writes inside the same
isolated SQLite database. No developer or user database is touched.
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
    """A single session for repository/service tests."""
    session = db_session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session_factory, monkeypatch) -> Generator[TestClient, None, None]:
    """A FastAPI TestClient wired entirely to the isolated test database."""

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
