# Sprint 5 - Appointment Booking Integrity

## Goal
Make the single shared clinic schedule reliable by enforcing the same active-slot rule for JSON and HTML appointment booking flows.

## Tasks
- Move duplicate-slot validation from the page router into `AppointmentService`.
- Enforce one active appointment per `starts_at` value with a partial unique index.
- Translate duplicate slots into a consistent HTTP 409 response.
- Add API scenario tests for duplicate and soft-deleted appointments.

## Files affected
- `app/models/appointment.py`
- `app/repositories/appointment_repository.py`
- `app/services/appointment_service.py`
- `app/routers/appointments.py`
- `app/routers/pages.py`
- `alembic/versions/20261002_0004_active_appointment_slot.py`
- `tests/test_appointment_booking.py`

## Database changes
Adds `uq_active_appointment_starts_at`, a partial unique index that applies only to non-deleted appointments. Existing databases must resolve duplicate active `starts_at` values before the migration can be applied; the migration intentionally does not delete or alter existing appointments.

## Risks
This is a single shared-slot policy. A future practitioner/resource scheduling module must replace the index with a scoped constraint such as `(provider_id, starts_at)`.

## Test plan
- `python -m compileall app tests alembic`
- `python -m pytest -q`
- `DATABASE_URL=sqlite:////tmp/cliniccore-alembic.db alembic upgrade head`
