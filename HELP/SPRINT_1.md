# Sprint 1 - Project Foundation

## Goal
Create the maintainable ClinicCore foundation with FastAPI, SQLAlchemy 2, Alembic, Persian-first UI shell, core patient and appointment modules, tests, and documentation.

## Tasks
- Build application package structure under `app/`.
- Add configuration, database session, models, schemas, repositories, services, and routers.
- Add initial Alembic migration for patients and appointments.
- Add Persian RTL home template and static CSS.
- Add initial health and UI tests.
- Update HELP documentation.

## Files affected
- `app/`
- `alembic/`
- `tests/`
- `HELP/`
- `README.md`
- `pyproject.toml`
- `main.py`

## Database changes
- Add `patients` table.
- Add `appointments` table.
- Add timestamp and soft-delete fields.

## Risks
- PostgreSQL must be available before running migrations.
- Future auth and permission design must stay simple and role-based.

## Test plan
- Run `pytest`.
- Run Alembic checks when PostgreSQL is configured.
