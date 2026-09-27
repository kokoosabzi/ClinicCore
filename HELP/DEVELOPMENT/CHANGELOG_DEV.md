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

## 2026-09-27 — Phase A2: Alembic reads database URL from application settings

- Phase/Task: Phase A / A2 (Alembic database URL)
- Commit: (recorded at commit time — see `git log`)
- Summary: `alembic/env.py` now sets Alembic's `sqlalchemy.url` from `settings.database_url`, making application settings the authoritative source. The hardcoded `sqlalchemy.url` entry was removed from `alembic.ini`. No models, routers, services, templates, static assets, or migration files were changed.
- Verification: `python -m compileall app tests alembic` — PASS in the Claude sandbox. `pytest` and a runtime Alembic migration were not available there because dependencies/database access were unavailable.
 ## 2026-09-27 — Phase A2: Alembic reads database URL from application settings

- Phase/Task: Phase A / A2 (Alembic database URL)
- Commit: (recorded at commit time — see `git log`)
- Summary: `alembic/env.py` now sets Alembic's `sqlalchemy.url` from `settings.database_url`, making application settings the authoritative source. The hardcoded URL entry was removed from `alembic.ini`. No models, routers, services, templates, static assets, or migration files were changed.
- Verification:
  - `python -m compileall app tests alembic` — PASS
  - `python -m pytest -q` — PASS, 7 tests passed
  - Alembic database URL resolution — PASS, `MATCH = True`
  - A real `alembic upgrade head` was intentionally not used as an A2 acceptance test because the existing PostgreSQL database has a separate pre-existing `appointmentstatus` duplicate-object migration issue.
- Status: COMPLETE

## 2026-09-27 — Phase A1: database test fixture

- Phase/Task: Phase A / A1 (Database Test Fixture)
- Commit: (recorded at commit time — see `git log`)
- Summary: Added `tests/conftest.py` (`db_engine`, `db_session_factory`,
  `db_session`, `client` fixtures — isolated in-memory SQLite per test,
  via `Base.metadata.create_all`, not Alembic) and
  `tests/test_db_fixture.py` (4 smoke tests: model persistence, test
  isolation, full HTTP CRUD round-trip, existing auth guard unaffected).
  No application code changed; see DDR-004 in `DECISIONS.md` for why the
  audit middleware required a monkeypatch rather than a refactor.
- Verification: `python -m compileall app` clean; `python -m pytest -q`
  — 7 passed (3 pre-existing + 4 new), 0 failed.

## 2026-09-27 — Development continuity system established

- Phase/Task: Phase 0 (pre-Phase-A) / continuity-system setup
- Commit: (recorded at commit time — see `git log`)
- Summary: Created `HELP/DEVELOPMENT/PROGRESS.md`,
  `HELP/DEVELOPMENT/DECISIONS.md`, `HELP/DEVELOPMENT/CHANGELOG_DEV.md`,
  and `HELP/CONTINUE_DEVELOPMENT.txt`; updated
  `HELP/DEVELOPMENT/AGENT_WORKFLOW.md` to reference the continuity
  system. No application code, migrations, templates, or tests changed.
- Verification: `python -m compileall app` and `python -m pytest -q`
  both pass (3/3 tests), matching the state already recorded in the
  Gap Analysis for commit `e46d5c24`. `git status`/`git diff` reviewed
  to confirm only `HELP/**` files are staged.
