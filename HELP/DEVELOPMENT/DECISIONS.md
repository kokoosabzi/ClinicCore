# ClinicCore — Development Decision Records

This file records **durable architectural/product decisions** made during the
redesign/development phase (Phase A onward, per `MASTER_PLAN.md`).

It is deliberately separate from `HELP/DECISIONS.txt` (the original
pre-redesign ADR log) and from `PROGRESS.md`/`CHANGELOG_DEV.md`:

- `HELP/DECISIONS.txt` — architecture decisions from the original build (Sprints 1–4). Not superseded; keep reading it too.
- `HELP/DEVELOPMENT/DECISIONS.md` (this file) — decisions made during the current redesign effort (Phase A onward).
- `PROGRESS.md` — current state, not decisions.
- `CHANGELOG_DEV.md` — a log of what changed and when, not why.

**Rule:** only record something here if it is a real architectural or
product decision — something that constrains future work and would be
expensive to silently reverse. Do not log ordinary implementation notes,
bug fixes, or routine task completion here; those belong in
`CHANGELOG_DEV.md`.

Each entry: number, date, decision, rationale, alternatives considered,
status.

---

## DDR-001 — Adopt a phased plan (A–J) derived from the Gap Analysis

- **Date:** 2026-09-27
- **Decision:** Development proceeds through the phases defined in the
  Gap Analysis's phased implementation plan: A (baseline hardening) →
  B (Settings) → C (Design System) → D (Calendar) → E (Dashboard/Reporting)
  → F (Messaging/Contacts) → G (Printing) → H (SQLite) → I (Plugins) →
  J (Final QA). This mirrors `MASTER_PLAN.md` §4's phase ordering but
  subdivides it into independently-testable tasks.
- **Rationale:** `MASTER_PLAN.md` §8 requires no large phase in one commit;
  `AGENT_WORKFLOW.md` requires small, independently testable tasks with
  clear prerequisites.
- **Alternatives considered:** Re-deriving a plan from scratch on every
  resume. Rejected — wastes effort and risks inconsistent sequencing
  between sessions/agents.
- **Status:** Active. Supersede only via a new DDR here, not silently.

## DDR-002 — Development continuity system location and scope

- **Date:** 2026-09-27
- **Decision:** Development continuity state lives in
  `HELP/DEVELOPMENT/PROGRESS.md` (current state),
  `HELP/DEVELOPMENT/DECISIONS.md` (this file, durable decisions only),
  `HELP/DEVELOPMENT/CHANGELOG_DEV.md` (dev milestones/commits), and
  `HELP/CONTINUE_DEVELOPMENT.txt` (the reusable resume instruction for
  any future agent). `AGENT_WORKFLOW.md` §2 (Rule Zero) and §18
  (First Task for Codex) are extended, not replaced, to point at these
  files.
- **Rationale:** The task explicitly requires that development be
  resumable after session loss, plan/usage limits, or a switch to a
  different AI agent, without relying on conversation memory. Git-committed
  files are the only continuity mechanism that survives all of those
  failure modes.
- **Alternatives considered:** Relying on commit messages alone (rejected —
  insufficient detail for "exact next action" and "what was/wasn't
  verified"); a single combined file instead of four (rejected — mixes
  frequently-changing state with rarely-changing decisions, making diffs
  noisy and decisions hard to find).
- **Status:** Active.

## DDR-003 — Continuity files are documentation-only; no schema/behavior change

- **Date:** 2026-09-27
- **Decision:** Setting up the continuity system does not touch
  application code, models, migrations, templates, or tests. It is a
  pure documentation/process addition.
- **Rationale:** Explicit task scope ("Do NOT start Phase A implementation.
  Do NOT modify application functionality. Do NOT perform a broad
  refactor. Do NOT delete existing files.").
- **Alternatives considered:** None — this was a hard constraint, not a
  judgment call.
- **Status:** Active; satisfied by this task's diff (verify via `git diff`
  before commit — only `HELP/**` files should appear).

## DDR-004 — Test fixture monkeypatches the audit middleware's `SessionLocal`; middleware itself not refactored

- **Date:** 2026-09-27
- **Decision:** `tests/conftest.py`'s `client` fixture redirects database
  access to an isolated per-test SQLite database via two mechanisms:
  (1) overriding the FastAPI `get_db` dependency (used by all routers),
  and (2) monkeypatching `app.core.audit.SessionLocal` directly. (2) is
  needed because `app/core/audit.py` does
  `from app.core.database import SessionLocal` and calls `SessionLocal()`
  directly inside `audit_request_middleware`, bypassing FastAPI's
  dependency injection entirely — overriding `get_db` alone does not
  redirect it. The middleware itself was **not** changed to use
  dependency injection instead.
