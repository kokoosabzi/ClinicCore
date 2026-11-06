# AGENTS.md — ClinicCore Development Rules

## Project identity

ClinicCore is a lightweight, Persian-first clinic management application for small medical offices and healthcare centers. It is not a hospital information system or an enterprise accounting ERP.

## Agent role

Act as the lead architect and senior Python engineer. Inspect the current code and tests before changing behavior. Prefer the smallest maintainable solution; avoid broad refactors and unnecessary dependencies.

## Technology and supported runtime

- Python 3.12+
- FastAPI, SQLAlchemy 2, Alembic
- SQLite file-backed database for the current supported runtime
- Jinja2, HTMX, Alpine.js
- Windows local installation is the delivery target for this phase
- Persian UI, RTL layout, Jalali date input/display

Do not describe PostgreSQL or Docker as prerequisites for the current supported installation. Do not remove or alter any external PostgreSQL database or Docker volume as part of ClinicCore work.

## Architecture

Preserve the existing layering:

`Router -> Service -> Repository -> Model/DB`

- Routers handle HTTP concerns, not core business rules.
- Services own domain behavior.
- Repositories own persistence queries.
- Templates contain presentation logic only.
- Database schema changes require Alembic migrations.
- Reuse existing services and shared UI tokens before introducing abstractions.

## Product principles

- Keep financial features as clinic record-keeping, not a full accounting ERP.
- Preserve authentication, CSRF, password hashing, audit logging, and role checks.
- Current roles: admin, doctor, secretary, accountant. Do not assume fine-grained permissions exist until implemented and tested.
- Keep core modules generic; specialty-specific features may be added as plugins when justified.
- All user-facing pages must preserve Persian language and RTL behavior.

## Development workflow

Before work:
1. Read `HELP/CONTINUE_DEVELOPMENT.txt`.
2. Read `HELP/DEVELOPMENT/PROGRESS.md`, `DECISIONS.md`, and the relevant specifications.
3. Inspect `git status`, branch, recent commits, migrations, and tests.
4. Stop if unrelated working-tree changes or a data-loss/security risk is found.

For each task:
1. Define one coherent scope.
2. Inspect the complete affected implementation.
3. Implement the smallest safe change.
4. Run relevant tests and compile checks.
5. Update progress and changelog with what was actually verified.
6. Review the diff and commit only the intended changes.

Never claim a test or manual check passed unless it was run and observed in the current environment. Never commit secrets, real credentials, database files, or runtime uploads.

## Windows delivery

The supported local workflow is:
- `setup.bat` — one-time environment/dependency/database setup.
- `start.bat` — start the local server.
- `stop.bat` — stop only the server instance recorded by ClinicCore's launcher.

Use the project-local `.venv`. Do not kill unrelated Python processes. Keep runtime data under `data/` and exclude it from Git.
