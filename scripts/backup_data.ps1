$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root "data"
$logoDir = Join-Path $root "app/static/uploads/clinic-logos"
$pidFile = Join-Path $dataDir "cliniccore.pid"

if (Test-Path -LiteralPath $pidFile) { throw "ClinicCore has a PID file. Run stop.bat before creating a backup." }
$listener = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($listener) { throw "Port 8000 is active. Stop ClinicCore before creating a backup." }
if (-not (Test-Path -LiteralPath $dataDir)) { throw "The data directory does not exist." }

$databaseUrl = $env:DATABASE_URL
if (-not $databaseUrl) {
    $envLine = Get-Content -LiteralPath (Join-Path $root ".env") -ErrorAction SilentlyContinue | Where-Object { $_ -match "^DATABASE_URL=" } | Select-Object -First 1
    if ($envLine) { $databaseUrl = $envLine.Substring("DATABASE_URL=".Length).Trim().Trim([char]34, [char]39) }
}
if (-not $databaseUrl.StartsWith("sqlite:///")) { throw "Backup supports file-backed SQLite databases under the local data directory only." }
$databaseRelative = $databaseUrl.Substring("sqlite:///".Length)
if ($databaseRelative -eq ":memory:") { throw "In-memory SQLite cannot be backed up." }
$databasePath = [System.IO.Path]::GetFullPath((Join-Path $root $databaseRelative))
$dataPrefix = [System.IO.Path]::GetFullPath($dataDir) + [System.IO.Path]::DirectorySeparatorChar
if (-not $databasePath.StartsWith($dataPrefix, [System.StringComparison]::OrdinalIgnoreCase)) { throw "The configured database is outside the data directory; refusing an incomplete backup." }
if (-not (Test-Path -LiteralPath $databasePath)) { throw "Configured SQLite database was not found: $databasePath" }

$backupDir = Join-Path $root "backups"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
$archive = Join-Path $backupDir "ClinicCore_backup_$stamp.zip"
$stage = Join-Path $env:TEMP ("ClinicCoreBackup_" + [guid]::NewGuid().ToString("N"))
try {
    $stageData = Join-Path $stage "data"
    $stageLogos = Join-Path $stage "clinic-logos"
    New-Item -ItemType Directory -Force -Path $stageData, $stageLogos | Out-Null
    Get-ChildItem -LiteralPath $dataDir -Force | Copy-Item -Destination $stageData -Recurse -Force
    if (Test-Path -LiteralPath $logoDir) {
        Get-ChildItem -LiteralPath $logoDir -Force | Copy-Item -Destination $stageLogos -Recurse -Force
    }
    Compress-Archive -Path $stageData, $stageLogos -DestinationPath $archive -CompressionLevel Optimal -Force
    Write-Host "ClinicCore backup created: $archive"
} finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}