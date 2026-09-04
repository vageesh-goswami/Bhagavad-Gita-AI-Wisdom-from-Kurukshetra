# Divine Frontend Update

This package changes only:

- `app.py`
- `core/styles.py`

It does not overwrite model configuration, API keys, retrieval code, tests, or data.
The included PowerShell installer creates a timestamped backup of the existing frontend
files before applying the update.

## Apply on Windows

From the extracted package folder:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\apply_divine_frontend.ps1
```

Then launch the project from the repository:

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\Bhagavad-Gita-AI-Wisdom-from-Kurukshetra"
.\.venv\Scripts\python.exe -m streamlit run app.py
```
