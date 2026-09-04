param(
    [string]$RepoPath = (Join-Path ([Environment]::GetFolderPath("Desktop")) "Bhagavad-Gita-AI-Wisdom-from-Kurukshetra")
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot

if (-not (Test-Path $RepoPath)) {
    throw "Repository not found: $RepoPath"
}
if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    throw "The target is not the expected Git repository: $RepoPath"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$repoParent = Split-Path -Parent $RepoPath
$repoName = Split-Path -Leaf $RepoPath
$backupRoot = Join-Path $repoParent "$repoName-frontend-backup-$timestamp"
New-Item -ItemType Directory -Path (Join-Path $backupRoot "core") -Force | Out-Null

Copy-Item (Join-Path $RepoPath "app.py") (Join-Path $backupRoot "app.py") -Force
Copy-Item (Join-Path $RepoPath "core\styles.py") (Join-Path $backupRoot "core\styles.py") -Force

Copy-Item (Join-Path $packageRoot "app.py") (Join-Path $RepoPath "app.py") -Force
Copy-Item (Join-Path $packageRoot "core\styles.py") (Join-Path $RepoPath "core\styles.py") -Force

Write-Host "Divine frontend applied successfully." -ForegroundColor Green
Write-Host "Backup created at: $backupRoot" -ForegroundColor Yellow

$pythonPath = Join-Path $RepoPath ".venv\Scripts\python.exe"
if (Test-Path $pythonPath) {
    Push-Location $RepoPath
    try {
        & $pythonPath -m compileall -q app.py core
        if ($LASTEXITCODE -ne 0) { throw "Python compilation failed." }
        & $pythonPath -m pytest
        if ($LASTEXITCODE -ne 0) { throw "Tests failed." }
        Write-Host "Compilation and tests passed." -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "No .venv found; skipped automated compilation and tests." -ForegroundColor Yellow
}
