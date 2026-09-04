# Vageesh's setup and submission checklist

## 1. Back up the current repository

From the parent directory of your existing project:

```powershell
Copy-Item -Recurse `
  "Bhagavad-Gita-AI-Wisdom-from-Kurukshetra" `
  "Bhagavad-Gita-AI-backup"
```

## 2. Copy this cleaned project over the existing repository

Keep the existing `.git` folder so your genuine commit history remains intact. Copy all
files from this package **except any `.git` folder** into your current repository and
allow Windows to replace matching files.

Old image and text files that are no longer imported may be removed in the same cleanup
commit after confirming the new version works.

## 3. Create and activate the environment

```powershell
cd Bhagavad-Gita-AI-Wisdom-from-Kurukshetra
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup_windows.ps1
```

Open `.env` and replace the placeholder with your actual Groq key. Never show or commit
this file.

## 4. Run the application

```powershell
.\scripts\run_windows.ps1
```

Test these questions:

1. `What does the Gita teach about focusing on action rather than results?`
2. `How can I apply this before a software engineering interview?`

Expand the retrieved-passages panel and confirm Bhagavad Gita 2.47 or 2.48 appears.

## 5. Verify before committing

```powershell
.\.venv\Scripts\python.exe -m compileall -q app.py answer_bot.py core tests
.\.venv\Scripts\python.exe -m pytest

git status
git diff --stat
```

Confirm `.env` does not appear in `git status`.

## 6. Commit the genuine upgrade

A suitable commit message is:

```powershell
git add .
git commit -m "refactor: modularize RAG pipeline and add retrieval tests"
git push origin main
```

Do not manufacture extra commits. One well-scoped, honest refactor commit is enough.

## 7. Loom preparation

- Start the app and ask one warm-up question before recording so the embedding model and
  FAISS index are cached.
- Keep the app, `core/rag_service.py`, `core/prompts.py`, README architecture, tests, and
  GitHub commits open in separate tabs.
- Hide `.env`, terminal command history, notifications, email, and API dashboards.
- Use the two tested questions above.
- Keep the final recording below five minutes.
