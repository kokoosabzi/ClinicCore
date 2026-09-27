# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."
> If this file disagrees with a chat/session memory, this file wins.

Last updated: 2026-09-27
Last updated by: AI agent (Phase A1 — Database Test Fixture)
Repository state this file describes: branch `main`, commit `a13ea11` (continuity system) + this session's uncommitted Phase A1 changes

---

## 1. Current project phase

**Phase A — Baseline hardening**, task **A1 (Database Test Fixture)**, per `MASTER_PLAN.md` §4 and the phased plan below: **Phase A (baseline hardening) → B (Settings) → C (Design System) → D (Calendar) → E (Dashboard/Reporting) → F (Messaging/Contacts) → G (Printing) → H (SQLite) → I (Plugins) → J (Final QA)**.

A1 is complete (see §3). A2–A4 and all later phases have not started.

## 2. Current task

**Task:** Phase A1 — Database Test Fixture. Provide a pytest fixture that provisions an isolated, throwaway database so later phases can write real CRUD/auth-flow tests, without touching the real PostgreSQL development database.

**Task status:** `COMPLETE` — implemented, verified (`compileall` + full `pytest` suite green, 7/7), and documented in this same session. Not yet committed to git as of this update (commit happens immediately after this file is saved, per `HELP/CONTINUE_DEVELOPMENT.txt` step 7).

## 3. Completed tasks

| Task | Status | Evidence |
|---|---|---|
| Repository inspection against `AGENTS.md` + development specs | COMPLETE | Gap Analysis delivered (20-section document + phased plan), based on a full read of `app/`, `alembic/`, `tests/`, `HELP/`, and a live `python -m compileall app` + `pytest` run (3/3 passed) on commit `e46d5c24`. |
| Development continuity system scaffolding | COMPLETE | Committed as `a13ea11` (verified via `git log`). |
| **Phase A1 — Database Test Fixture** | COMPLETE | `tests/conftest.py` (fixtures: `db_engine`, `db_session_factory`, `db_session`, `client`) + `tests/test_db_fixture.py` (4 tests). All 7 tests pass (`python -m pytest -q`); `python -m compileall app` clean. Isolation, full HTTP CRUD round-trip, and existing auth guard (`require_user`) all verified by the new tests themselves. |

No implementation phase task beyond A1 has been started or completed. Do not mark any later Phase A–J task as complete unless a future PROGRESS.md update documents real repository evidence for it.

## 4. In-progress tasks

None.

## 5. Not-started tasks

- **Phase A (remaining)** — A2 (fix `alembic.ini`/`env.py` hardcoded Postgres URL), A3 (reconcile appointment double-booking rule between `pages.py` and `AppointmentService`), A4 (document/warn on default admin credentials).
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

- `tests/conftest.py` — created. Fixtures: `db_engine`, `db_session_factory`, `db_session`, `client`. See its module docstring for the audit-middleware monkeypatch rationale.
- `tests/test_db_fixture.py` — created. 4 smoke tests proving isolation, a full HTTP CRUD round-trip, and that the existing `require_user` auth guard is unaffected by the DB override.
- `HELP/DEVELOPMENT/PROGRESS.md` — this update.
- `HELP/DEVELOPMENT/CHANGELOG_DEV.md` — new entry added (see file).

No application code (`app/**`), migrations, templates, or static assets were touched by this task.

## 9. Current blockers

None for A1 (complete). Carried forward, unchanged, affecting later phases:

- Phase H (SQLite) cannot start until Phase A2 (hardcoded Postgres URL in `alembic.ini`/`env.py`) is fixed.
- No PostgreSQL instance is available in the current verification environment — real-Postgres and Alembic-migration verification steps in `ACCEPTANCE_TESTS.md` still need to be run in an environment with a real database before being marked verified. A1's SQLite fixture does not close this gap; it only unblocks fast, isolated unit/integration tests.

## 10. Decisions relevant to the current task

See `HELP/DEVELOPMENT/DECISIONS.md` DDR-004 for the one architectural note from A1 (the audit-middleware monkeypatch, and why it wasn't "fixed" instead).

## 11. Exact next action

Start **Phase A2**: make Alembic read the database URL from `app.core.config.settings`/`DATABASE_URL` instead of the value hardcoded in `alembic.ini`, per Gap Analysis §5/§14 and `PROGRESS.md`'s prior blocker notes. This is required before Phase H (SQLite) can start, and is otherwise independent of A1.

If A2 is judged unnecessary or superseded when work resumes, record that as a decision in `DECISIONS.md` before deviating — do not silently skip it.

## 12. Recommended command(s) to verify the next action

Before starting Phase A2:

```bash
git status
git log --oneline -10
cat HELP/DEVELOPMENT/PROGRESS.md   # re-read this file for any update since this snapshot
python -m compileall app
python -m pytest -q
grep -n "sqlalchemy.url" alembic.ini
sed -n '1,40p' alembic/env.py
```

After implementing Phase A2 (adjust to what's actually built — e.g. if a test spins up a scratch SQLite/Postgres DB and runs `alembic upgrade head` against it):

```bash
python -m pytest -q
python -m compileall app tests
alembic upgrade head   # against whatever DB the fix targets, once implemented
```

Do not mark Phase A2 complete in `PROGRESS.md` until both the implementation and a passing verification run are confirmed in the same session, per `AGENT_WORKFLOW.md` §16 (Completion Criteria).
