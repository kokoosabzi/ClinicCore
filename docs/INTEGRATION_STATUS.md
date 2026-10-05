# Repository Integration Status

## Scope and repository identity

The working copy identifies itself as **ClinicCore**, not BonyanCore. On 2026-10-02 it had no configured Git remote, no remote-tracking branches, and one reachable local branch before this integration branch was created. Consequently the requested GitHub branches and commit objects cannot be inspected or merged from this clone.

## Branch report

| Branch/reference requested or found | HEAD / status | Unique feature assessment | Decision |
|---|---|---|---|
| `work` | `0b73724` — `fix(alembic): read database url from app settings` | Contains the ClinicCore baseline, A1 isolated DB fixture, and A2 Alembic configuration fix. | Preserved as the integration base. |
| `integration/bonyancore-unified` | Created from `work` | Adds A3 appointment booking integrity. | Active unified branch. |
| `main` | Not present locally or remotely | Cannot compare. | Not merged. |
| `feature/bonyancore-current` | Not present; supplied object unavailable | Cannot compare. | Not merged. |
| `bonyancore-final-integration` | Not present; supplied object unavailable | Cannot compare. | Not merged. |
| `bonyancore-final-v1`, `bonyancore-financial-integration`, `feature/latest-changes`, `codex`, `codex-q4wbh1` | Not present locally or remotely | Cannot compare. | Not merged. |

The supplied BonyanCore hashes `4a70f078e1e418ba3b92cc17d31bf580bc9ef6cf`, `c384ddd40cac0d7a22ab20b252e5c60955577b4d`, and `11c022d8f59e982c8c07e3abae6530a1b8a3d7be` are not objects in this repository.

## Merge/conflict report

No Git merge was possible: no remote exists and no named BonyanCore references or objects are available. No `ours`/`theirs` conflict resolution was used. No files named `journal_entry.py`, `bulk_import.py`, `pages1.py`, Jalali schemas/utilities, or their listed templates exist in this checkout; repository-wide searches found no imports or route registrations for them.

## Consolidated changes on the unified branch

| Feature | Files | Conflict/decision | Test/status |
|---|---|---|---|
| Alembic database URL configuration | `alembic/env.py`, `alembic.ini` from base | Preserved from `work`. | Previously verified; clean SQLite migration chain rechecked. |
| Appointment slot integrity | appointment model/repository/service/routers, revision `20261002_0004`, tests | HTML-only validation was incomplete because the API bypassed it. A single service rule plus a partial unique index preserves soft-delete behavior and handles concurrent inserts. | Compile and SQLite migration pass; full pytest environment-blocked. |

## Architecture review

- **Present:** patient, appointment, simple payment/expense, messaging provider shell, user/authentication, CSRF, audit log, Alembic migrations, Persian RTL templates.
- **Absent:** journal entry/accounting ledger, chart of accounts, receipts linked to journal postings, BonyanCore business entities, bulk Excel import, Jalali conversion pipeline, and the named BonyanCore modules.
- **Migration state:** one Alembic head (`20261002_0004`) and a successful clean SQLite upgrade. PostgreSQL application remains unverified.

## Remaining risks and next phase

1. Obtain the intended BonyanCore remote or a clone containing its refs before claiming a cross-repository merge is complete.
2. Verify Alembic upgrades against PostgreSQL and resolve any existing duplicate active appointment slots before applying revision `20261002_0004`.
3. Restore/install test dependency `httpx` in the execution environment and run the complete suite.
4. Complete ClinicCore Phase A4: document and warn about the default administrator credentials. This is the single recommended next task.