- **Rationale:** Phase A1's scope is a test fixture, not an application
  refactor ("Do not modify unrelated application code", "Do not
  silently fix unrelated issues" — explicit task constraints). Changing
  `audit_request_middleware` to accept an injected session is a real,
  reasonable fix, but it is an application-code change with its own
  blast radius (every request path) and belongs to a later, explicitly
  scoped task, not folded into a test-infrastructure task.
- **Alternatives considered:** Refactoring the middleware now to close
  the gap properly (rejected — out of A1's authorized scope). Skipping
  audit-safe testing and letting the middleware attempt a real
  PostgreSQL connection during tests (rejected — would make every
  DB-backed test fail or hang in any environment without a live
  PostgreSQL instance, defeating the purpose of an isolated fixture).
- **Status:** Active. Any future agent adding a *second* place that
  imports `SessionLocal` directly (instead of using `get_db`) must
  either route it through `get_db` or extend the same monkeypatch
  pattern in `tests/conftest.py` — grep for `SessionLocal` before
  assuming the `client` fixture covers a new code path.

---

## DDR-005 — Appointment slots are globally unique while active

- **Date:** 2026-10-02
- **Decision:** ClinicCore currently permits exactly one non-deleted appointment for a given `starts_at` value. The service performs an early availability check and a database partial unique index is the authoritative concurrent-write guard. Soft-deleted appointments release their time slot.
- **Rationale:** The present domain model has no practitioner, room, or resource field; its existing HTML route already treated every occupied start time as unavailable. Applying the rule in the service gives HTML and JSON routes identical behavior, while the partial index prevents a check-then-insert race without deleting historical records.
- **Alternatives considered:** Keeping validation only in the HTML router (rejected — API bypasses it); a normal unique index (rejected — it would prevent a replacement booking after soft deletion); a provider-scoped constraint (deferred — no provider/resource domain exists yet).
- **Status:** Active. When practitioner or room scheduling is added, replace this constraint with a scoped active-slot constraint through a new migration and decision record.

<!--
Template for new entries — copy this block for each new decision:

## DDR-0XX — <short title>

- **Date:** YYYY-MM-DD
- **Decision:** <what was decided>
- **Rationale:** <why>
- **Alternatives considered:** <what else was weighed, and why rejected>
- **Status:** Active | Superseded by DDR-0YY | Reverted
-->


## DDR-006 — SQLite-only local runtime for the current Windows delivery phase

- **Date:** 2026-11-06
- **Decision:** The supported local installation target is Windows with file-backed SQLite at `data/cliniccore.db`. PostgreSQL and Docker are not prerequisites or supported runtime options in this phase.
- **Rationale:** Keep installation and operation simple for a local clinic environment. The current application configuration rejects non-SQLite `DATABASE_URL` values and a file-backed migration test exists.
- **Alternatives considered:** Retain dual SQLite/PostgreSQL runtime support. Deferred because the current configuration and tests already define SQLite-only behavior and dual-dialect compatibility would expand the release surface.
- **Safety constraint:** This decision does not authorize deleting or modifying any pre-existing PostgreSQL database, Docker container, or volume outside this repository.
- **Status:** Active for the current local delivery phase.


## DDR-007 — Database-backed role and permission catalog

- **Date:** 2026-11-06
- **Decision:** Use normalized `roles`, `permissions`, and `role_permissions` tables with an additive Alembic migration. Keep the existing user role column and role keys for compatibility; add `clinic_manager` as a supported built-in role. The system administrator role is immutable and always retains all permissions. The administrator may adjust grants for other built-in roles.
- **Rationale:** This provides configurable least-privilege access without replacing the existing user model, rewriting account records, or introducing a complex policy engine. Resolving effective grants from the database on each protected request makes role and permission changes take effect without a server restart.
- **Alternatives considered:** Hard-coded permission dictionaries (rejected because administrators could not adjust grants); storing a JSON permission map in general settings (rejected because normalized constraints and queries are clearer); replacing the existing user role column with a new role foreign key (deferred to avoid a risky rewrite of existing accounts).
- **Safety constraints:** The migration must not modify existing usernames or password hashes. Only the system administrator may edit the permission matrix or grant the administrator role. The last active administrator cannot be demoted or deactivated. Alembic remains the only schema migration mechanism.
- **Status:** Active.
