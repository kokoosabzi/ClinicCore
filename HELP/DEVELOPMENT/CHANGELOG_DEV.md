# ClinicCore — Development Changelog (Redesign Phase)

## 2026-11-06 — Sprint 0: Windows CI diagnosis and remediation

- Phase/Task: Sprint 0 / Windows readiness and CI hardening
- Branch: `stabilization/windows-sqlite-runtime`
- CI evidence: Windows workflow run #8 completed on Windows Server 2025 / Python 3.12.10. Compileall passed; pytest reported 24 passed and 5 failed; the Alembic step was skipped because pytest failed.
- Root causes found in the run logs:
  - Windows had no IANA timezone database available to Python `zoneinfo`; tests using `Asia/Tehran` failed, and settings submissions returned validation errors.
  - `tests/test_app.py` used a bare TestClient and bypassed the shared isolated SQLite test fixture; the homepage request therefore had no `system_settings` table.
- Remediation committed:
  - Added `tzdata>=2024.1` as an application runtime dependency for Windows timezone support.
  - Changed the application smoke tests to use the shared fixture, which overrides the database and audit session with isolated SQLite.
  - Rewrote obsolete PostgreSQL-specific fixture documentation.
  - Removed `Base.metadata.create_all` from `scripts/seed_admin.py`; Alembic is now the only schema creation/migration path, and the seed script is limited to creating the initial admin record after migration.
- Verification after remediation: pending. No successful run against the updated branch head is yet visible. No manual Windows installation/runtime test has been performed.
- Safety: no merge to `main`, no database deletion, and no user data changes.

---

## 2026-11-06 — Sprint 0: Windows and SQLite runtime stabilization

- Phase/Task: Sprint 0 / Windows readiness
- Commit: implementation/documentation commit series on `stabilization/windows-sqlite-runtime`
- Summary: Aligned installation and runtime documentation with the existing SQLite-only implementation. Added secure first-install credential bootstrap and dedicated setup/start/stop scripts. Updated progress and Windows acceptance criteria.
- Follow-up review: Added Windows GitHub Actions checks; fixed a PowerShell `$PID` reserved-variable collision in the stop script and made PID cleanup conditional on verified process exit.
- Verification: The first CI run was not successful; see the remediation entry above. No local Python test suite, Alembic command, or Windows manual test was run in the development environment.

---
