# Bhagavad Gita AI — Wisdom from Kurukshetra 🕉️🤖

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A spiritual AI chatbot that answers your questions on Dharma, Karma, Life & Duty — powered by the sacred wisdom of the **Bhagavad Gita** using a fully local RAG (Retrieval-Augmented Generation) pipeline.

![App Screenshot](Copilot_20250726_004311.png)

---

## 📖 About the Project

**Bhagavad Gita AI** bridges ancient Vedic philosophy with modern generative AI. Ask any life question — about duty, purpose, fear, or action — and receive guidance rooted directly in the Gita's verses. The project runs **100% locally** using Ollama, requiring no paid API keys.

---

## ✨ Features

- 🙏 Ask any spiritual, philosophical, or life-related question
- 📚 Answers grounded in actual Bhagavad Gita verses (RAG pipeline)
- 🧠 Fully local LLM inference via **Ollama** (Mistral model)
- 🔍 Semantic search using **FAISS** vector store + Nomic embeddings
- 🎨 Beautiful Streamlit UI with custom background & Devanagari font support
- ⚡ Cached QA chain for fast repeated queries
- 🖼️ Battlefield of Kurukshetra themed visual design

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit |
| **LLM** | Ollama (Mistral) |
| **Embeddings** | Ollama (nomic-embed-text) |
| **Vector Store** | FAISS |
| **RAG Framework** | LangChain (RetrievalQA) |
| **Document Loader** | LangChain TextLoader |
| **Text Splitter** | RecursiveCharacterTextSplitter |
| **Language** | Python 3.10+ |

---

## 📂 File Structure

```
Bhagavad-Gita-AI-Wisdom-from-Kurukshetra/
│
├── app.py                          # Main Streamlit app (UI + RAG pipeline)
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
- [Ollama](https://ollama.com/) installed and running locally

### 1. Clone the Repository

```bash
git clone https://github.com/vageesh-goswami/Bhagavad-Gita-AI-Wisdom-from-Kurukshetra.git
cd Bhagavad-Gita-AI-Wisdom-from-Kurukshetra
```

### 2. Install Dependencies

```bash
pip install streamlit langchain langchain-community langchain-ollama faiss-cpu
```

### 3. Pull Required Ollama Models

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 4. Run the App

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

---

## 🧠 How It Works

```
User Question
     │
     ▼
[ Streamlit UI ]
     │
     ▼
[ TextLoader → gita2.txt ]
     │
     ▼
[ RecursiveCharacterTextSplitter (chunk_size=500, overlap=30) ]
     │
     ▼
[ OllamaEmbeddings (nomic-embed-text) → FAISS Vector DB ]
     │
     ▼
[ Retriever (top-3 relevant chunks) ]
     │
     ▼
[ OllamaLLM (Mistral) + RetrievalQA Chain ]
     │
     ▼
Krishna's Wisdom (Answer)
```

1. The Bhagavad Gita text is loaded and split into small chunks.
2. Each chunk is embedded using `nomic-embed-text` and stored in a FAISS index.
3. When a question is asked, the top-3 most relevant chunks are retrieved.
4. The `Mistral` LLM generates an answer grounded in those retrieved passages.

---

## 🧾 Use Cases

| Who | Use Case |
|---|---|
| 👨‍🎓 Students | Seek guidance for life decisions & purpose |
| 🧘 Spiritual Seekers | Get Gita-based answers to philosophical queries |
| 💻 Developers | Learn RAG & LangChain through a meaningful project |
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
- Add more Gita text sources
- Improve the UI/UX
- Add multilingual support (Hindi, Sanskrit)
- Integrate voice input/output
- Replace local Ollama with cloud LLMs (OpenAI, Gemini, etc.)

```bash
# Fork the repo, create a branch, and submit a PR
git checkout -b feature/your-feature-name
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- The sacred text of the **Bhagavad Gita**
- [LangChain](https://github.com/langchain-ai/langchain) for the RAG framework
- [Ollama](https://ollama.com/) for local LLM serving
- [Streamlit](https://streamlit.io/) for the web UI framework
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI for vector search

---

<p align="center">
  Made with 🙏 and 🤖 by <a href="https://github.com/vageesh-goswami">Vageesh Goswami</a>
</p>
