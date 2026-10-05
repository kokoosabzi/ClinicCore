# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."

Last updated: 2026-10-06
Last updated by: AI agent (Phase D2 — Header current date/time)
Repository state this file describes: branch `codex-d2-header-clock-20261006`, pending merge to `main`

---

## 1. Current project phase

**Phase D — Calendar & Date/Time**, current task **D2 (Header current date/time)**. Phases A, B, and C are complete.

## 2. Current task

**Task:** Phase D2 — Header current date/time.

**Task status:** COMPLETE on `codex-d2-header-clock-20261006`. The shared header now displays the current date/time using the configured calendar, timezone, date format, time format, and seconds preference. Stored appointment datetime semantics are unchanged.

## 3. Completed tasks

A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4, C5, D1, and D2 are complete.

## 4. In-progress tasks

None.

## 5. Not-started tasks

- **Phase D3** — Jalali-aware appointment date input/display.
- **Phase E** — Dashboard & Reporting.
- **Phase F** — Messaging & Contacts.
- **Phase G** — Printing.
- **Phase H** — Local Database / SQLite.
- **Phase I** — Plugin Architecture.
- **Phase J** — Final QA & Security Hardening.

## 6. Last completed checkpoint

**Phase D2 — Header current date/time**, implemented on branch `codex-d2-header-clock-20261006`.

## 7. Last successful verification

No local runtime verification was available in this GitHub-only session. Repository inspection confirmed the header uses the configured settings and no appointment model, schema, migration, or stored datetime semantics were changed.

## 8. Files changed by the current task

- `app/services/datetime_service.py`
- `app/core/database.py`
- `app/templates/base.html`
- `app/static/css/app.css`
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
- D2 derives the displayed clock from the current UTC instant and converts it with the configured IANA timezone before applying calendar/format preferences.

## 11. Exact next action

Start **Phase D3 — Jalali-aware appointment date input/display**: adapt appointment date entry and display to the configured calendar while converting values back to the existing Gregorian datetime storage format.

## 12. Recommended command(s) to verify the next action

```
python -m compileall app tests alembic
python -m pytest -q
```

For the header UI, perform the relevant authenticated dashboard/header smoke check.
