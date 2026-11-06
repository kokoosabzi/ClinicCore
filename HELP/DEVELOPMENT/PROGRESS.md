# ClinicCore — Development Progress

> این فایل وضعیت واقعی مخزن و شواهد تست را ثبت می‌کند. هیچ تست اجرا‌نشده‌ای نباید Pass علامت بخورد.

Last updated: 2026-11-06
Last updated by: ChatGPT — Sprint 1 user administration and RBAC implementation
Repository baseline: `main` at `4c7d5e7c31accfca670283e2460a81a97860686a`
Sprint 0 branch: `stabilization/windows-sqlite-runtime`
Sprint 1 branch: `feature/user-management-rbac`
Sprint 1 head at last verified run: `25b881b6f8c672812cbe4ff7206cbb2287eac279`

## 1. Current delivery status

- **Sprint 0 — Windows & SQLite readiness:** hosted Windows CI passed; manual installation/runtime acceptance on the target PC is still pending. PR #14 remains Draft.
- **Sprint 1 — User Administration & RBAC:** implementation is present on the dependent feature branch; hosted Windows CI run #93 passed. UI acceptance on the target PC and review are still pending. PR #15 remains Draft and targets the Sprint 0 branch.
- Neither PR has been merged. `main` remains unchanged.

## 2. Existing application baseline

- FastAPI + SQLAlchemy 2 + Alembic + Jinja2, Persian RTL UI.
- Windows local deployment uses file-backed SQLite at `data/cliniccore.db`.
- Alembic remains the only schema creation/migration mechanism.
- Existing modules include patients, appointments, financial records, messaging, settings and print views.
- Existing roles were admin, doctor, secretary and accountant; Sprint 1 adds clinic_manager without rewriting existing user rows.

## 3. Sprint 0 — completed implementation, manual acceptance pending

- Aligned documentation and local runtime with SQLite-only Windows delivery.
- Added `setup.bat`, bootstrap of a private local `.env`, and start/stop scripts with PID/process identity checks.
- Existing `.env` is not overwritten; no application database is deleted or reset.
- Added Windows CI and fixed the PowerShell reserved-variable collision involving `$PID`.
- Fixed missing Windows IANA timezone data by adding `tzdata`.
- Corrected the homepage smoke test to use the isolated SQLite fixture.
- Removed `Base.metadata.create_all` from the admin seed script so Alembic is the single schema source of truth.

## 4. Sprint 1 — implementation completed on the feature branch

- Added `Role`, `Permission`, and `RolePermission` models.
- Added Alembic revision `20261106_0006` with five built-in roles and the initial permission matrix.
- Added the clinic manager role while retaining legacy role keys and existing user/password data.
- Added database-backed `require_permission` checks and refreshed effective user/permission state on every request.
- Enforced permissions across patient, appointment, financial, messaging, settings and user routes.
- Restricted dashboard totals and patient-chart sections according to effective permissions. Accountants do not receive clinical chart access by default; doctors/receptionists do not receive financial access by default.
- Added Persian RTL user administration: list, create, update, deactivate/reactivate and one-time temporary password reset.
- Added administrator-only role permission matrix for built-in non-admin roles; admin permissions are immutable.
- Added protection against deactivating/demoting the last active administrator and against clinic managers modifying system-administrator accounts.
- Added CSRF validation to login, logout, password-change, user-management and role-permission browser forms; successful login rotates the session.
- Added RBAC integration tests and a migration regression test proving existing usernames, roles and password-hash values remain unchanged when upgrading a populated 0005 database.

## 5. Verification evidence

### Sprint 0
- Windows CI run #23 on Windows Server 2025 / Python 3.12.10: compileall passed; pytest 29 passed / 0 failed; clean SQLite Alembic migration passed through `20261005_0005`.
- Manual Windows acceptance on the user's PC: **not run**.

### Sprint 1
- Windows CI run #93 on Windows Server 2025 / Python 3.12.10: **success**.
- Dependency installation: passed.
- `python -m compileall app tests main.py alembic scripts`: passed.
- `python -m pytest -q`: **40 passed, 0 failed** (81 dependency/deprecation warnings).
- `python -m alembic upgrade head`: passed on a clean SQLite database through `20261106_0006`.
- Dedicated populated-database upgrade regression: passed; the existing user's username, role and exact password-hash string were preserved while the five role rows and administrator grants were added.
- Run: https://github.com/kokoosabzi/ClinicCore/actions/runs/42190638528

## 6. Remaining work / release gates

- On the target Windows PC, complete Sprint 0 setup/start/stop and persistence acceptance from AT-1101 through AT-1105.
- After PR #14 is accepted and merged, update the Sprint 1 branch base as needed; do not merge PR #15 ahead of PR #14.
- On Windows, manually inspect the user-management page, role-permission matrix, CSRF-protected forms, forced password change, role-specific navigation, and permission-denied behavior.
- Review the 81 dependency/deprecation warnings separately; they did not fail CI.
- Review existing appointment global-slot uniqueness before adding practitioner/room scheduling.
- Fine-grained record ownership (e.g. doctor sees only assigned patients) is not implemented in this sprint; current permissions are module/action level.

## 7. Next action

1. User performs the Sprint 0 Windows installation/runtime checklist without deleting `.env` or `data`.
2. Review and merge PR #14 only after acceptance.
3. Rebase/update PR #15 on the accepted Sprint 0 branch, run CI again, and complete manual Sprint 1 UI acceptance.
4. Only then consider merging PR #15. No merge to `main` is authorized by this progress update.
