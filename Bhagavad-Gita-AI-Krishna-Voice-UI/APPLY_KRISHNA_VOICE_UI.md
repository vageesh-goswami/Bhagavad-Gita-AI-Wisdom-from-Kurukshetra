# Apply the Shri Krishna Vāṇī Frontend

This is a focused update for the existing Bhagavad Gita AI repository. It preserves your `.git` history, `.env`, Groq model configuration, RAG service, FAISS knowledge base, and existing tests.

## What it adds

- Tap the Krishna portrait to expand a large divine avatar.
- Avatar artwork includes Sheshnag, Sudarshan Chakra, Shankha, Gada, and Padma.
- The first tap starts Hindi narration immediately.
- After a generated answer, only the **Hindi Explanation** section is spoken.
- Pause, resume, replay, stop, close, and speed controls.
- Animated aura and voice waveform while narration is playing.
- Hindi voice uses the browser's Web Speech API, so no second API key is required.
- Five additional unit tests for Hindi extraction and speech-text cleanup.

## 1. Stop the application

In the PowerShell window running Streamlit, press:

```text
Ctrl + C
```

## 2. Extract this ZIP

Use Windows **Extract All**. The extracted folder should be similar to:

```text
C:\Users\vagee\Downloads\Bhagavad-Gita-AI-Krishna-Voice-UI
```

## 3. Apply the update

Open PowerShell and run:

```powershell
$repo = "C:\Users\vagee\OneDrive\Attachments\Desktop\Bhagavad-Gita-AI-Wisdom-from-Kurukshetra"
$update = "$HOME\Downloads\Bhagavad-Gita-AI-Krishna-Voice-UI"

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

& "$update\scripts\apply_krishna_voice_ui.ps1" `
    -RepoPath $repo
```

The script creates a timestamped backup, applies the files, compiles the project, and runs the complete test suite. When validation fails, it restores the previous frontend automatically.

Expected ending:

```text
SHRI KRISHNA VOICE UI APPLIED SUCCESSFULLY
```

The test total should increase from 11 to 16.

## 4. Launch

```powershell
cd $repo
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

Use `Ctrl + F5` once so the browser does not reuse old CSS.

## 5. Test the experience

Before asking a question, tap **श्रीकृष्ण को सुनें**. The avatar should expand and speak a Hindi welcome.

Then ask:

```text
फल की चिंता छोड़कर कर्म पर ध्यान कैसे दूँ?
```

After the answer appears, tap the Krishna portrait below the conversation. It should narrate only the Hindi section.

## Voice troubleshooting

- Use current Chrome or Edge.
- Confirm that the browser tab and Windows audio are not muted.
- Speech starts only after a tap; it intentionally does not autoplay on page load.
- When the pronunciation uses a non-Hindi accent, install or enable a Hindi system voice, restart the browser, and tap again.
- The component labels the narration as AI-generated educational audio; it is not an authentic recording of Shri Krishna.

## Groq model reminder

This package deliberately does not replace `core/config.py`. If the app still reports that `llama-3.3-70b-versatile` is unavailable, retain the model-ID correction you made earlier and select a model returned by your Groq Models API.
