# ClinicCore — Development Changelog

## 2026-11-06 — Phase 0: Windows and SQLite runtime stabilization

- Phase/Task: Phase 0 / Windows readiness
- Commit: pending branch completion
- Summary: Aligned the primary project documentation with the existing SQLite-only implementation and Windows local delivery target. Added secure first-install bootstrap and setup/start/stop scripts. Updated progress to distinguish source inspection from tests actually executed.
- Verification: GitHub source inspection only. No local Python test suite, Alembic command, or Windows manual test was run in this environment.

---

## 2026-10-06 — Phase D1: Jalali date service
- Phase/Task: Phase D / D1
- Commit: implementation commits on branch codex-d1-jalali
- Summary: Added Gregorian/Jalali conversion, formatting, and parsing helpers and focused unit coverage. Appointment storage remains Gregorian.
- Verification: Repository inspection; no fresh local compileall/pytest run was available.

## 2026-10-05 — Phase C2: design tokens and shared UI primitives
- Phase/Task: Phase C / C2
- Commit: `dbc25789b7ae8e316f671fb4cd4d8f36946b965c`
- Summary: Extracted shared color, typography, spacing, radius, shadow, and semantic state values into reusable CSS design tokens.
- Verification: Repository inspection; no fresh local compileall/pytest or browser smoke test was available.
