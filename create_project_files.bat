@echo off

echo Creating ClinicCore base files...

(
echo # ClinicCore
echo.
echo Lightweight modular Persian-first Clinic Management Platform.
echo.
echo ## Technology
echo.
echo - FastAPI
echo - SQLAlchemy 2
echo - PostgreSQL
echo - Jinja2
echo - HTMX
echo - Alpine.js
echo - Bootstrap RTL
echo.
echo ## Status
echo.
echo Under Development
) > README.md


(
echo # AGENTS.md
echo.
echo Permanent instructions for AI coding agents.
echo.
echo ## Mission
echo Build ClinicCore as a lightweight modular clinic management platform.
echo.
echo ## Rules
echo - Prefer simplicity
echo - Keep architecture clean
echo - Use FastAPI
echo - Use SQLAlchemy 2
echo - Use PostgreSQL
echo - Use Jinja2 HTMX
echo - Keep documentation updated
echo - Create small commits
echo - Avoid unnecessary complexity
echo.
echo ## Documentation
echo Maintain HELP folder with installation and architecture documents.
) > AGENTS.md


(
echo # Python
echo __pycache__/
echo *.py[cod]
echo.
echo # Virtual Environment
echo .venv/
echo venv/
echo env/
echo.
echo # Environment
echo .env
echo.
echo # IDE
echo .vscode/
echo .idea/
echo.
echo # Database
echo *.sqlite3
echo *.db
echo.
echo # Logs
echo *.log
) > .gitignore


mkdir HELP 2>nul

echo.
echo Files created successfully.
echo.
dir

pause