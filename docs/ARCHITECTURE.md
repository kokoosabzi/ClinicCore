# ClinicCore Architecture Status

## Structure

ClinicCore is a FastAPI application organized as routers → services → repositories → SQLAlchemy models. Pydantic schemas form API contracts; Jinja templates implement the Persian RTL interface; `app/core` provides settings, sessions, authentication, CSRF, audit logging, and database infrastructure. The `app/plugins` namespace is reserved for specialty workflows.

## Domain modules

| Module | Current status | Notes |
|---|---|---|
| Patients | Operational | CRUD API and protected RTL pages use a repository and service. |
| Appointments | Operational baseline | A shared active time slot is validated in `AppointmentService` and protected by a partial database unique index. Lifecycle actions and Jalali input remain planned. |
| Finance | Basic capture only | Payments and expenses exist; reports, balances, cash box, shares, and accounting journal entries do not exist. |
| Messaging | Development stub | Provider abstraction exists with a console provider; contacts and production providers remain planned. |
| Users/auth | Baseline | Session authentication, roles, CSRF-protected pages, and first-login password rotation exist. |
| Plugins | Placeholder | Psychology namespace exists but no plugin contract or workflow is implemented. |

## Appointment flow

The HTML and JSON routes construct `AppointmentCreate` data and invoke `AppointmentService.book`. The service rejects an existing non-deleted slot before insert. The partial unique index is the authoritative concurrent-write guard; an index violation is rolled back and reported as the same domain error. Timestamps are stored as Python `datetime` values in the database. Jalali conversion has not yet been implemented, so UI input is Gregorian `datetime-local`.

## Database and migrations

SQLAlchemy models are the application schema source; Alembic revisions manage deployment changes. The current migration head is `20261002_0004`. It adds `uq_active_appointment_starts_at`, a partial unique index over active appointments. Its downgrade removes that index. Existing deployments must correct duplicate active slot values before applying the revision; no records are silently deleted.

## UI and testing

Templates use the shared base layout and Persian RTL markup. Router dependencies enforce authenticated access; form writes validate CSRF tokens. Tests use an isolated in-memory SQLite schema and FastAPI test client. The environment must install the declared development dependencies (including `httpx`) to run the suite.

## Development phases

The immediate next prerequisite is Phase A4: make default-admin credential risk visible in startup and documentation. After stabilization, proceed with settings/design system, then Jalali calendar and appointment lifecycle, reporting, messaging contacts, printing, SQLite runtime support, plugins, and final QA as recorded in `HELP/DEVELOPMENT/PROGRESS.md`.
