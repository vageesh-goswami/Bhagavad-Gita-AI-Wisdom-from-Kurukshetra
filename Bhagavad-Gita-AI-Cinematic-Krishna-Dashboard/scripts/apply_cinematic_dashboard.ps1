param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent $PSScriptRoot
$RepoPath = (Resolve-Path $RepoPath).Path

if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    throw "The target is not the existing Git repository: $RepoPath"
}

$requiredPackageFiles = @(
    "app.py",
    "core\styles.py",
    "core\voice_experience.py",
    "assets\krishna_dashboard.webp",
    "assets\krishna_symbols.webp",
    "assets\krishna_icon.webp",
    "tests\test_voice_experience.py",
    "CINEMATIC_DASHBOARD.md"
)

foreach ($relative in $requiredPackageFiles) {
    $source = Join-Path $PackageRoot $relative
    if (-not (Test-Path $source)) {
        throw "Update package is incomplete. Missing: $source"
    }
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$parent = Split-Path -Parent $RepoPath
$name = Split-Path -Leaf $RepoPath
$backup = Join-Path $parent "$name-cinematic-backup-$timestamp"
New-Item -ItemType Directory -Path $backup -Force | Out-Null

$targets = @(
    "app.py",
    "core\styles.py",
    "core\voice_experience.py",
    "assets\krishna_dashboard.webp",
    "assets\krishna_symbols.webp",
    "assets\krishna_icon.webp",
    "tests\test_voice_experience.py",
    "CINEMATIC_DASHBOARD.md"
)

Write-Host "Backing up current interface to:" -ForegroundColor Cyan
Write-Host $backup -ForegroundColor Yellow

foreach ($relative in $targets) {
    $existing = Join-Path $RepoPath $relative
    if (Test-Path $existing) {
        $backupTarget = Join-Path $backup $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $backupTarget) -Force | Out-Null
        Copy-Item -LiteralPath $existing -Destination $backupTarget -Force
    }
}

try {
    foreach ($relative in $targets) {
        $source = Join-Path $PackageRoot $relative
        $destination = Join-Path $RepoPath $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $destination -Force
    }

    $venvPython = Join-Path $RepoPath ".venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        throw "Virtual environment not found: $venvPython"
    }

    Push-Location $RepoPath
    try {
        Write-Host "Compiling the updated interface..." -ForegroundColor Cyan
        & $venvPython -m compileall -q app.py core tests
        if ($LASTEXITCODE -ne 0) { throw "Python compilation failed." }

        Write-Host "Running all tests..." -ForegroundColor Cyan
        & $venvPython -m pytest -q
        if ($LASTEXITCODE -ne 0) { throw "One or more tests failed." }
    }
    finally {
        Pop-Location
    }
}
catch {
    Write-Host "Validation failed. Restoring files from backup..." -ForegroundColor Red
    foreach ($relative in $targets) {
        $backedUp = Join-Path $backup $relative
        $destination = Join-Path $RepoPath $relative
        if (Test-Path $backedUp) {
            New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
            Copy-Item -LiteralPath $backedUp -Destination $destination -Force
        }
        elseif (Test-Path $destination) {
            Remove-Item -LiteralPath $destination -Force
        }
    }
    throw
}

Write-Host "" 
Write-Host "CINEMATIC SHRI KRISHNA DASHBOARD APPLIED SUCCESSFULLY" -ForegroundColor Green
Write-Host "Run:" -ForegroundColor Cyan
Write-Host "  cd `"$RepoPath`"" -ForegroundColor White
Write-Host "  .\.venv\Scripts\python.exe -m streamlit run app.py" -ForegroundColor White
Write-Host "Then press Ctrl + F5 in Chrome or Edge." -ForegroundColor Yellow
