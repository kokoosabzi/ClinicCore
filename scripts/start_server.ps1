$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"
$dataDir = Join-Path $root "data"
$pidFile = Join-Path $dataDir "cliniccore.pid"

if (-not (Test-Path -LiteralPath $python)) { throw "Project Python not found. Run setup.bat first." }
if (-not (Test-Path -LiteralPath (Join-Path $root ".env"))) { throw ".env not found. Run setup.bat first." }
New-Item -ItemType Directory -Force -Path $dataDir | Out-Null

if (Test-Path -LiteralPath $pidFile) {
    $oldPidText = (Get-Content -LiteralPath $pidFile -Raw).Trim()
    $oldPid = 0
    if ([int]::TryParse($oldPidText, [ref]$oldPid)) {
        $old = Get-CimInstance Win32_Process -Filter "ProcessId = $oldPid" -ErrorAction SilentlyContinue
        if ($null -ne $old) {
            if (($old.ExecutablePath -ieq $python) -and ($old.CommandLine -like "*uvicorn app.main:app*")) {
                Write-Host "ClinicCore is already running (PID $oldPid) at http://127.0.0.1:8000"
                exit 0
            }
            throw "The saved PID belongs to another process. No process was stopped; inspect data\cliniccore.pid."
        }
    }
    Remove-Item -LiteralPath $pidFile -Force
}

$listener = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($null -ne $listener) {
    throw "Port 8000 is already in use by another process. No process was stopped."
}

$arguments = @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000")
$process = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -PassThru -WindowStyle Hidden
Set-Content -LiteralPath $pidFile -Value $process.Id -Encoding ascii

$healthy = $false
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Seconds 1
    $process.Refresh()
    if ($process.HasExited) {
        Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
        throw "ClinicCore exited during startup. Check the application logs/console output."
    }
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) { $healthy = $true; break }
    } catch {
        # Continue polling while the ASGI application initializes.
    }
}

if (-not $healthy) {
    Write-Warning "The server process is running, but the health endpoint did not respond within 20 seconds."
    Write-Host "Use stop.bat to stop the tracked process."
    exit 1
}

Write-Host "ClinicCore is running at http://127.0.0.1:8000 (PID $($process.Id))."
