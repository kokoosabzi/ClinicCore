# ClinicCore Architecture Status

## Structure

ClinicCore is a FastAPI application organized as routers → services → repositories → SQLAlchemy models. Pydantic schemas form API contracts; Jinja templates implement the Persian RTL interface; `app/core` provides configuration, sessions, authentication, CSRF, audit logging, Persian helpers and database infrastructure.

## Runtime and persistence

- Supported deployment target: local Windows.
- Supported database: file-backed SQLite at `data/cliniccore.db` by default.
- Alembic is the only schema migration path. Do not use `Base.metadata.create_all` in installation or runtime bootstrap.
- PostgreSQL and Docker are not prerequisites for the current delivery target.
- Existing `.env` and database files must not be silently overwritten or removed by setup/start scripts.

## Domain modules

| Module | Current status | Notes |
|---|---|---|
| Patients | Operational baseline | CRUD API and protected RTL pages use repository/service layers. |
| Appointments | Booking baseline with Jalali UI | Dedicated Jalali calendar and available-time selection are implemented. Appointment timestamps are stored as Gregorian Python datetimes. Appointment lifecycle, configurable working hours and provider-specific schedules remain future work. |
| Finance | Basic record capture | Payment/expense records and print views exist; the application does not execute financial transactions. Reports, balances, cash box and accounting journal are not complete. |
| Messaging | Development foundation | Provider abstraction and console/development path exist. Production providers, contacts and delivery integration remain future work. |
| Users/auth | User administration and RBAC implemented | Session authentication, forced password rotation, five built-in roles, normalized permission catalog, route enforcement, CSRF-protected forms and role matrix are present. |
| Settings | Central settings baseline | Application/clinic identity, appearance, date/time, messaging, reports, contacts, print and system settings are stored through SettingsService. |
| Printing | Basic printable views | Patient, appointment and payment views exist. Print visual acceptance and full reporting/export layouts remain incomplete. |
| Plugins | Placeholder | No general plugin contract or production specialty workflow is implemented. |

## Appointment flow

The booking UI uses a dedicated Persian Jalali calendar rather than a free-text date field or the browser's Gregorian `datetime-local` input. The selected Jalali date is converted server-side by `datetime_service` to a Gregorian `datetime` for persistence. Available slots are queried for the selected day. `AppointmentService.book` checks for an existing active slot; a partial unique index is the final concurrent-write guard. The appointment form revalidates availability on save through the service.

The current default schedule is 09:00–17:00 in 30-minute slots. This is a baseline, not yet configurable per clinic, provider or day.

## Authentication and authorization

Five built-in roles are seeded by the additive RBAC migration: system administrator, clinic manager, doctor, secretary and accountant. Permissions are checked server-side and reloaded from persisted role grants on protected requests. The current model primarily enforces module/action boundaries; full record ownership/row-level rules (such as restricting doctors to assigned patients) are not complete and must not be assumed.

The application is not a financial transaction processor. Financial pages represent manually recorded clinic records.

## Database and migrations

The current RBAC schema revision is `20261106_0006`. The migration adds normalized roles, permissions and role-permission grants while preserving existing users and password hashes. Earlier migrations remain the source of schema history. Verify the current head with `alembic heads`; do not hard-code an older revision in operational instructions.

## UI and testing

Templates use the shared base layout and Persian RTL markup. The UI includes four system-wide visual presets and configurable font scale/density. Appearance settings are administrator-managed defaults; per-user overrides are not implemented. Print pages must remain paper-safe and visually independent of the selected application theme.

Automated Windows CI runs compilation, pytest and a clean SQLite Alembic migration. CI success does not establish manual Windows installation, browser visual acceptance, printer output, or real user workflow acceptance.

## Next development priorities

1. Complete manual Windows installation and browser acceptance, recording actual results.
2. Add explicit tests for Jalali date conversion boundaries, form validation and appointment availability edge cases.
3. Design and implement record-level access rules if doctor/patient ownership restrictions are required.
4. Add appointment lifecycle operations and configurable working schedules/durations.
5. Complete reporting/export and print QA.
6. Complete contacts and production messaging provider integrations.
7. Implement documented backup/restore workflow and final release QA.