@echo off
setlocal
title ClinicCore - Start
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo ClinicCore is not installed. Run setup.bat first.
  pause
  exit /b 1
)
if not exist ".env" (
  echo Missing .env. Run setup.bat first.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)"
if errorlevel 1 (
  echo Python 3.12 or newer is required. Re-run setup with a supported Python.
  pause
  exit /b 1
)

echo Checking database migrations...
".venv\Scripts\python.exe" -m alembic upgrade head
if errorlevel 1 (
  echo Database migration failed. No database files were deleted.
  pause
  exit /b 1
)

echo Starting ClinicCore on http://127.0.0.1:8000 ...
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\start_server.ps1"
if errorlevel 1 (
  echo ClinicCore could not be started. Review the message above.
  pause
  exit /b 1
)
echo ClinicCore launcher completed.
endlocal
