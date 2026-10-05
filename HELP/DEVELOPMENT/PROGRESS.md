# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."

Last updated: 2026-10-06
Last updated by: AI agent (Phase D1 — Jalali date service)
Repository state this file describes: branch `codex-d1-jalali`, pending merge to `main`

---

## 1. Current project phase

**Phase D — Calendar & Date/Time**, current task **D1 (Jalali date service)**. Phases A, B, and C are complete.

## 2. Current task

**Task:** Phase D1 — Jalali date service.

**Task status:** COMPLETE on `codex-d1-jalali`. Added a focused Gregorian/Jalali conversion boundary while preserving Gregorian/Python datetime storage semantics.

## 3. Completed tasks

A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4, C5, and D1 are complete.

## 4. In-progress tasks

None.

## 5. Not-started tasks

- **Phase D2** — Header current date/time using the configured calendar/timezone.
- **Phase D3** — Jalali-aware appointment date input/display.
- **Phase E** — Dashboard & Reporting.
- **Phase F** — Messaging & Contacts.
- **Phase G** — Printing.
- **Phase H** — Local Database / SQLite.
- **Phase I** — Plugin Architecture.
- **Phase J** — Final QA & Security Hardening.

## 6. Last completed checkpoint

**Phase D1 — Jalali date service**, implemented on branch `codex-d1-jalali`.

## 7. Last successful verification

No local runtime verification was available in this GitHub-only session. The implementation was inspected for scope: no appointment model, schema, migration, or stored datetime semantics were changed.

## 8. Files changed by the current task

- `app/services/datetime_service.py`
- `tests/test_datetime_service.py`
- `HELP/DEVELOPMENT/PROGRESS.md`
- `HELP/DEVELOPMENT/CHANGELOG_DEV.md`

## 9. Current blockers

- Local compileall/pytest could not be run from the GitHub-only editing session.
- The pre-existing PostgreSQL migration-chain issue involving `appointmentstatus` remains outside D1 scope.

## 10. Decisions relevant to the current task

- DDR-001: phased A–J development plan is active.
- DDR-002: continuity files are the source of development continuity.
- D1 deliberately keeps database/business datetime values Gregorian/Python datetime and limits Jalali conversion to the presentation/input boundary.

## 11. Exact next action

Start **Phase D2 — Header current date/time**: use the existing Date & Time settings for calendar/timezone-aware display in the shared header, without changing stored appointment datetimes.

## 12. Recommended command(s) to verify the next action

```
python -m compileall app tests alembic
python -m pytest -q
```

For the header UI, perform the relevant authenticated dashboard/header smoke check.
