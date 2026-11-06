# ClinicCore — Development Decision Records

این فایل تصمیم‌های معماری/محصولی پایدار را ثبت می‌کند. وضعیت جاری در `PROGRESS.md` و شرح تغییرات در `CHANGELOG_DEV.md` نگهداری می‌شود.

## DDR-001 — Adopt a phased plan (A–J) derived from the Gap Analysis
- Date: 2026-09-27
- Decision: Development proceeds through baseline, settings, design system, calendar, dashboard/reporting, messaging/contacts, printing, local database, plugins and final QA phases.
- Rationale: Keep large changes independently testable and preserve prerequisites.
- Status: Active.

## DDR-002 — Development continuity system location and scope
- Date: 2026-09-27
- Decision: Continuity state lives in PROGRESS.md, DECISIONS.md, CHANGELOG_DEV.md and CONTINUE_DEVELOPMENT.txt.
- Rationale: Work must be resumable without chat history.
- Status: Active.

## DDR-003 — Continuity files are documentation-only
- Date: 2026-09-27
- Decision: Continuity setup does not change application behavior or schema.
- Rationale: Keep process documentation separate from feature work.
- Status: Active.

## DDR-004 — Audit middleware test fixture compatibility
- Date: 2026-09-27
- Decision: Tests monkeypatch the audit middleware's directly imported SessionLocal rather than refactoring the middleware as part of fixture setup.
- Rationale: Avoid unrelated application refactoring.
- Status: Active.

## DDR-005 — Appointment slots are globally unique while active
- Date: 2026-10-02
- Decision: Exactly one non-deleted appointment may occupy a given starts_at value. The service checks availability and a partial unique index protects concurrent writes.
- Rationale: The current appointment model has no practitioner/room/resource scope.
- Status: Active. Replace through a new migration and decision if resource-scoped scheduling is introduced.

## DDR-006 — SQLite-only local runtime for the current Windows delivery phase
- Date: 2026-11-06
- Decision: The supported local installation target is Windows with file-backed SQLite at data/cliniccore.db. PostgreSQL and Docker are not prerequisites or supported runtime options in this phase.
- Rationale: Keep installation and operation simple for a single local clinic environment. The current application configuration rejects non-SQLite DATABASE_URL values and a file-backed migration test exists.
- Alternatives considered: Retain dual SQLite/PostgreSQL runtime support. Deferred because the current configuration and tests already define SQLite-only behavior and dual-dialect compatibility would expand the release surface.
- Safety constraint: This decision does not authorize deleting or modifying any pre-existing PostgreSQL database, Docker container, or volume outside this repository.
- Status: Active for the current local delivery phase.
