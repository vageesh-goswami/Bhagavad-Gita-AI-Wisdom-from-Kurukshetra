# Troubleshooting

## PowerShell blocks script execution

Run this once in the current terminal, then run the setup script again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## `py -3.11` cannot find Python

Install 64-bit Python 3.11 and enable **Add Python to PATH**, or replace `py -3.11`
with the full path to your Python 3.11 executable.

## Cloud mode says the Groq key is missing

Copy `.env.example` to `.env`, replace the placeholder, save the file, and restart
Streamlit. Do not wrap the key in quotation marks.

## First cloud-mode question is slow

The multilingual sentence-transformer model is downloaded and the FAISS index is
built on the first question. Run one test question before recording the Loom video;
subsequent questions reuse Streamlit's cached index.

## Ollama connection error

Confirm Ollama is installed and running, then execute:

```powershell
ollama pull mistral
ollama pull nomic-embed-text
ollama list
```

Restart the app after both models are available.

## `faiss-cpu` installation fails

Use 64-bit Python 3.11 and a fresh virtual environment. Confirm the interpreter with:

```powershell
.\.venv\Scripts\python.exe --version
```

## The selected Groq model is unavailable

Model availability can change. Update `GROQ_MODELS` in `core/config.py` to an active
model ID shown in your Groq console, then restart Streamlit.
