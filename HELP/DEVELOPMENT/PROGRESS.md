# ClinicCore — Development Progress

> این فایل مرجع وضعیت واقعی مخزن است. تستی که اجرا نشده نباید Pass علامت بخورد.

Last updated: 2026-11-06
Last updated by: ChatGPT — Windows CI failure analysis and remediation
Repository baseline inspected: `main` at `4c7d5e7c31accfca670283e2460a81a97860686a`
Working branch: `stabilization/windows-sqlite-runtime`
Current branch head: `0ba8226a125e81d9600e7a0d812cb0b2adbc1850`

## 1. Current project phase

**Sprint 0 — Project Stabilization & Windows Readiness**

## 2. Current task

**Task:** Align Windows installation/runtime and project documentation with the existing SQLite-only implementation.

**Status:** IN_PROGRESS. The first Windows CI run exposed test/dependency gaps. Fixes have been committed, but a run against the updated head is still pending; manual Windows acceptance is also pending.

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
- Added a Windows GitHub Actions workflow for compileall, pytest, and a clean SQLite Alembic migration.
- Corrected a PowerShell shutdown bug: the local PID variable no longer conflicts with PowerShell's reserved `$PID`; shutdown now verifies process exit before deleting the PID file.
- First Windows CI run #8 completed: compileall passed; pytest reported **24 passed, 5 failed**. The migration step was skipped because pytest failed.
- CI failure analysis identified two root causes: Windows lacked the IANA timezone database package (`tzdata`), and `tests/test_app.py` bypassed the shared isolated-SQLite fixture for the homepage request.
- Added `tzdata` as a runtime dependency so Windows installations can resolve configured IANA zones such as `Asia/Tehran`.
- Updated `tests/test_app.py` to use the shared `client` fixture and its isolated in-memory SQLite database.
- Rewrote stale PostgreSQL references in `tests/conftest.py` to describe the actual isolated SQLite test setup.
- Removed `Base.metadata.create_all` from `scripts/seed_admin.py`; the setup flow now relies on the already-run Alembic migrations as the single schema source of truth, while the seed script only creates the administrator record.
- Updated this progress record and development changelog with the observed CI result and remediation.

## 5. Not yet verified

- The remediation commits are on the branch, but no workflow run against the new head is visible yet.
- The prior CI run's compileall step passed; its pytest step failed (24 passed, 5 failed); its Alembic migration step was skipped.
- No fresh pytest run, clean-database Alembic run, or local PowerShell execution has been performed after the fixes.
- No real Windows runtime is available in this execution environment; setup/start/stop, browser login and shutdown have not been manually executed.
- Existing user accounts and existing `.env` values were not changed.

## 6. Current blockers / risks

- Updated-head CI verification remains outstanding.
- `get_db` catches broad exceptions while loading settings and falls back silently; review separately.
- The seed script no longer creates ORM tables; Alembic is the schema source of truth. This change is awaiting updated-head CI verification.
- Fine-grained permissions and full user CRUD are not yet complete.
- Active appointment uniqueness is global per `starts_at`; adding doctor/room scheduling requires a scoped migration and decision record.

## 7. Verification evidence

- Workflow run #8: Windows Server 2025, Python 3.12.10.
- `python -m compileall app tests main.py alembic scripts`: passed.
- `python -m pytest -q`: failed — 24 passed, 5 failed.
- Failure groups: missing `tzdata` for IANA zones (3 affected tests including two settings submissions), and homepage test bypassing the database fixture (1 affected test).
- Alembic migration step: skipped due to earlier pytest failure.
- Updated-head workflow result: not yet available.
- Manual Windows acceptance: not run.

## 8. Exact next action

Obtain a fresh Windows CI run for current branch head `0ba8226a125e81d9600e7a0d812cb0b2adbc1850`. Confirm pytest, then confirm the clean SQLite Alembic migration. If GitHub does not automatically schedule a run, trigger/re-enable it through repository Actions or an authorized workflow dispatch.

After CI passes, run on a clean Windows clone:
```powershell
python -m compileall app tests main.py alembic scripts
python -m pytest -q
python -m alembic upgrade head
```
Then test `setup.bat`, generated administrator login and mandatory password change, dashboard, patient/appointment pages, persistence after restart, `stop.bat`, and confirm unrelated Python processes remain running.

Only after automated checks and manual Windows acceptance pass should Sprint 0 be marked complete. Next product task: Phase 1 — User Administration & Access Control.
