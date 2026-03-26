# Bhagavad-Gita-AI-Wisdom-from-Kurukshetra
Bhagavad Gita AI — Wisdom from Kurukshetra
# Bhagavad-Gita-AI-Wisdom-from-Kurukshetra 🕉️🤖

A spiritual AI chatbot that extracts and delivers profound wisdom from the sacred scripture **Bhagavad Gita**. Powered by natural language processing (NLP), this project bridges ancient philosophy with modern artificial intelligence.

---

## 📌 Features

- ✨ Ask any spiritual or life-related question
- 📚 Get answers based on Bhagavad Gita verses
- 🌐 Multiple interfaces: Web UI (Streamlit), CLI, and REST API
- 🧠 **Flexible LLM Support**: Choose from Ollama (local), OpenAI, Google Gemini, or Anthropic Claude
- 🔌 REST API for integration with other applications
- 🔑 Use your own API key from any supported provider
- 💻 Completely free option with local Ollama

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

Choose one of the following LLM providers:

#### **Option 1: Ollama (Local, Free)** ⭐ Recommended for privacy

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Pull required models**:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

#### **Option 2: OpenAI (Cloud, Paid)**

1. Get an API key from [platform.openai.com](https://platform.openai.com/)
2. Create `.env` file and add:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

#### **Option 3: Google Gemini (Cloud, Free tier available)**

1. Get an API key from [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Create `.env` file and add:
```env
LLM_PROVIDER=google
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-pro
```

#### **Option 4: Anthropic Claude (Cloud, Paid)**

1. Get an API key from [console.anthropic.com](https://console.anthropic.com/)
2. Create `.env` file and add:
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
# Note: Claude requires OpenAI for embeddings
OPENAI_API_KEY=your_openai_api_key_here
```

### Installation

```bash
# Clone the repository
git clone https://github.com/vageesh-goswami/Bhagavad-Gita-AI-Wisdom-from-Kurukshetra.git
cd Bhagavad-Gita-AI-Wisdom-from-Kurukshetra

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy .env.example and configure your provider
cp .env.example .env
# Edit .env with your preferred provider settings
```

---

## 💻 Running the Application

This project provides **three different ways** to interact with the Bhagavad Gita AI:

> **Note:** All three interfaces support Ollama, OpenAI, Google Gemini, and Anthropic Claude. The system automatically uses the provider specified in your `.env` file (defaults to Ollama if not specified).

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

- **LLM Providers**:
  - Local: Ollama (Mistral)
  - Cloud: OpenAI (GPT-3.5/GPT-4), Google Gemini, Anthropic Claude
- **Embeddings**: Provider-specific (Ollama, OpenAI, Google)
- **Vector Store**: FAISS
- **Framework**: LangChain
- **Web UI**: Streamlit
- **API**: FastAPI
- **Language**: Python 3.8+

---

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file (see `.env.example`):

```env
# Choose your LLM provider
LLM_PROVIDER=ollama  # Options: ollama, openai, google, anthropic

# Provider-specific API keys (only needed for cloud providers)
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Model configurations (optional, defaults are set)
OPENAI_MODEL=gpt-3.5-turbo
GOOGLE_MODEL=gemini-pro
ANTHROPIC_MODEL=claude-3-sonnet-20240229
OLLAMA_MODEL=mistral
```

### Switching Between Providers

Simply change the `LLM_PROVIDER` in your `.env` file:

- `LLM_PROVIDER=ollama` - Free, local, private
- `LLM_PROVIDER=openai` - Fast, powerful (requires API key)
- `LLM_PROVIDER=google` - Free tier available (requires API key)
- `LLM_PROVIDER=anthropic` - High quality responses (requires API key + OpenAI key for embeddings)

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
