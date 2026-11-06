# ClinicCore — Development Progress

> این فایل مرجع وضعیت واقعی مخزن است. تستی که اجرا نشده نباید Pass علامت بخورد.

Last updated: 2026-11-06
Last updated by: ChatGPT — Windows CI diagnosis, remediation and verification
Repository baseline inspected: `main` at `4c7d5e7c31accfca670283e2460a81a97860686a`
Working branch: `stabilization/windows-sqlite-runtime`

## 1. Current project phase

**Sprint 0 — Project Stabilization & Windows Readiness**

## 2. Current task

**Task:** Align Windows installation/runtime and project documentation with the existing SQLite-only implementation.

**Status:** AUTOMATED CHECKS PASSED; MANUAL WINDOWS ACCEPTANCE PENDING. Keep PR #14 in Draft until the local Windows setup/start/stop and browser acceptance checklist is completed.

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
- First Windows CI run #8 exposed two issues: missing IANA timezone data and a homepage smoke test that bypassed the isolated SQLite fixture.
- Added `tzdata` as a runtime dependency so Windows installations can resolve configured IANA zones such as `Asia/Tehran`.
- Updated `tests/test_app.py` to use the shared `client` fixture and its isolated in-memory SQLite database.
- Rewrote stale PostgreSQL references in `tests/conftest.py` to describe the actual isolated SQLite test setup.
- Removed `Base.metadata.create_all` from `scripts/seed_admin.py`; Alembic is the single schema creation/migration source of truth, while the seed script only creates the initial administrator record.
- Updated the PR description, progress record and development changelog with the real CI failure, fixes and successful rerun.

## 5. Not yet verified

- No real Windows desktop/local-clone acceptance has been performed by the user: `setup.bat`, `start.bat`, browser login, mandatory password change, persistence, and `stop.bat` remain to be tested on the target PC.
- No existing user accounts or existing `.env` values were changed.
- The successful CI run validates the updated source in a hosted Windows runner; it does not replace testing the user's actual PC, installed Python environment, browser, firewall/port availability, and filesystem permissions.

## 6. Current blockers / risks

- Manual Windows acceptance is the only Sprint 0 release gate still outstanding.
- `get_db` catches broad exceptions while loading settings and falls back silently; review separately.
- Fine-grained permissions and full user CRUD are not yet complete; they belong to the next product phase.
- Active appointment uniqueness is global per `starts_at`; adding doctor/room scheduling requires a scoped migration and decision record.
- CI emitted 81 warnings (primarily dependency deprecations); they did not fail the run and should be reviewed in a maintenance pass.

## 7. Verification evidence

- Workflow run #8: Windows Server 2025 / Python 3.12.10; compileall passed; pytest 24 passed / 5 failed; migration step skipped. This run exposed the issues listed above.
- Workflow run #23 on the remediated branch: **success**.
- `python -m pip install -e ".[dev]"`: passed.
- `python -m compileall app tests main.py alembic scripts`: passed.
- `python -m pytest -q`: **29 passed, 0 failed** (81 warnings).
- `python -m alembic upgrade head`: passed on a fresh CI SQLite database through revision `20261005_0005`.
- Manual Windows acceptance on the user's computer: pending.

## 8. Exact next action

On the target Windows PC, clone/sync branch `stabilization/windows-sqlite-runtime` and run:

```powershell
setup.bat
start.bat
```

Then verify `http://127.0.0.1:8000/health`, log in with the generated initial administrator credentials, complete the mandatory password change, inspect dashboard/patient/appointment/settings/print pages, create a test patient and appointment, stop and restart the app, and confirm the records persist. Run `stop.bat` and verify unrelated Python/Uvicorn processes remain running.

Do not delete the `data` folder or overwrite an existing `.env`. Record any failure text and the Windows/Python versions. Only after this acceptance passes should PR #14 be marked ready for review and Sprint 0 be considered complete. No merge to `main` is requested yet.
