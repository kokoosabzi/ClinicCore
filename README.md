# ClinicCore

ClinicCore is a Persian-first clinic management application for small medical offices and healthcare centers.

## Technology

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- Alembic
- SQLite (local, file-backed)
- Jinja2, HTMX and Alpine.js
- Persian RTL interface and Jalali date presentation

## Windows quick start

1. Install **Python 3.12 or newer** and Git.
2. Clone this repository and open its folder.
3. Run `setup.bat` once. It creates `.venv`, installs dependencies, creates a private local `.env` for a fresh installation, applies database migrations, and creates the initial administrator.
4. Run `start.bat` to start the local application.
5. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).
6. Use `stop.bat` to stop the server started by this launcher.

The first-run administrator password is generated randomly and printed once by setup. The account requires a password change on first login. Keep the password safe.

Detailed instructions: [HELP/INSTALL.txt](HELP/INSTALL.txt), [HELP/RUN.txt](HELP/RUN.txt), and [HELP/AUTHENTICATION.txt](HELP/AUTHENTICATION.txt).

## Database and data safety

The current application configuration supports **SQLite only**. The default database is `data/cliniccore.db`. The application creates the data directory when needed. Database schema changes are managed by Alembic.

The setup and launch scripts do not delete or replace an existing database. They do not stop Docker containers, remove volumes, or modify PostgreSQL data. If an existing `.env` points to a non-SQLite database, setup will fail safely; review that configuration deliberately rather than overwriting it.

Back up the `data` directory while the application is stopped. Do not commit `.env`, database files, uploaded logos, or credentials.

## Current scope

ClinicCore includes authentication, user roles, patient records, appointment booking, financial records, messaging foundations, settings, and printable views. The role model currently includes administrator, doctor, secretary, and accountant. Detailed permission granularity and full user administration remain planned work.

## Development

```powershell
python -m compileall app tests main.py alembic scripts
python -m pytest -q
python -m alembic upgrade head
```

Run these commands from the repository root with the virtual environment activated. A successful automated test run does not replace a Windows browser smoke test of setup, login, core workflows, persistence, printing, and shutdown.
