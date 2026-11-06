@echo off
setlocal
title ClinicCore - First Time Setup
cd /d "%~dp0"

echo ==========================================
echo ClinicCore - Windows Setup
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo Creating project virtual environment...
  py -3.12 -m venv .venv
  if errorlevel 1 (
    echo Python launcher could not find Python 3.12. Trying the default python...
    python -m venv .venv
    if errorlevel 1 (
      echo ERROR: Python 3.12 or newer is required.
      pause
      exit /b 1
    )
  )
)

".venv\Scripts\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)"
if errorlevel 1 (
  echo ERROR: The selected Python is older than 3.12. Install Python 3.12+ and remove only the incomplete .venv folder before retrying.
  pause
  exit /b 1
)

echo Installing Python dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pip install -e ".[dev]"
if errorlevel 1 goto :failed

echo Preparing local environment...
".venv\Scripts\python.exe" scripts\bootstrap_env.py
if errorlevel 1 goto :failed

echo Applying database migrations...
".venv\Scripts\python.exe" -m alembic upgrade head
if errorlevel 1 (
  echo ERROR: Migration failed. Existing database files have not been deleted.
  goto :failed
)

echo Creating the initial administrator if one does not already exist...
".venv\Scripts\python.exe" scripts\seed_admin.py
if errorlevel 1 goto :failed

echo.
echo Setup completed.
echo Run start.bat to launch ClinicCore.
echo Keep the generated administrator password shown above in a safe place.
pause
exit /b 0

:failed
echo.
echo Setup did not complete. Review the error above; do not delete your data folder.
pause
exit /b 1
