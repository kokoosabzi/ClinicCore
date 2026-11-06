@echo off
setlocal
title ClinicCore - Stop
cd /d "%~dp0"

if not exist "scripts\stop_server.ps1" (
  echo Missing stop script. Nothing was stopped.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\stop_server.ps1"
if errorlevel 1 (
  echo ClinicCore could not be stopped automatically. Review the message above.
  pause
  exit /b 1
)
endlocal
