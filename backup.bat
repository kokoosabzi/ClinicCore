@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\backup_data.ps1"
if errorlevel 1 (
  echo Backup failed. Review the error above.
  if not defined CI pause
  exit /b 1
)
if not defined CI pause
exit /b 0
