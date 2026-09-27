# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."
> If this file disagrees with a chat/session memory, this file wins.

Last updated: 2026-09-27
Last updated by: AI agent (Phase A2 — Alembic Database URL)
Repository state this file describes: branch `main`, baseline commit `ab4e2be`

---

## 1. Current project phase

**Phase A — Baseline hardening**, task **A1 (Database Test Fixture)**, per `MASTER_PLAN.md` §4 and the phased plan below: **Phase A (baseline hardening) → B (Settings) → C (Design System) → D (Calendar) → E (Dashboard/Reporting) → F (Messaging/Contacts) → G (Printing) → H (SQLite) → I (Plugins) → J (Final QA)**.

A1 is complete (see §3). A2 is implemented but **not runtime-verified**; A3–A4 and all later phases have not started.

## 2. Current task

**Task:** Phase A2 — Alembic Database URL. Make Alembic use the database URL resolved by `app.core.config.settings` (including `DATABASE_URL` / `.env`) instead of a hardcoded URL in `alembic.ini`.

**Task status:** `COMPLETE` — implementation and local verification completed in the repository clone. `python -m compileall app tests alembic` passed, all 7 tests passed, and the Alembic database URL resolution was verified to match `settings.database_url`. A real `alembic upgrade head` was not used as an A2 acceptance test because the existing PostgreSQL database has a separate pre-existing `appointmentstatus` duplicate-object migration issue.

## 3. Completed tasks

| Task | Status | Evidence |
|---|---|---|
| Repository inspection against `AGENTS.md` + development specs | COMPLETE | Gap Analysis delivered (20-section document + phased plan), based on a full read of `app/`, `alembic/`, `tests/`, `HELP/`, and a live `python -m compileall app` + `pytest` run (3/3 passed) on commit `e46d5c24`. |
| Development continuity system scaffolding | COMPLETE | Committed as `a13ea11` (verified via `git log`). |
| **Phase A1 — Database Test Fixture** | COMPLETE | `tests/conftest.py` (fixtures: `db_engine`, `db_session_factory`, `db_session`, `client`) + `tests/test_db_fixture.py` (4 tests). All 7 tests pass (`python -m pytest -q`); `python -m compileall app` clean. Isolation, full HTTP CRUD round-trip, and existing auth guard (`require_user`) all verified by the new tests themselves. |
| **Phase A2 — Alembic Database URL** | COMPLETE | `alembic/env.py` now uses `settings.database_url`; the hardcoded URL was removed from `alembic.ini`. Local verification: `python -m compileall app tests alembic` passed, `python -m pytest -q` passed with 7 tests, and direct URL resolution verification returned `MATCH = True`. |

## 4. In-progress tasks


## 5. Not-started tasks

- **Phase A (remaining)** — A3 (reconcile appointment double-booking rule between `pages.py` and `AppointmentService`), A4 (document/warn on default admin credentials).
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

Phase A1 (Database Test Fixture) implemented and verified this session, on top of the continuity-system commit `a13ea11`.
Phase A2 (Alembic Database URL) implemented and verified in the local repository clone.

## 7. Last successful verification

Run this session, on the repository state described above:

```
python -m compileall app     # PASS — no syntax/import errors
python -m pytest -q          # PASS — 7 passed:
                              #   test_health_endpoint
                              #   test_home_is_persian_rtl
                              #   test_password_hash_roundtrip
                              #   test_db_session_fixture_persists_and_queries_a_model
                              #   test_client_fixture_isolated_database_per_test
                              #   test_client_fixture_supports_full_crud_round_trip_through_http
                              #   test_client_fixture_still_enforces_authentication
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
- The existing PostgreSQL database still has a separate migration-chain issue (`appointmentstatus` already exists); this is outside A2 scope and was not changed as part of A2.
- Phase H (SQLite) is no longer blocked on A2 verification.

## 10. Decisions relevant to the current task

See `HELP/DEVELOPMENT/DECISIONS.md` DDR-004 for the one architectural note from A1 (the audit-middleware monkeypatch, and why it wasn't "fixed" instead).

## 11. Exact next action

Proceed to **Phase A3** after committing the verified Phase A2 changes.

## 12. Recommended command(s) to verify the next action

For Phase A3, first re-read `HELP/CONTINUE_DEVELOPMENT.txt`, `HELP/DEVELOPMENT/AGENT_WORKFLOW.md`, and this file. Then inspect the relevant appointment booking logic before making any changes.
