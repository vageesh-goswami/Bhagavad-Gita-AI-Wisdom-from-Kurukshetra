# Apply the Cinematic Shri Krishna Dashboard

This update preserves the existing RAG backend, `.env`, API key, knowledge base, and
model configuration. It replaces only the interface and adds the Hindi voice console.

## Windows PowerShell

```powershell
$repo = "C:\Users\vagee\OneDrive\Attachments\Desktop\Bhagavad-Gita-AI-Wisdom-from-Kurukshetra"
$zip = Join-Path "$HOME\Downloads" "Bhagavad-Gita-AI-Cinematic-Krishna-Dashboard.zip"
$extract = Join-Path "$HOME\Downloads" "Bhagavad-Gita-AI-Cinematic-Krishna-Dashboard-package"

if (Test-Path $extract) { Remove-Item $extract -Recurse -Force }
Expand-Archive -LiteralPath $zip -DestinationPath $extract -Force

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
& "$extract\Bhagavad-Gita-AI-Cinematic-Krishna-Dashboard\scripts\apply_cinematic_dashboard.ps1" -RepoPath $repo
```

Expected test result: `16 passed`.

Launch:

```powershell
cd $repo
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501` and press `Ctrl + F5`.
