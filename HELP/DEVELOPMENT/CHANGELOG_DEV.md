# ClinicCore — Development Changelog (Redesign Phase)

Concise, chronological log of development milestones and commits made
during the current redesign effort (Phase A onward, per `MASTER_PLAN.md`).

This is separate from `HELP/CHANGELOG.txt` (the original Sprint 1–4
changelog, which is not superseded — keep reading both) and from
`HELP/DEVELOPMENT/DECISIONS.md` (why something was decided, not what/when
changed).

**Format per entry:**

```
## YYYY-MM-DD — <short title>
- Phase/Task: <e.g. Phase A / A2>
- Commit: <short hash, once committed>
- Summary: <1-3 sentences, what changed>
- Verification: <what was run/checked>
```

Add the newest entry at the top.

---

## 2026-10-05 — Phase A4: default admin credential warning

- Phase/Task: Phase A / A4
- Commit: `7afed422fd60c6764d4eb01f25237a0fd56ea556` (documentation/run-guide update; implementation commits immediately before this continuity update include `8ab5517`, `893c754`, and `4218d8d`)
- Summary: The admin seed command now prints a security warning when the insecure `admin` fallback password is used. Authentication, implementation, and run guides now clearly identify the fallback as development-only and require production credentials to be configured before seeding.
- Verification: Repository/code inspection completed; A4 changes are limited to the admin bootstrap warning and related documentation. No fresh local `pytest` or `compileall` run was available in this GitHub-only session.

## 2026-10-05 — Phase A3 merged to main and continuity state synchronized

- Phase/Task: Phase A / A3 (appointment booking integrity)
- Commit: `427e9157057ea0daa64e2c176316a0ef9b723061` (merge commit)
- Summary: Merged PR #3 into `main`, bringing the centralized active-slot booking validation, partial unique index migration, unified HTML/JSON booking flow, and appointment conflict scenarios into the final branch. Synchronized `HELP/DEVELOPMENT/PROGRESS.md` so it now identifies A4 as the next unfinished task.
- Verification: Merge completed successfully on GitHub. The A3 verification recorded before merge passed for `python -m compileall app tests alembic`, fresh SQLite Alembic upgrade through `20261002_0004`, and direct duplicate/soft-delete slot scenarios. A post-merge full `pytest` run was not performed in this documentation-only update.

## 2026-10-02 — Phase A3: appointment booking integrity

- Phase/Task: Phase A / A3 (reconcile duplicate appointment booking rule)
- Commit: `184d9edf82e06cb1ac00c508a0386c35d1d73b0d` (PR #3 head; merged to `main` as `427e915`)
- Summary: Moved active-slot validation from the HTML page router into `AppointmentService`, routed JSON and HTML booking through that service, and added a partial unique index migration that excludes soft-deleted appointments. Added duplicate-slot and released-slot API scenarios.
- Verification: `python -m compileall app tests alembic` — PASS. Fresh SQLite Alembic upgrade through `20261002_0004` — PASS. Direct in-memory duplicate-slot rejection and soft-deleted slot release — PASS. Full `pytest` was blocked before collection because `httpx` was not installed; installing dev dependencies from PyPI failed with HTTP 403.

## 2026-09-27 — Phase A2: Alembic reads database URL from application settings

- Phase/Task: Phase A / A2 (Alembic database URL)
- Commit: (recorded at commit time — see `git log`)
- Summary: `alembic/env.py` now sets Alembic's `sqlalchemy.url` from `settings.database_url`, making application settings the authoritative source. The hardcoded `sqlalchemy.url` entry was removed from `alembic.ini`. No models, routers, services, templates, static assets, or migration files were changed.
- Verification:
  - `python -m compileall app tests alembic` — PASS
  - `python -m pytest -q` — PASS, 7 tests passed
  - Alembic database URL resolution — PASS, `MATCH = True`
  - A real `alembic upgrade head` was intentionally not used as an A2 acceptance test because the existing PostgreSQL database has a separate pre-existing `appointmentstatus` duplicate-object migration issue.
- Status: COMPLETE

## 2026-09-27 — Phase A1: database test fixture

- Phase/Task: Phase A / A1 (Database Test Fixture)
- Commit: (recorded at commit time — see `git log`)
- Summary: Added `tests/conftest.py` (`db_engine`, `db_session_factory`, `db_session`, `client` fixtures — isolated in-memory SQLite per test, via `Base.metadata.create_all`, not Alembic) and `tests/test_db_fixture.py` (4 smoke tests: model persistence, test isolation, full HTTP CRUD round-trip, existing auth guard unaffected). No application code changed; see DDR-004 in `DECISIONS.md` for why the audit middleware required a monkeypatch rather than a refactor.
- Verification: `python -m compileall app` clean; `python -m pytest -q` — 7 passed (3 pre-existing + 4 new), 0 failed.

## 2026-09-27 — Development continuity system established

- Phase/Task: Phase 0 (pre-Phase-A) / continuity-system setup
- Commit: (recorded at commit time — see `git log`)
- Summary: Created `HELP/DEVELOPMENT/PROGRESS.md`, `HELP/DEVELOPMENT/DECISIONS.md`, `HELP/DEVELOPMENT/CHANGELOG_DEV.md`, and `HELP/CONTINUE_DEVELOPMENT.txt`; updated `HELP/DEVELOPMENT/AGENT_WORKFLOW.md` to reference the continuity system. No application code, migrations, templates, or tests changed.
- Verification: `python -m compileall app` and `python -m pytest -q` both pass (3/3 tests), matching the state already recorded in the Gap Analysis for commit `e46d5c24`. `git status`/`git diff` reviewed to confirm only `HELP/**` files are staged.
