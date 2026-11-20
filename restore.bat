@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\restore_data.ps1"
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\restore_data.ps1" -ArchivePath "%~1"
)
if errorlevel 1 (
  echo Restore failed. Existing data was preserved when validation failed before replacement.
  if not defined CI pause
  exit /b 1
)
if not defined CI pause
exit /b 0
