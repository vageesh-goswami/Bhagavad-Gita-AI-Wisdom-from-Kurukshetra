# Bhagavad Gita AI — Dual-Mode Multilingual RAG Assistant

A source-grounded conversational assistant that retrieves relevant Bhagavad Gita
passages before generating a response. The app supports fast cloud generation with
Groq and fully local generation with Ollama.

> This repository is an educational software project, not a substitute for a verified
> critical edition, qualified spiritual teacher, or professional mental-health advice.

## What the project demonstrates

- Retrieval-augmented generation rather than an ungrounded API call
- Direct FAISS cosine-similarity search over dense embeddings
- Cloud and local model-provider selection behind one service interface
- Bounded conversation memory to prevent unlimited prompt growth
- Visible retrieved evidence and similarity scores for every answer
- Secure API-key loading from environment variables
- Reusable core logic shared by Streamlit and a command-line client
- Unit tests, defensive validation, CI configuration, and clean repository structure

## Architecture

```text
User question
     │
     ▼
Streamlit chat interface
     │
     ├── Cloud mode ── SentenceTransformer embeddings
     │                  + Groq chat generation
     │
     └── Local mode ── Ollama embeddings
                        + Ollama chat generation
     │
     ▼
Curated Gita text → chunking → dense vectors → FAISS index
     │
     ▼
Top-k passages + bounded chat history + grounded prompt
     │
     ▼
Multilingual answer + displayed retrieval evidence
```

## Repository structure

```text
.
├── app.py                         # Streamlit UI and session orchestration
├── answer_bot.py                  # Reusable command-line client
├── core/
│   ├── config.py                  # Models, paths, and retrieval parameters
│   ├── prompts.py                 # Grounded prompt and memory formatting
│   ├── rag_service.py             # Embeddings, direct FAISS search, generation
│   └── styles.py                  # Compact Streamlit presentation theme
├── data/
│   ├── gita_knowledge_base.txt    # Curated multilingual demonstration corpus
│   └── README.md                  # Corpus limitations and replacement guidance
├── tests/                         # Dependency-light unit tests
├── scripts/                       # Windows and Unix setup helpers
├── .github/workflows/tests.yml    # Compile and unit-test workflow
├── .env.example
├── requirements.txt
├── requirements-dev.txt
└── TROUBLESHOOTING.md
```

## Recommended setup: Windows PowerShell

Use 64-bit Python 3.11 for the most predictable setup.

```powershell
git clone https://github.com/vageesh-goswami/Bhagavad-Gita-AI-Wisdom-from-Kurukshetra.git
cd Bhagavad-Gita-AI-Wisdom-from-Kurukshetra

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup_windows.ps1
```

Open `.env` and replace the placeholder with your own Groq API key:

```env
GROQ_API_KEY=replace-me
```

Run the app:

```powershell
.\scripts\run_windows.ps1
```

Or run it manually:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Manual setup

```bash
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS or Linux
source .venv/bin/activate
```

Install and verify:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m compileall -q app.py answer_bot.py core tests
python -m pytest
python -m streamlit run app.py
```

## Cloud mode

Cloud mode uses a local multilingual sentence-transformer for retrieval and Groq for
answer generation. Keep your key in `.env`; `.gitignore` prevents that file from being
committed.

The first question may be slower because the embedding model is downloaded and the
index is built. Ask one question before recording your Loom demonstration so the index
is already cached.

## Fully local Ollama mode

Install and start Ollama, then pull the two required models:

```bash
ollama pull mistral
ollama pull nomic-embed-text
ollama list
```

Select **Local — Ollama** in the sidebar. No cloud API key is used in this mode.

## Command-line use

```bash
python answer_bot.py "How should I focus on effort instead of results?"
```

Local mode:

```bash
python answer_bot.py --mode ollama "How can I control a distracted mind?"
```

## Good demonstration questions

1. `What does the Gita teach about focusing on action rather than results?`
2. `How can I apply this before a software engineering interview?`

The second question demonstrates bounded conversational memory. Expand **Retrieved
passages used for this answer** to show that the response was grounded in actual indexed
text rather than generated without evidence.

## Design decisions worth explaining in an interview

### Direct FAISS integration

The project normalises document and query vectors and uses `IndexFlatIP`. Inner product
between normalised vectors is cosine similarity. This makes the retrieval logic explicit
and avoids hiding it behind a large wrapper.

### Two embedding backends behind one interface

Both SentenceTransformer and Ollama expose `embed_documents` and `embed_query` through
a small protocol. The FAISS index therefore does not need provider-specific logic.

### Bounded memory

Only the latest configured number of completed user-assistant pairs are inserted into
the prompt. This prevents history from growing indefinitely and keeps behaviour easy to
reason about.

### Evidence visibility

The interface displays the exact retrieved passages and similarity scores. This helps
with debugging and makes grounding inspectable during a code walkthrough.

## Honest limitations

- The bundled corpus is curated and compact, not the complete 700-verse scripture.
- Similarity retrieval does not guarantee the ideal theological passage for every query.
- Generated explanations still require evaluation for faithfulness and translation quality.
- The FAISS index is rebuilt per server process rather than persisted to disk.
- The application has unit tests for deterministic logic but not a full model-output eval suite.

## Suggested next improvements

- Replace the demonstration corpus with a verified edition and detailed source metadata.
- Add retrieval test cases with expected verse references.
- Add an LLM faithfulness evaluator and human review rubric.
- Persist the FAISS index with a content hash and rebuild only when the corpus changes.
- Add Hindi/Sanskrit query benchmarks and citation validation.

## Licence

Application code is released under the MIT Licence. Review the rights and attribution
requirements of any full scripture edition or translation before adding it to the project.
