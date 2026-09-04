param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

$ErrorActionPreference = "Stop"

$RepoPath = [System.IO.Path]::GetFullPath($RepoPath)
$PackageRoot = Split-Path -Parent $PSScriptRoot
$RepoName = Split-Path -Leaf $RepoPath
$RepoParent = Split-Path -Parent $RepoPath
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupRoot = Join-Path $RepoParent "$RepoName-krishna-voice-backup-$Timestamp"
$Python = Join-Path $RepoPath ".venv\Scripts\python.exe"

if (-not (Test-Path $RepoPath -PathType Container)) {
    throw "Repository folder not found: $RepoPath"
}

if (-not (Test-Path (Join-Path $RepoPath ".git") -PathType Container)) {
    throw "The target folder is not the expected Git repository: $RepoPath"
}

if (-not (Test-Path $Python -PathType Leaf)) {
    throw "Virtual environment Python was not found: $Python`nRun the project setup first."
}

$RelativeFiles = @(
    "app.py",
    "core\styles.py",
    "core\voice_experience.py",
    "assets\krishna_divine.webp",
    "assets\krishna_icon.webp",
    "tests\test_voice_experience.py",
    "KRISHNA_VOICE_FEATURE.md"
)

$PreviouslyExisted = @{}
New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null

Write-Host "Creating frontend backup at:" -ForegroundColor Cyan
Write-Host $BackupRoot -ForegroundColor DarkCyan

foreach ($RelativeFile in $RelativeFiles) {
    $Source = Join-Path $PackageRoot $RelativeFile
    $Destination = Join-Path $RepoPath $RelativeFile

    if (-not (Test-Path $Source -PathType Leaf)) {
        throw "Update package is incomplete. Missing: $Source"
    }

    $PreviouslyExisted[$RelativeFile] = Test-Path $Destination -PathType Leaf

    if ($PreviouslyExisted[$RelativeFile]) {
        $BackupFile = Join-Path $BackupRoot $RelativeFile
        $BackupDirectory = Split-Path -Parent $BackupFile
        New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
        Copy-Item -LiteralPath $Destination -Destination $BackupFile -Force
    }

    $DestinationDirectory = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Path $DestinationDirectory -Force | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    Write-Host "Applied: $RelativeFile" -ForegroundColor Green
}

try {
    Push-Location $RepoPath

    Write-Host "Checking Python syntax..." -ForegroundColor Cyan
    & $Python -m compileall -q app.py core tests
    if ($LASTEXITCODE -ne 0) {
        throw "Python compilation failed."
    }

    Write-Host "Running the complete test suite..." -ForegroundColor Cyan
    & $Python -m pytest
    if ($LASTEXITCODE -ne 0) {
        throw "One or more tests failed."
    }

    Write-Host ""
    Write-Host "SHRI KRISHNA VOICE UI APPLIED SUCCESSFULLY" -ForegroundColor Green
    Write-Host "Your Groq model configuration and .env file were not changed." -ForegroundColor Yellow

    $ConfigPath = Join-Path $RepoPath "core\config.py"
    $ConfigText = Get-Content -LiteralPath $ConfigPath -Raw
    if ($ConfigText -match "llama-3\.3-70b-versatile|llama-3\.1-8b-instant") {
        Write-Warning "core\config.py still contains a Groq model ID that may be unavailable. Keep your earlier openai/gpt-oss model fix before recording."
    }

    Write-Host "Launch with: .\.venv\Scripts\python.exe -m streamlit run app.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Current Git changes:" -ForegroundColor Cyan
    git status --short
}
catch {
    Write-Host "Validation failed. Restoring the previous frontend..." -ForegroundColor Red

    foreach ($RelativeFile in $RelativeFiles) {
        $Destination = Join-Path $RepoPath $RelativeFile
        if ($PreviouslyExisted[$RelativeFile]) {
            $BackupFile = Join-Path $BackupRoot $RelativeFile
            $DestinationDirectory = Split-Path -Parent $Destination
            New-Item -ItemType Directory -Path $DestinationDirectory -Force | Out-Null
            Copy-Item -LiteralPath $BackupFile -Destination $Destination -Force
        }
        elseif (Test-Path $Destination -PathType Leaf) {
            Remove-Item -LiteralPath $Destination -Force
        }
    }

    throw
}
finally {
    Pop-Location
}
