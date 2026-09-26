@echo off
setlocal
title ClinicCore - Local Launcher
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  py -3.12 -m venv venv
  if errorlevel 1 (echo Python 3.12 is required.& pause& exit /b 1)
)

call "venv\Scripts\activate.bat"
echo Installing project dependencies...
python -m pip install --upgrade pip
pip install -e ".[dev]"
if errorlevel 1 (pause& exit /b 1)

echo Applying database migrations...
alembic upgrade head
if errorlevel 1 (
  echo Migration failed. Make sure PostgreSQL is running and .env is configured.
  pause
  exit /b 1
)

echo Creating default admin if needed...
python scripts\seed_admin.py

echo Starting API...
echo API:     http://127.0.0.1:8000/
echo Swagger: http://127.0.0.1:8000/docs
echo Health:  http://127.0.0.1:8000/health
echo Default admin: admin / admin
echo.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
endlocal