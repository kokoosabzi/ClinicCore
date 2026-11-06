# ClinicCore — Development Changelog (Redesign Phase)

## 2026-11-06 — Sprint 0: Windows CI diagnosis, remediation and successful verification

- Phase/Task: Sprint 0 / Windows readiness and CI hardening
- Branch: `stabilization/windows-sqlite-runtime`
- Initial CI evidence: workflow run #8 on Windows Server 2025 / Python 3.12.10. Compileall passed; pytest reported 24 passed and 5 failed; the Alembic step was skipped because pytest failed.
- Root causes found in the run logs:
  - Windows had no IANA timezone database available to Python `zoneinfo`; tests using `Asia/Tehran` failed, and settings submissions returned validation errors.
  - `tests/test_app.py` used a bare TestClient and bypassed the shared isolated SQLite test fixture; the homepage request therefore had no `system_settings` table.
- Remediation committed:
  - Added `tzdata>=2024.1` as an application runtime dependency for Windows timezone support.
  - Changed the application smoke tests to use the shared fixture, which overrides the database and audit session with isolated SQLite.
  - Rewrote obsolete PostgreSQL-specific fixture documentation.
  - Removed `Base.metadata.create_all` from `scripts/seed_admin.py`; Alembic is now the only schema creation/migration path, and the seed script is limited to creating the initial admin record after migration.
- Successful verification: workflow run #23 on Windows Server 2025 / Python 3.12.10 completed successfully.
  - Dependency installation: passed.
  - `python -m compileall app tests main.py alembic scripts`: passed.
  - `python -m pytest -q`: **29 passed, 0 failed**.
  - `python -m alembic upgrade head`: passed on a clean SQLite database through `20261005_0005`.
  - 81 dependency/deprecation warnings were emitted; they did not fail the run and are recorded for later maintenance.
- Remaining verification: no manual acceptance test has yet been performed on the user's Windows PC. `setup.bat`, `start.bat`, login/password change, application workflows, persistence and `stop.bat` remain release gates.
- Safety: no merge to `main`, no database deletion, and no user data changes.

---

## 2026-11-06 — Sprint 0: Windows and SQLite runtime stabilization

- Phase/Task: Sprint 0 / Windows readiness
- Commit: implementation/documentation commit series on `stabilization/windows-sqlite-runtime`
- Summary: Aligned installation and runtime documentation with the existing SQLite-only implementation. Added secure first-install credential bootstrap and dedicated setup/start/stop scripts. Updated progress and Windows acceptance criteria.
- Follow-up review: Added Windows GitHub Actions checks; fixed a PowerShell `$PID` reserved-variable collision in the stop script and made PID cleanup conditional on verified process exit.
- Verification: See the diagnosis/remediation entry above. The hosted Windows CI passed after fixes; manual Windows acceptance remains pending.

---
