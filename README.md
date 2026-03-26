# Bhagavad Gita AI — Wisdom from Kurukshetra 🕉️🤖

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Cloud%20API-orange?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

> A spiritual AI chatbot that answers your questions on Dharma, Karma, Life & Duty — powered by the sacred wisdom of the **Bhagavad Gita**. Supports both **local Ollama** and **cloud Groq API** modes.

![App Screenshot](Copilot_20250726_004311.png)

---

## 📖 About the Project

**Bhagavad Gita AI** bridges ancient Vedic philosophy with modern generative AI. Ask any life question — about duty, purpose, fear, or action — and receive guidance rooted directly in the Gita’s verses.

The app now supports **two modes**:
- **🖥️ Local Mode** — Runs 100% offline using Ollama (Mistral LLM + nomic-embed-text embeddings). No API key needed.
- **☁️ Cloud Mode** — Enter your own **Groq API key** and use powerful cloud LLMs (LLaMA 3, Mixtral, Gemma) without installing anything locally.

---

## ✨ Features

- 🙏 Ask any spiritual, philosophical, or life-related question
- 📚 Answers grounded in actual Bhagavad Gita verses (RAG pipeline)
- 🔑 **User-provided Groq API key** — enter your key in the sidebar, no `.env` file needed
- 🧠 Fully local LLM inference via **Ollama** (Mistral model)
- ☁️ Cloud inference via **Groq API** (LLaMA 3, Mixtral, Gemma2)
- 🔍 Semantic search using **FAISS** vector store
- 🎨 Beautiful Streamlit UI with custom battlefield background & Devanagari font
- ⚡ Cached QA chain for fast repeated queries
- ❌ Graceful error handling with helpful messages

---

## 🔑 API Key Feature (New!)

You can now run this project **without installing Ollama** by using your own **Groq API key**.

### How it works:
1. Open the app sidebar
2. Select **☁️ Cloud (Groq API)** mode
3. Paste your Groq API key (starts with `gsk_`)
4. Choose a model (LLaMA 3, Mixtral, Gemma2, etc.)
5. Ask your question!

> Your API key is **never stored** — it only lives in your browser session and is sent directly to Groq.

### Get a FREE Groq API Key:
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create a new API key
4. Paste it in the sidebar

---

## 🛠️ Tech Stack

| Layer | Local Mode | Cloud Mode |
|---|---|---|
| **Frontend / UI** | Streamlit | Streamlit |
| **LLM** | Ollama (Mistral) | Groq (LLaMA 3 / Mixtral / Gemma2) |
| **Embeddings** | Ollama (nomic-embed-text) | HuggingFace (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS | FAISS |
| **RAG Framework** | LangChain (RetrievalQA) | LangChain (RetrievalQA) |
| **Language** | Python 3.10+ | Python 3.10+ |

---

## 📂 File Structure

```
Bhagavad-Gita-AI-Wisdom-from-Kurukshetra/
│
├── app.py                          # Main Streamlit app (UI + dual-mode RAG pipeline)
├── answer_bot.py                   # Core RAG logic (CLI version)
├── gita.txt                        # Bhagavad Gita text (source 1)
├── gita2.txt                       # Bhagavad Gita text (source 2, used for embeddings)
├── battlefield-of-kurushreta.jpg   # Background image asset
├── Copilot_20250726_004311.png     # App screenshot / background
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- For **Local mode**: [Ollama](https://ollama.com/) installed and running
- For **Cloud mode**: A free [Groq API key](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/vageesh-goswami/Bhagavad-Gita-AI-Wisdom-from-Kurukshetra.git
cd Bhagavad-Gita-AI-Wisdom-from-Kurukshetra
```

### 2. Install Dependencies

```bash
pip install streamlit langchain langchain-community langchain-ollama langchain-groq faiss-cpu sentence-transformers
```

### 3a. Local Mode — Pull Ollama Models

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 3b. Cloud Mode — Get Groq API Key

```
1. Go to https://console.groq.com
2. Sign up for free
3. Create an API key
4. Paste it in the app sidebar
```

### 4. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and choose your mode from the sidebar.

---

## 🧠 How It Works

```
User Question
     │
     ▼
[ Streamlit UI + Sidebar Mode Selector ]
     │
     ┬─────────────────────────────────────┤
     │ Local Mode                  Cloud Mode │
     ▼                                        ▼
[OllamaEmbeddings]              [HuggingFaceEmbeddings]
[nomic-embed-text]              [all-MiniLM-L6-v2]
     │                                        │
     ▼                                        ▼
         [ FAISS Vector DB (gita2.txt) ]
                       │
                       ▼
            [ Retriever (top-3 chunks) ]
                       │
          ┬─────────────────────┤
          │ Local               Cloud │
          ▼                           ▼
    [OllamaLLM]            [ChatGroq + User API Key]
     (Mistral)           (llama3 / mixtral / gemma2)
          │                           │
          └───────▼───────┘
            Krishna's Wisdom
```

---

## 🧾 Use Cases

| Who | Use Case |
|---|---|
| 👨‍🎓 Students | Seek guidance for life decisions & purpose |
| 🧘 Spiritual Seekers | Get Gita-based answers to philosophical queries |
| 💻 Developers | Learn RAG + LangChain through a meaningful project |
| 🙏 Teachers | Create a classroom tool to teach Bhagavad Gita |
| 💬 Everyone | Daily dose of divine knowledge |

---

## 💬 Example Questions

- *"What is true duty according to the Gita?"*
- *"How should I deal with fear and anxiety?"*
- *"What does Krishna say about action without desire?"*
- *"What is the meaning of Karma Yoga?"*
- *"How to attain inner peace?"*

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add OpenAI / Gemini API key support
- Add multilingual support (Hindi, Sanskrit)
- Integrate voice input/output
- Improve the UI/UX

```bash
git checkout -b feature/your-feature-name
```

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

- The sacred text of the **Bhagavad Gita**
- [LangChain](https://github.com/langchain-ai/langchain) for the RAG framework
- [Ollama](https://ollama.com/) for local LLM serving
- [Groq](https://groq.com/) for blazing-fast cloud inference
- [Streamlit](https://streamlit.io/) for the web UI framework
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI for vector search

---

<p align="center">
  Made with 🙏 and 🤖 by <a href="https://github.com/vageesh-goswami">Vageesh Goswami</a>
</p>
