# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."
> If this file disagrees with a chat/session memory, this file wins.

Last updated: 2026-10-05
Last updated by: AI agent (Phase B4 — messaging settings)
Repository state this file describes: branch `main`, latest B4 reporting-settings implementation is recorded in the commits immediately preceding this continuity update

---

## 1. Current project phase

**Phase B — Settings & Application Identity**, next task **B4 (Messaging/Contacts/Reporting/Printing/System settings)**, per `MASTER_PLAN.md` §4 and the phased plan below: **Phase A (baseline hardening) → B (Settings) → C (Design System) → D (Calendar) → E (Dashboard/Reporting) → F (Messaging/Contacts) → G (Printing) → H (SQLite) → I (Plugins) → J (Final QA)**.

A1, A2, A3, A4, B1, B2, and B3 are complete. B4 is the next task within Phase B.

## 2. Current task

**Task:** Phase B4 — Messaging settings slice.

**Task status:** COMPLETE. Added persistent messaging enable/disable and default-provider settings with validation and admin UI controls. Provider credentials/secrets remain outside the settings store.

## 3. Completed tasks

| Task | Status | Evidence |
|---|---|---|
| Repository inspection against `AGENTS.md` + development specs | COMPLETE | Gap Analysis delivered (20-section document + phased plan), based on a full read of `app/`, `alembic/`, `tests/`, `HELP/`, and a live `python -m compileall app` + `pytest` run (3/3 passed) on commit `e46d5c24`. |
| Development continuity system scaffolding | COMPLETE | Committed as `a13ea11`. |
| **Phase A1 — Database Test Fixture** | COMPLETE | Added isolated SQLite fixtures and 4 smoke tests; 7 tests passed. |
| **Phase A2 — Alembic Database URL** | COMPLETE | `alembic/env.py` uses `settings.database_url`; hardcoded URL removed from `alembic.ini`; compileall, 7 tests, and URL resolution verification passed. |
| **Phase A3 — Appointment booking integrity** | COMPLETE | PR #3 merged into `main` on 2026-10-05 as merge commit `427e9157057ea0daa64e2c176316a0ef9b723061`. Centralized active-slot validation in `AppointmentService`, added the active-slot partial unique index migration, unified HTML/JSON booking behavior, and added booking conflict scenarios. |
| **Phase A4 — Default admin credential warning/documentation** | COMPLETE | Added a seed-time warning for the insecure `admin` fallback password and clarified the production credential requirement in `HELP/AUTHENTICATION.txt`, `HELP/IMPLEMENTATION.txt`, and `HELP/RUN.txt`. |
| **Phase B1 — Persistent application identity settings** | COMPLETE | Added persistent `system_settings`, a central `SettingsService`, admin-only `/settings` UI, application/clinic identity fields, and dynamic application identity in shared/auth/home templates. |
| **Phase B2 — Theme/mode and appearance settings** | COMPLETE | Added persistent light/dark/system theme and comfortable/compact density settings, validation, admin UI controls, and dynamic application-wide rendering through the shared layout. |
| **Phase B3 — Date & Time settings** | COMPLETE | Added persistent calendar, timezone, date-format, time-format, and seconds-display preferences, validation, admin UI controls, and shared-layout propagation. Business datetime storage and Jalali conversion remain outside B3 scope. |

## 4. In-progress tasks

None.

## 5. Not-started tasks

- **Phase B4** — Contacts/Printing/System settings.
- **Phase C** — Design System & Navigation (design tokens, shared partials, Back/Breadcrumb, theme).
- **Phase D** — Calendar & Date/Time (Jalali conversion service, header clock, date picker).
- **Phase E** — Dashboard & Reporting (today's-appointments KPI fix, charts, report pages).
- **Phase F** — Messaging & Contacts (Contact model/CRUD, honest provider selection).
- **Phase G** — Printing (clinic identity/logo on receipts, shared print partial).
- **Phase H** — Local Database / SQLite.
- **Phase I** — Plugin Architecture (contract + psychology plugin as reference implementation).
- **Phase J** — Final QA & Security Hardening.

## 6. Last completed checkpoint

**Phase B4 — Messaging settings slice**, implemented on `main`; this slice is complete and the next B4 slice is Contacts settings.

## 7. Last successful verification

For A3, the PR branch reported:
- `python -m compileall app tests alembic` — PASS.
- Fresh SQLite Alembic upgrade through revision `20261002_0004` — PASS.
- Direct in-memory scenario — PASS: duplicate active-slot booking rejected; soft-deleted appointment releases the slot.
- Full `pytest` was not completed for A3 because `httpx` was unavailable in the environment and installing dev dependencies from PyPI failed with HTTP 403.

Do not treat the A3 PR verification as a fresh post-merge full test run; it is the verification recorded for the merged change.

## 8. Files changed by the current task

B4 reporting-settings changed:
- `app/services/settings_service.py`
- `app/core/database.py`
- `app/routers/pages.py`
- `app/main.py`
- `app/templates/base.html`
- `app/templates/settings.html`
- `app/static/css/app.css`
- `app/models/__init__.py`
- `app/services/settings_service.py`
- `app/core/database.py`
- `app/routers/pages.py`
- `app/main.py`
- `app/templates/base.html`
- `app/templates/home.html`
- `app/templates/settings.html`
- `app/templates/auth/login.html`
- `alembic/versions/20261005_0005_system_settings.py`
- `tests/test_settings.py`

This continuity update changes:
- `HELP/DEVELOPMENT/PROGRESS.md`
- `HELP/DEVELOPMENT/CHANGELOG_DEV.md`

## 9. Current blockers

- No blocker is recorded for Phase B.
- The pre-existing PostgreSQL migration-chain issue involving `appointmentstatus` remains a known environment/database issue and was not part of A3's scope.

## 10. Decisions relevant to the current task

- DDR-001: phased A–J development plan is active.
- DDR-002: continuity files are the source of development continuity.
- DDR-004: test fixture audit-middleware `SessionLocal` handling remains intentionally scoped.
- DDR-005: active appointment slots are globally unique until practitioner/room/resource scoping is introduced.

## 11. Exact next action

Start **Phase B4 — Contacts settings**: inspect the existing patient/contact abstractions and add the smallest safe persistent contact configuration slice. Keep the task limited to settings/contacts behavior.

## 12. Recommended command(s) to verify the next action

Before editing:
- Read `HELP/CONTINUE_DEVELOPMENT.txt`, `HELP/DEVELOPMENT/AGENT_WORKFLOW.md`, `HELP/DEVELOPMENT/PROGRESS.md`, `HELP/DEVELOPMENT/DECISIONS.md`.
- Inspect the admin bootstrap/authentication implementation and the relevant install/run documentation.

After editing:
```
python -m compileall app tests alembic
python -m pytest -q
```

For any auth/UI change, also perform the relevant smoke/manual acceptance checks from `HELP/DEVELOPMENT/ACCEPTANCE_TESTS.md` and `AGENT_WORKFLOW.md`.
