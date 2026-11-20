param([string]$ArchivePath)
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root "data"
$logoDir = Join-Path $root "app/static/uploads/clinic-logos"
$pidFile = Join-Path $dataDir "cliniccore.pid"
$python = Join-Path $root ".venv/Scripts/python.exe"

if (-not $ArchivePath) { $ArchivePath = Read-Host "Enter the full path of the ClinicCore backup ZIP" }
$ArchivePath = [System.IO.Path]::GetFullPath($ArchivePath)
if (-not (Test-Path -LiteralPath $ArchivePath -PathType Leaf)) { throw "Backup archive not found: $ArchivePath" }
if (Test-Path -LiteralPath $pidFile) { throw "ClinicCore has a PID file. Run stop.bat before restoring a backup." }
$listener = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($listener) { throw "Port 8000 is active. Stop ClinicCore before restoring a backup." }
if (-not (Test-Path -LiteralPath $python)) { throw "Project Python not found. Run setup.bat first." }

$databaseUrl = $env:DATABASE_URL
if (-not $databaseUrl) {
    $envLine = Get-Content -LiteralPath (Join-Path $root ".env") -ErrorAction SilentlyContinue | Where-Object { $_ -match "^DATABASE_URL=" } | Select-Object -First 1
    if ($envLine) { $databaseUrl = $envLine.Substring("DATABASE_URL=".Length).Trim().Trim([char]34, [char]39) }
}
if (-not $databaseUrl.StartsWith("sqlite:///")) { throw "Restore supports file-backed SQLite databases under the local data directory only." }
$databaseRelative = $databaseUrl.Substring("sqlite:///".Length)
if ($databaseRelative -eq ":memory:") { throw "In-memory SQLite cannot be restored." }
$databasePath = [System.IO.Path]::GetFullPath((Join-Path $root $databaseRelative))
$dataPrefix = [System.IO.Path]::GetFullPath($dataDir) + [System.IO.Path]::DirectorySeparatorChar
if (-not $databasePath.StartsWith($dataPrefix, [System.StringComparison]::OrdinalIgnoreCase)) { throw "The configured database is outside the data directory; refusing an incomplete restore." }
$relativeDatabasePath = $databasePath.Substring($dataPrefix.Length)

$stage = Join-Path $env:TEMP ("ClinicCoreRestore_" + [guid]::NewGuid().ToString("N"))
$oldData = Join-Path $root ("data.pre-restore_" + [guid]::NewGuid().ToString("N"))
$oldLogos = Join-Path $root ("clinic-logos.pre-restore_" + [guid]::NewGuid().ToString("N"))
$hadData = Test-Path -LiteralPath $dataDir
$hadLogos = Test-Path -LiteralPath $logoDir
$dataMoved = $false
$logosMoved = $false
try {
    Expand-Archive -LiteralPath $ArchivePath -DestinationPath $stage -Force
    $restoreData = Join-Path $stage "data"
    $restoreLogos = Join-Path $stage "clinic-logos"
    $restoreDatabase = Join-Path $restoreData $relativeDatabasePath
    if (-not (Test-Path -LiteralPath $restoreDatabase -PathType Leaf)) { throw "The selected backup does not contain the configured SQLite database." }

    $checkCode = "import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); r=c.execute('PRAGMA quick_check').fetchone()[0]; print(r); c.close(); sys.exit(0 if r == 'ok' else 1)"
    & $python -c $checkCode $restoreDatabase
    if ($LASTEXITCODE -ne 0) { throw "The backup database failed SQLite integrity validation." }

    if (Test-Path -LiteralPath $databasePath) { & (Join-Path $PSScriptRoot "backup_data.ps1") | Out-Null }
    if ($hadData) { Move-Item -LiteralPath $dataDir -Destination $oldData; $dataMoved = $true }
    if ($hadLogos) { Move-Item -LiteralPath $logoDir -Destination $oldLogos; $logosMoved = $true }

    New-Item -ItemType Directory -Force -Path $dataDir, $logoDir | Out-Null
    Get-ChildItem -LiteralPath $restoreData -Force | Copy-Item -Destination $dataDir -Recurse -Force
    if (Test-Path -LiteralPath $restoreLogos) {
        Get-ChildItem -LiteralPath $restoreLogos -Force | Copy-Item -Destination $logoDir -Recurse -Force
    }
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
    & $python -c $checkCode $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Restored database failed SQLite integrity validation." }

    if ($dataMoved) { Remove-Item -LiteralPath $oldData -Recurse -Force; $dataMoved = $false }
    if ($logosMoved) { Remove-Item -LiteralPath $oldLogos -Recurse -Force; $logosMoved = $false }
    Write-Host "ClinicCore data and clinic logos restored from: $ArchivePath"
    Write-Host "The current .env file was preserved. Start the application with start.bat."
} catch {
    if (Test-Path -LiteralPath $dataDir) { Remove-Item -LiteralPath $dataDir -Recurse -Force }
    if (Test-Path -LiteralPath $logoDir) { Remove-Item -LiteralPath $logoDir -Recurse -Force }
    if ($dataMoved -and (Test-Path -LiteralPath $oldData)) { Move-Item -LiteralPath $oldData -Destination $dataDir }
    if ($logosMoved -and (Test-Path -LiteralPath $oldLogos)) { Move-Item -LiteralPath $oldLogos -Destination $logoDir }
    throw
} finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}