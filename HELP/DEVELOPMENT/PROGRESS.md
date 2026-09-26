# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."
> If this file disagrees with a chat/session memory, this file wins.

Last updated: 2026-09-27
Last updated by: AI agent (continuity-system setup task)
Repository state this file describes: branch `main`, commit `e46d5c24b28937abcf6a267975b83b32a6908281`

---

## 1. Current project phase

**Phase 0 — Baseline & Continuity Setup** (per `MASTER_PLAN.md` §4 "Phase 0 — Baseline & Specification", extended to include the development-continuity system).

The Gap Analysis (see `HELP/DEVELOPMENT/GAP_ANALYSIS.md` if present, or the most recent Gap Analysis delivered to the project owner) has been completed and defines the phased plan referenced throughout this file: **Phase A (baseline hardening) → B (Settings) → C (Design System) → D (Calendar) → E (Dashboard/Reporting) → F (Messaging/Contacts) → G (Printing) → H (SQLite) → I (Plugins) → J (Final QA)**.

No implementation phase (A through J) has started yet. This is intentional — the current task was scoped to build the continuity system only.

## 2. Current task

**Task:** Establish the Git-based development continuity/checkpoint system (this file, `DECISIONS.md`, `CHANGELOG_DEV.md`, `HELP/CONTINUE_DEVELOPMENT.txt`, and an update to `AGENT_WORKFLOW.md`).

**Task status:** `IN_PROGRESS` → will be marked `COMPLETE` in this same file once baseline tests are re-run and the commit is made (see §12 of `AGENT_WORKFLOW.md` — a task is only complete after verification, docs, and commit).

## 3. Completed tasks

| Task | Status | Evidence |
|---|---|---|
| Repository inspection against `AGENTS.md` + development specs | COMPLETE | Gap Analysis delivered (20-section document + phased plan), based on a full read of `app/`, `alembic/`, `tests/`, `HELP/`, and a live `python -m compileall app` + `pytest` run (3/3 passed) on commit `e46d5c24`. |
| Development continuity system scaffolding | IN_PROGRESS (this task) | This file + `DECISIONS.md` + `CHANGELOG_DEV.md` + `HELP/CONTINUE_DEVELOPMENT.txt` created; `AGENT_WORKFLOW.md` updated in the same commit. |

No implementation phase (A–J) task has been started or completed. Do not mark any Phase A–J task as complete unless a future PROGRESS.md update documents real repository evidence for it.

## 4. In-progress tasks

- Continuity system setup (this task) — see §2.

## 5. Not-started tasks

All of Phase A through Phase J from the Gap Analysis phased plan are **NOT_STARTED**:

- **Phase A** — Baseline hardening: A1 (DB test fixture), A2 (fix `alembic.ini`/`env.py` hardcoded Postgres URL), A3 (reconcile appointment double-booking rule between `pages.py` and `AppointmentService`), A4 (document/warn on default admin credentials).
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

Gap Analysis completed and delivered (repository read-only inspection, commit `e46d5c24`). This continuity-system task is the current checkpoint being closed out.

## 7. Last successful verification

Run against commit `e46d5c24`, this session:

```
python -m compileall app     # PASS — no syntax/import errors
python -m pytest -q          # PASS — 3 passed (test_health_endpoint,
                              #        test_home_is_persian_rtl,
                              #        test_password_hash_roundtrip)
```

No database was available in the verification environment, so DB-backed routes (dashboard, patients, appointments, financial, messaging pages) were **not** exercised via live HTTP calls — this was true for the Gap Analysis and remains true now. Phase A1 (add a DB test fixture) is the task that will close this gap; until then, do not assume DB-backed routes are verified beyond static code review.

## 8. Files changed by the current task

- `HELP/DEVELOPMENT/PROGRESS.md` — created (this file)
- `HELP/DEVELOPMENT/DECISIONS.md` — created
- `HELP/DEVELOPMENT/CHANGELOG_DEV.md` — created
- `HELP/CONTINUE_DEVELOPMENT.txt` — created
- `HELP/DEVELOPMENT/AGENT_WORKFLOW.md` — updated (added a "Continuity System" section referencing the four files above)

No application code, templates, migrations, or tests were touched by this task.

## 9. Current blockers

None blocking the continuity system itself. Blockers that **will** affect the next phase (Phase A):

- Phase H (SQLite) cannot start until Phase A2 (hardcoded Postgres URL in `alembic.ini`/`env.py`) is fixed — recorded as a dependency, not an active blocker yet since Phase H is not next.
- No PostgreSQL instance was available in the verification environment used for the Gap Analysis or this task — DB-backed manual verification steps in `ACCEPTANCE_TESTS.md` (AT-003 beyond `/health`, AT-501 dashboard KPIs, etc.) still need to be run in an environment with a real database before being marked verified.

## 10. Decisions relevant to the current task

See `HELP/DEVELOPMENT/DECISIONS.md` for the durable record. Summary: the continuity system itself is additive documentation only (no code/schema/behavior change), so no architectural decision record was required for this task beyond documenting the continuity workflow's existence.

## 11. Exact next action

Start **Phase A1**: add a `pytest` fixture that provisions a throwaway database (SQLite in-memory or temp file, independent of the later Phase H Local-deployment SQLite decision) so that subsequent phases can write real CRUD/auth-flow tests. This is the smallest, least ambiguous, dependency-free next task in the plan.

If Phase A1 is judged unnecessary or already superseded by a different testing decision when work resumes, the next agent must record that as a decision in `DECISIONS.md` before deviating — do not silently skip it.

## 12. Recommended command(s) to verify the next action

Before starting Phase A1:

```bash
git status
git log --oneline -10
cat HELP/DEVELOPMENT/PROGRESS.md   # re-read this file for any update since this snapshot
python -m compileall app
python -m pytest -q
```

After implementing Phase A1 (example — adjust to the fixture actually built):

```bash
python -m pytest -q                     # full suite still green
python -m pytest -q tests/ -k db        # new DB-fixture-based tests, if named accordingly
python -m compileall app tests
```

Do not mark Phase A1 complete in this file until both the implementation and a passing test run are confirmed in the same session, per `AGENT_WORKFLOW.md` §16 (Completion Criteria).
