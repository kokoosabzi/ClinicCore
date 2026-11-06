# ClinicCore — Development Changelog (Redesign Phase)

## 2026-11-06 — Dynamic UI themes and appearance controls

- Branch: `development`, based directly on `main` after PR #14 and PR #15 were merged.
- Added four semantic visual presets: Clinical Light, Modern Dark, Soft Neutral, and High Contrast.
- Added validated `app.style` and `app.font_scale` settings; existing theme mode, primary color, and density controls remain available.
- Added live preview behavior on the administrator settings page without saving changes until the form is submitted.
- Added isolated theme stylesheet and lightweight preview controller; no CSS framework or new runtime dependency was introduced.
- Kept print views on a paper-safe light palette independent of the selected application preset.
- Added tests for persistence and invalid appearance preset rejection, plus acceptance criteria and settings documentation.
- Verification: Windows CI run #102 passed on the source branch; consolidated-branch CI and manual Windows/browser acceptance remain pending. This work is not marked complete.
- Scope note: appearance remains an administrator-managed system default; per-user theme overrides are not implemented in this change.

---

## 2026-11-06 — Sprint 1: User Administration & RBAC implementation

- Branch: `feature/user-management-rbac`; dependent on Sprint 0 PR #14.
- Added normalized `roles`, `permissions`, and `role_permissions` tables through Alembic revision `20261106_0006`. Existing user rows and password hashes are not rewritten.
- Added built-in roles: admin, clinic_manager, doctor, secretary, accountant; seeded initial permission grants.
- Added database-backed route authorization and current-principal/permission refresh on every request.
- Added user lifecycle operations and Persian RTL user-management page: create, edit, deactivate/reactivate and one-time temporary password reset.
- Added administrator-only role-permission matrix. Admin permissions are immutable; clinic managers cannot manage system-admin accounts; last active admin cannot be deactivated or demoted.
- Enforced module permissions across patient, appointment, financial, messaging, settings and user routes. Restricted dashboard and patient-chart financial/clinical details according to effective permissions.
- Added CSRF protection to login/logout/password-change and user/role management forms; successful login clears and rotates the session.
- Added RBAC route tests, role matrix tests, least-privilege visibility tests and a populated SQLite migration test proving existing password hashes remain unchanged.
- CI diagnosis and fixes:
  - Early run exposed middleware ordering: the request-settings middleware accessed session before SessionMiddleware. Reordered middleware so SessionMiddleware is outermost.
  - Updated legacy tests to authenticate through the actual login flow and seeded role catalog instead of overriding the old require_user dependency.
- Successful verification: Windows CI run #93 on Windows Server 2025 / Python 3.12.10.
  - Dependency installation: passed.
  - `python -m compileall app tests main.py alembic scripts`: passed.
  - `python -m pytest -q`: **40 passed, 0 failed** (81 warnings).
  - `python -m alembic upgrade head`: passed on a clean SQLite database through `20261106_0006`.
  - Populated-database migration regression: passed; pre-existing username, role and exact password-hash string preserved.
- Remaining: manual Windows UI acceptance and code review. PR #15 remains Draft and is stacked on PR #14. No merge to main.

---

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
  - 81 dependency/deprecation warnings were emitted; they did not fail the run and are recorded for a later maintenance pass.
- Remaining verification: no manual acceptance test has yet been performed on the user's Windows PC.
- Safety: no merge to `main`, no database deletion, and no user data changes.

---
