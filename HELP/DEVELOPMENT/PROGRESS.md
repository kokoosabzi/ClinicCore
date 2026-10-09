# ClinicCore — Development Progress

> **Read this file first, before any other context, when resuming work.**
> This file is the single source of truth for "where development actually is."

Last updated: 2026-10-06
Last updated by: AI agent (Phase D3 — Jalali-aware appointment date input/display)
Repository state this file describes: branch `feature-calendar-input`, pending merge to `main`

---

## 1. Current project phase

**Phase D — Calendar & Date/Time**, current task **D3 (Jalali-aware appointment date input/display)**. Phases A, B, and C are complete.

## 2. Current task

**Task:** Phase D3 — Jalali-aware appointment date input/display.

**Task status:** IMPLEMENTED on `feature-calendar-input`. Appointment form input is interpreted using the configured calendar and converted to existing Gregorian datetime storage. Appointment list display uses the configured calendar, timezone-independent stored datetime, configured date/time format, seconds preference, and Persian numerals.

## 3. Completed tasks

A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4, C5, D1, D2, and D3 implementation are complete.

## 4. In-progress tasks

- D3 verification and review fixes.

## 5. Not-started tasks

- **Phase D4** — RTL/Jalali date picker.
- **Phase E** — Dashboard & Reporting.
- **Phase F** — Messaging & Contacts.
- **Phase G** — Printing.
- **Phase H** — Local Database / SQLite.
- **Phase I** — Plugin Architecture.
- **Phase J** — Final QA & Security Hardening.

## 6. Last completed checkpoint

**Phase D3 — Jalali-aware appointment date input/display**, implemented on `feature-calendar-input`.

## 7. Last successful verification

GitHub review identified conversion and formatting defects; those fixes are now applied. No local runtime verification is available in this GitHub-only session.

## 8. Current blockers

- Local compileall/pytest must still be run.
- PR #6 must receive a clean review after the fixes.
- The PostgreSQL migration-chain issue involving `appointmentstatus` remains a separate environment concern.

## 9. Decisions relevant to the current task

- Database/business datetime values remain Gregorian/Python datetime.
- Jalali conversion is limited to the presentation/input boundary.
- Invalid Jalali dates are rejected by round-trip validation.
- 12-hour time includes the Persian AM/PM marker, with seconds rendered before the marker.
- Calendar-formatted UI dates/times use Persian numerals.

## 10. Exact next action

Run compile/tests, review PR #6 again, then merge D3 only after the critical review findings are resolved. After that start **Phase D4 — RTL/Jalali date picker**.
