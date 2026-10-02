# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."
> If this file disagrees with a chat/session memory, this file wins.

Last updated: 2026-10-02
Last updated by: AI agent (Phase A3 — Appointment Booking Integrity)
Repository state this file describes: branch `integration/bonyancore-unified`, baseline commit `0b73724` plus the A3 work described below

---

## 1. Current project phase

**Phase A — Baseline hardening**, task **A1 (Database Test Fixture)**, per `MASTER_PLAN.md` §4 and the phased plan below: **Phase A (baseline hardening) → B (Settings) → C (Design System) → D (Calendar) → E (Dashboard/Reporting) → F (Messaging/Contacts) → G (Printing) → H (SQLite) → I (Plugins) → J (Final QA)**.

A1–A3 are complete. A4 and all later phases have not started.

## 2. Current task

**Task:** Phase A3 — reconcile the appointment double-booking rule between `pages.py` and `AppointmentService`.

**Task status:** `COMPLETE` — both booking routes now use `AppointmentService`; active slots are protected by a reversible partial unique index migration. Compilation and a clean SQLite Alembic upgrade were verified. Full pytest is environment-blocked because its declared `httpx` test dependency is not installed and package installation cannot reach PyPI.

## 3. Completed tasks

| Task | Status | Evidence |
|---|---|---|
| Repository inspection against `AGENTS.md` + development specs | COMPLETE | Gap Analysis delivered (20-section document + phased plan), based on a full read of `app/`, `alembic/`, `tests/`, `HELP/`, and a live `python -m compileall app` + `pytest` run (3/3 passed) on commit `e46d5c24`. |
| Development continuity system scaffolding | COMPLETE | Committed as `a13ea11` (verified via `git log`). |
| **Phase A1 — Database Test Fixture** | COMPLETE | `tests/conftest.py` (fixtures: `db_engine`, `db_session_factory`, `db_session`, `client`) + `tests/test_db_fixture.py` (4 tests). All 7 tests pass (`python -m pytest -q`); `python -m compileall app` clean. Isolation, full HTTP CRUD round-trip, and existing auth guard (`require_user`) all verified by the new tests themselves. |
| **Phase A2 — Alembic Database URL** | COMPLETE | `alembic/env.py` now uses `settings.database_url`; the hardcoded URL was removed from `alembic.ini`. Local verification: `python -m compileall app tests alembic` passed, `python -m pytest -q` passed with 7 tests, and direct URL resolution verification returned `MATCH = True`. |
| **Phase A3 — Appointment Booking Integrity** | COMPLETE | `AppointmentService` is the single validation point for API and UI bookings; migration `20261002_0004` adds a partial unique active-slot index; duplicate and released-slot scenarios are covered in `tests/test_appointment_booking.py`. Compilation and a fresh SQLite migration upgrade passed. |

## 4. In-progress tasks


## 5. Not-started tasks

- **Phase A (remaining)** — A4 (document/warn on default admin credentials).
- **Phase B** — Settings & Application Identity (model, service, `/settings` UI, permissions).
- **Phase C** — Design System & Navigation (design tokens, shared partials, Back/Breadcrumb, theme).
- **Phase D** — Calendar & Date/Time (Jalali conversion service, header clock, date picker).
- **Phase E** — Dashboard & Reporting (today's-appointments KPI fix, charts, report pages).
- **Phase F** — Messaging & Contacts (Contact model/CRUD, honest provider selection).
- **Phase G** — Printing (clinic identity/logo on receipts, shared print partial).
- **Phase H** — Local Database / SQLite (blocked on A2 specifically).
- **Phase I** — Plugin Architecture (contract + psychology plugin as reference implementation).
- **Phase J** — Final QA & Security Hardening.

## 6. Last completed checkpoint

Phase A3 (Appointment Booking Integrity) is implemented and verified for compilation and a fresh SQLite Alembic migration chain.

## 7. Last successful verification

Run this session, on the repository state described above:

```
python -m compileall app tests alembic  # PASS — no syntax/import errors
DATABASE_URL=sqlite:////tmp/cliniccore-alembic.db alembic upgrade head  # PASS — reaches 20261002_0004
python -m pytest -q  # BLOCKED before collection: `httpx` is not installed; PyPI access returned 403 while installing `.[dev]`.
```

DB-backed routes can now be exercised in tests via the `client`/`db_session` fixtures in `tests/conftest.py` (SQLite in-memory, isolated per test). This does **not** verify the app against real PostgreSQL, nor does it verify the Alembic migration chain — both remain open per Gap Analysis §15/§17 and are unrelated to A1's scope (A1 uses `Base.metadata.create_all`, not Alembic).

## 8. Files changed by the current task

- `alembic/env.py` — added `settings.database_url` as the authoritative Alembic database URL.
- `alembic.ini` — removed the hardcoded `sqlalchemy.url` entry.
- `HELP/DEVELOPMENT/PROGRESS.md` — this update.
- `HELP/DEVELOPMENT/CHANGELOG_DEV.md` — A2 entry added.

No models, routers, services, templates, static assets, or migration files were changed.

## 9. Current blockers

-- No blocker remains for Phase A2.
- Full pytest is blocked by environment dependency availability (`httpx` missing; network denied while installing it).
- PostgreSQL migration application remains unverified. Existing deployments with duplicate active appointment start times must resolve those records before applying migration `20261002_0004`; the migration intentionally preserves data rather than selecting a record to delete.

## 10. Decisions relevant to the current task

See `HELP/DEVELOPMENT/DECISIONS.md` DDR-005 for the active shared-slot policy and its future migration path.

## 11. Exact next action

Proceed to **Phase A4**: document and warn about default administrator credentials before further feature work.

## 12. Recommended command(s) to verify the next action

For Phase A4, first re-read `HELP/CONTINUE_DEVELOPMENT.txt`, `HELP/DEVELOPMENT/AGENT_WORKFLOW.md`, and this file. Then inspect startup, authentication, seed scripts, and user-facing documentation before making any changes.
