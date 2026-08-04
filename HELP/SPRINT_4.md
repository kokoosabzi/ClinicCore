# Sprint 4 - Priority System Completion

## Goal
Complete the highest-priority development items: synchronized runbooks, developer environment files, protected routes, CSRF for UI forms, patient management pages, appointment listing, finance/message listing, and a provider-based messaging stub.

## Tasks
- Add `.env.example`, `docker-compose.yml`, and `Makefile`.
- Add CSRF helpers and tokens to UI form workflows.
- Protect HTML and JSON workflows with session/RBAC dependencies.
- Add patient list, search, detail, edit, and soft-delete pages.
- Add appointment, finance, and messaging index pages.
- Add console messaging provider and send-pending service routine.
- Add admin password change helper script.

## Database changes
No migration is required. Existing tables support these workflows.

## Risks
- Production must replace default admin credentials and `SECRET_KEY`.
- Console messaging provider is a local development implementation only.

## Test plan
- `make compile`
- `make test`
- `docker compose up -d postgres`
- `make migrate`
- `make seed`
- `make run`
