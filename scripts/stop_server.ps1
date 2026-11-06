$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"
$pidFile = Join-Path (Join-Path $root "data") "cliniccore.pid"

if (-not (Test-Path -LiteralPath $pidFile)) {
    Write-Host "No ClinicCore PID file found; nothing to stop."
    exit 0
}

$pidText = (Get-Content -LiteralPath $pidFile -Raw).Trim()
$clinicPid = 0
if (-not [int]::TryParse($pidText, [ref]$clinicPid)) {
    throw "Invalid PID file. No process was stopped; inspect data\cliniccore.pid."
}

$processInfo = Get-CimInstance Win32_Process -Filter "ProcessId = $clinicPid" -ErrorAction SilentlyContinue
if ($null -eq $processInfo) {
    Remove-Item -LiteralPath $pidFile -Force
    Write-Host "The recorded process has already exited. Removed stale PID file."
    exit 0
}

if (($processInfo.ExecutablePath -ine $python) -or ($processInfo.CommandLine -notlike "*uvicorn app.main:app*")) {
    throw "The saved PID does not identify the ClinicCore server. No process was stopped."
}

Stop-Process -Id $clinicPid -ErrorAction Stop
try {
    Wait-Process -Id $clinicPid -Timeout 10 -ErrorAction Stop
} catch {
    # Verify below rather than assuming a timeout means the process exited.
}
$stillRunning = Get-CimInstance Win32_Process -Filter "ProcessId = $clinicPid" -ErrorAction SilentlyContinue
if ($null -ne $stillRunning) {
    throw "ClinicCore process did not exit. PID file was retained so stop can be retried."
}
Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
Write-Host "ClinicCore process $clinicPid stopped."
