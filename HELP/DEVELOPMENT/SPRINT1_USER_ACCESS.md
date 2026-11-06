# Sprint 1 — User Administration & Role-Based Access Control

## Status

Design baseline for implementation. This branch is intentionally based on the unmerged Sprint 0 branch `stabilization/windows-sqlite-runtime`; it must not be merged into `main` independently of its prerequisite. Sprint 0 hosted Windows CI is green, while manual acceptance on the target Windows PC remains outstanding.

## 1. Goals

- Provide a usable Persian RTL user administration screen.
- Support create, list, edit, deactivate/reactivate, and administrator-assisted password reset.
- Enforce permissions on the server for every protected route; hiding navigation links is not authorization.
- Keep authentication/session behavior simple and suitable for a single-clinic local Windows deployment.
- Preserve existing users and password hashes through additive Alembic migrations.

## 2. Role model

The initial built-in roles are:

| Role key | Persian label | Purpose |
|---|---|---|
| `admin` | مدیر سیستم | Full access, user and permission administration |
| `clinic_manager` | مدیر کلینیک | Operational oversight; no system-owner escalation |
| `doctor` | پزشک | Patient and appointment workflow |
| `secretary` | پذیرش | Patient registration and appointment workflow |
| `accountant` | حسابدار | Financial workflow and financial reports |

Existing `secretary` and `accountant` users remain valid. Existing `admin` and `doctor` users keep their roles. The legacy role value `secretary` remains the canonical role key; no bulk user conversion is required.

## 3. Permission vocabulary

Permissions are domain/action pairs, checked on the server:

- `users.view`, `users.create`, `users.update`, `users.deactivate`, `users.reset_password`, `users.assign_role`
- `patients.view`, `patients.create`, `patients.update`, `patients.archive`
- `appointments.view`, `appointments.create`, `appointments.update`, `appointments.cancel`
- `financial.view`, `financial.create`, `financial.update`, `financial.void`
- `messaging.view`, `messaging.create`
- `reports.view`, `reports.financial`
- `settings.view`, `settings.update`
- `audit.view`

## 4. Initial default role matrix

- **admin:** all permissions.
- **clinic_manager:** all operational patient, appointment, financial, messaging, reporting, settings-view and audit-view permissions; can manage ordinary staff accounts, but cannot create/promote another system administrator or change the permission matrix.
- **doctor:** patient view/create/update; appointment view/create/update/cancel; messaging view/create.
- **secretary:** patient view/create/update; appointment view/create/update/cancel; messaging view/create.
- **accountant:** patient view (minimum identity needed for billing); financial view/create/update; financial reports.

These are least-privilege starting defaults. The system administrator can adjust permissions for built-in non-admin roles in the role-permission screen. The `admin` role remains immutable and always retains all permissions.

## 5. Data and migration approach

- Keep the existing `users` table and password hashes.
- Add normalized `roles` and `permissions` / role-permission mapping tables using additive Alembic migrations.
- Add `clinic_manager` as a supported role without rewriting existing user rows.
- Seed built-in roles and permission grants idempotently.
- Do not create tables from application startup or seed scripts; Alembic remains the only schema source of truth.
- Do not delete, replace, or reset the existing SQLite database.

## 6. Security and behavior rules

- All permission checks are server-side dependencies/service checks.
- A user with `must_change_password=True` may only access logout and the password-change flow until the password is changed.
- Deactivated/soft-deleted users cannot authenticate; changing a user's role or deactivating them invalidates their next authenticated request/session.
- Never expose password hashes or plaintext passwords in list/detail responses or audit logs.
- Admin reset creates a one-time temporary password, stores only its hash, and sets `must_change_password=True`; show the temporary password only once.
- Prevent self-deactivation and prevent deactivation/demotion of the last active system administrator.
- All state-changing browser forms require CSRF validation.
- Audit user creation, role changes, deactivation/reactivation and password resets without logging secrets.
- Existing session values are not treated as the sole authority for permissions; resolve the current active user and permissions from the database for protected requests.

## 7. UI

- Add a Users page linked only for principals with `users.view`.
- Provide searchable user list, status, role, last update and actions.
- Add create/edit form with role selection constrained by the actor's permissions.
- Add activate/deactivate and reset-password confirmation flows.
- Add a role-permission matrix visible only to the system administrator.
- Use the existing base layout, RTL styling, CSRF token pattern and form conventions.

## 8. Acceptance tests

- Existing users can still log in after migration.
- Existing password hashes are not rewritten by migration.
- New users can be created with hashed passwords and assigned built-in roles.
- Duplicate usernames are rejected with a safe user-facing error.
- Inactive users cannot log in.
- Role changes take effect without requiring a server restart.
- Every protected API and HTML route rejects insufficient permissions (403) and unauthenticated requests (401/redirect as appropriate).
- Users cannot grant permissions they do not possess.
- Only system admin can edit the permission matrix or assign the `admin` role.
- Clinic manager cannot promote a user to system admin.
- A forced-password-change user cannot navigate to dashboard or domain pages before changing password.
- Last active administrator cannot be deactivated or demoted.
- CSRF is enforced on all mutating browser forms.
- Passwords and hashes never appear in responses, audit details or rendered HTML.
- Full Windows CI (compileall, pytest, clean Alembic migration) passes.

## 9. Delivery sequence

1. Add permission catalog, role-permission model and additive migration; seed defaults.
2. Resolve active user from database and add reusable `require_permission` dependencies.
3. Protect existing HTML/API routes with the permission matrix.
4. Complete user CRUD service and API validation.
5. Add Persian RTL user administration UI and password reset workflow.
6. Add role-permission UI and comprehensive authorization tests.
7. Run CI and review migration compatibility; keep PR dependent on Sprint 0 until manual Windows acceptance is recorded.

## 10. Explicit non-goals

No MFA, external identity provider, network/SSO deployment, advanced intrusion detection, or complex policy language in this sprint. This is a local single-clinic application with straightforward role-based access control.
