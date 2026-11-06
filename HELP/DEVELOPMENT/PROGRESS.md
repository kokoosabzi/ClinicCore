# ClinicCore — Development Progress

> این فایل مرجع وضعیت واقعی مخزن است. تستی که اجرا نشده نباید Pass علامت بخورد.

Last updated: 2026-11-06
Last updated by: ChatGPT — repository stabilization review
Repository baseline inspected: `main` at `4c7d5e7c31accfca670283e2460a81a97860686a`
Working branch: `stabilization/windows-sqlite-runtime`

## 1. Current project phase

**Phase 0 — Stabilization & Windows Readiness**

## 2. Current task

**Task:** Align Windows installation/runtime and project documentation with the existing SQLite-only implementation.

**Status:** IN_PROGRESS until automated tests and Windows runtime checks are available.

## 3. Existing implementation confirmed by source inspection

- FastAPI + SQLAlchemy 2 + Alembic + Jinja2 application.
- SQLite is the only accepted database URL in `app/core/config.py`.
- Default file-backed database path is `data/cliniccore.db`; the database module creates its parent directory.
- Alembic head migration is `20261005_0005`; a file-backed SQLite migration test exists in `tests/test_sqlite_migrations.py`.
- Current user roles: admin, doctor, secretary, accountant.
- Passwords are hashed; seeded initial admin is marked `must_change_password`.
- Settings, Jalali date/time formatting, appointment booking, print views and patient/financial modules exist in the repository.
- Most application tests use in-memory SQLite; file-backed migration verification is a separate test.

## 4. Work in this branch

- Inspected the mainline implementation and identified stale PostgreSQL/Docker instructions.
- Updated the primary README, agent rules, installation/run/authentication guides and master plan for SQLite-only Windows delivery.
- Added a Windows bootstrap path to generate local credentials for a fresh installation without overwriting an existing `.env`.
- Added setup/start/stop launch scripts using the project-local `.venv` and PID-verified process shutdown.
- Updated Git ignore rules for runtime PID files.
- Updated this progress record and development changelog.

## 5. Not yet verified

- No Windows runtime is available in this execution environment; setup/start/stop, browser login and shutdown have not been manually executed.
- No fresh `pytest`, `compileall` or clean-database Alembic run has been executed in this turn.
- Existing tests and migrations were inspected but not run.
- Existing user accounts and existing `.env` values were not changed.

## 6. Current blockers / risks

- `get_db` catches broad exceptions while loading settings and falls back silently; review separately.
- `scripts/seed_admin.py` calls `Base.metadata.create_all` in addition to Alembic; review separately before release.
- Fine-grained permissions and full user CRUD are not yet complete.
- Active appointment uniqueness is global per `starts_at`; adding doctor/room scheduling requires a scoped migration and decision record.

## 7. Last successful verification

No new automated or manual verification was run in this turn. Repository inspection is not a passing test result.

## 8. Exact next action

Run on a clean Windows clone:
```powershell
python -m compileall app tests main.py alembic scripts
python -m pytest -q
python -m alembic upgrade head
```
Then test `setup.bat`, generated administrator login and mandatory password change, dashboard, patient/appointment pages, persistence after restart, `stop.bat`, and confirm unrelated Python processes remain running.

Only after these checks pass should Phase 0 be marked complete. Next product task: Phase 1 — User Administration & Access Control.
