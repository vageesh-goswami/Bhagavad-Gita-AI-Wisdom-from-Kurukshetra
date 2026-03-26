# Bhagavad-Gita-AI-Wisdom-from-Kurukshetra
Bhagavad Gita AI — Wisdom from Kurukshetra
# Bhagavad-Gita-AI-Wisdom-from-Kurukshetra 🕉️🤖

A spiritual AI chatbot that extracts and delivers profound wisdom from the sacred scripture **Bhagavad Gita**. Powered by natural language processing (NLP), this project bridges ancient philosophy with modern artificial intelligence.

---

## 📌 Features

- ✨ Ask any spiritual or life-related question
- 📚 Get answers based on Bhagavad Gita verses
- 🌐 Multiple interfaces: Web UI (Streamlit), CLI, and REST API
- 🧠 Runs locally with Ollama (Mistral model) OR with OpenAI
- 🔌 REST API for integration with other applications
- 🔑 Flexible: Use your own OpenAI API key or run completely locally
- 💻 No external API keys required (if using Ollama)

---

## 🧾 Use Cases

| Who | Use Case |
|-----|----------|
| 👨‍🎓 Students | Seek guidance in life decisions |
| 🧘 Spiritual Seekers | Get Gita-based answers to philosophical queries |
| 💻 Developers | Learn NLP & chatbot development through a spiritual lens |
| 🙏 Teachers | Create a classroom tool to teach Bhagavad Gita |
| 💬 Everyone | Daily dose of divine knowledge |

---

## 📂 File Structure

```
├── app.py              # Streamlit Web UI
├── answer_bot.py       # CLI chatbot interface
├── api.py              # FastAPI REST API server
├── gita2.txt           # Bhagavad Gita text corpus
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

**Option 1: Using Ollama (Local, Free)**

1. **Install Ollama**: Download and install Ollama from [ollama.ai](https://ollama.ai)

2. **Pull required models**:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

**Option 2: Using OpenAI (Cloud, Requires API Key)**

1. **Get an OpenAI API key**: Sign up at [platform.openai.com](https://platform.openai.com/) and get your API key

2. **Create a `.env` file** in the project root:
```bash
cp .env.example .env
```

3. **Edit the `.env` file** and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_api_key_here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
```

**Install Python Dependencies (Required for both options)**:
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

This project provides **three different ways** to interact with the Bhagavad Gita AI:

> **Note:** All three interfaces support both Ollama (local) and OpenAI (cloud). The system automatically uses the provider specified in your `.env` file (defaults to Ollama if not specified).

### 1. Web UI (Streamlit) - Recommended for Interactive Use

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Beautiful UI with background image
- Input field for questions
- Formatted display of answers
- Easy to use for non-technical users

---

### 2. Command Line Interface (CLI) - For Terminal Users

```bash
python answer_bot.py
```

**Features:**
- Simple terminal-based interaction
- Type your question and get instant answers
- Type `exit` to quit
- Great for quick queries

---

### 3. REST API (FastAPI) - For Integration & Development

```bash
python api.py
```

The API server will start at `http://localhost:8000`

**Features:**
- RESTful API endpoints
- Interactive documentation at `http://localhost:8000/docs`
- Integrate with other applications
- Suitable for mobile apps, websites, or automation

#### API Endpoints:

**GET /** - API information and available endpoints

**GET /health** - Check if the API is running and models are loaded

**POST /ask** - Ask a question and get an answer

Example request:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is dharma according to the Gita?"}'
```

Example response:
```json
{
  "query": "What is dharma according to the Gita?",
  "answer": "According to the Bhagavad Gita, dharma represents one's duty..."
}
```

**Interactive API Documentation:**
Visit `http://localhost:8000/docs` for Swagger UI where you can test all endpoints interactively.

---

## 🛠️ Technical Stack

- **LLM**: Ollama (Mistral model) OR OpenAI (GPT-3.5-turbo/GPT-4)
- **Embeddings**: Nomic-embed-text (Ollama) OR OpenAI text-embedding-ada-002
- **Vector Store**: FAISS
- **Framework**: LangChain
- **Web UI**: Streamlit
- **API**: FastAPI
- **Language**: Python 3.8+

---

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root:

```env
# LLM Provider: "ollama" (default) or "openai"
LLM_PROVIDER=ollama

# OpenAI Configuration (only needed if LLM_PROVIDER=openai)
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
```

**To switch between providers:**
- For local Ollama: Set `LLM_PROVIDER=ollama` (or omit it, as this is the default)
- For OpenAI: Set `LLM_PROVIDER=openai` and provide your `OPENAI_API_KEY`

---

## 📖 Example Questions

Try asking questions like:
- What is the purpose of life according to the Gita?
- How should I handle difficult situations?
- What does Krishna say about karma?
- What is the path to inner peace?
- How to overcome fear and anxiety?

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📜 License

This project is open source and available for spiritual and educational purposes.

---

## 🙏 Acknowledgments

- The timeless wisdom of the Bhagavad Gita
- Ollama for local LLM capabilities
- LangChain for the RAG framework
- The open-source community

---

**May this project bring wisdom and peace to all who seek it.** 🕉️
