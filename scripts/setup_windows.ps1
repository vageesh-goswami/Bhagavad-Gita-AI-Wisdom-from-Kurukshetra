$ErrorActionPreference = "Stop"

Write-Host "Creating Python 3.11 virtual environment..." -ForegroundColor Cyan
py -3.11 -m venv .venv

Write-Host "Upgrading pip..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host "Installing application and test dependencies..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env. Add your Groq API key before running cloud mode." -ForegroundColor Yellow
}

Write-Host "Running fast verification..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m compileall -q app.py answer_bot.py core tests
.\.venv\Scripts\python.exe -m pytest

Write-Host "Setup complete. Run: .\scripts\run_windows.ps1" -ForegroundColor Green
