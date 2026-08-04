# Sprint 3 - Authentication, System Logs, Print Forms, and Runbook

## Goal
Complete the operational shell with printable clinic forms, explicit database table documentation, system request logging, login/logout, initial admin seeding, and implementation/run instructions.

## Tasks
- Add session-based login/logout pages and router.
- Add system HTTP audit middleware using `audit_logs`.
- Add initial admin seed script with default `admin` / `admin` credentials.
- Add printable patient, appointment, and payment templates.
- Add implementation, authentication, printing, and table-structure documentation.

## Files affected
- `app/core/`
- `app/routers/`
- `app/services/`
- `app/templates/`
- `app/static/`
- `scripts/`
- `HELP/`

## Database changes
No schema migration is required; this sprint uses the existing `users` and `audit_logs` tables.

## Risks
- Default `admin` / `admin` is for first local setup only and must be changed in production.
- Audit middleware intentionally ignores database logging errors so user requests are not blocked by logging failure.

## Test plan
- Compile all Python files.
- Run pytest after dependencies are installed.
- Run `alembic upgrade head`, then `python scripts/seed_admin.py`, then login at `/login`.
