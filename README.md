# ClinicCore

ClinicCore is a lightweight, modular, Persian-first clinic management platform for small medical offices and healthcare centers.

## Stack

- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- Jinja2
- HTMX / Alpine.js ready
- Bootstrap RTL ready

## Current status

Sprint 1 created the base application structure, API shell, SQLAlchemy models, Alembic migration setup, Persian RTL home page, and initial tests.

## Quick start

See `HELP/INSTALL.txt` and `HELP/RUN.txt`.


## Database for the current development phase

ClinicCore currently uses a local SQLite database at `./data/cliniccore.db` by default. Set `DATABASE_URL=sqlite:///./data/cliniccore.db` in your local `.env` file. PostgreSQL support and its driver are intentionally disabled for this phase. Existing PostgreSQL test containers, volumes, and database files are not automatically deleted or modified; keep them untouched unless you separately decide to remove them.

## Branding and printing

Administrators can configure the displayed system title, primary UI color, clinic identity, and logo by uploading a PNG/JPEG/WebP file (up to 2 MB) or entering a logo path/URL. Messaging defaults and print layout are also available in **تنظیمات**. Print templates support A4, A5, and thermal receipt widths of 58 mm or 80 mm, configurable margins, institution header/footer, table borders, and a closing message. Browser and printer driver settings still determine final physical output, so check Print Preview before printing important documents.
