# Sprint 2 - Operational MVP Shell

## Goal
Generate the main ClinicCore pages, modules, forms, API connections, and database routines so execution and full testing can happen after generation.

## Tasks
- Add users, financial, messaging, and audit models.
- Add schemas, repositories, services, and routers for operational modules.
- Add Persian RTL pages and forms for dashboard, patients, appointments, payments, expenses, and messages.
- Add secure password hashing helper.
- Add Alembic migration for new operational tables.

## Files affected
- `app/models/`
- `app/schemas/`
- `app/repositories/`
- `app/services/`
- `app/routers/`
- `app/templates/`
- `app/static/`
- `alembic/versions/`
- `HELP/`

## Database changes
- Add `users`.
- Add `payments`.
- Add `expenses`.
- Add `messages`.
- Add `audit_logs`.

## Risks
- Form handlers use simple URL-encoded parsing to avoid adding multipart dependencies.
- External messaging providers are placeholders only.

## Test plan
- Run compile checks after generation.
- Run pytest after dependencies are available.
- Run migrations against PostgreSQL.
