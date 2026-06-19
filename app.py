import os
import pathlib
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

BASE_DIR = pathlib.Path(__file__).parent

# ── Background helper ──────────────────────────────────────────────────────────
def set_background(image_file):
    import base64
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <head>
          <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;700&display=swap" rel="stylesheet">
        </head>
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background(str(BASE_DIR / "Copilot_20250726_004311.png"))

# ── Premium Theme CSS ──────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Google Fonts setup */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;
    }
    
    /* Header transparency */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Main Container Glassmorphism Card */
    [data-testid="stMainBlockContainer"] {
        background-color: rgba(18, 18, 24, 0.82) !important;
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        border-radius: 20px !important;
        padding: 2.5rem 3rem !important;
        border: 1px solid rgba(255, 215, 0, 0.18) !important;
        max-width: 820px !important;
        margin-top: 2.5rem !important;
        margin-bottom: 2.5rem !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65) !important;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(12, 12, 16, 0.95) !important;
        border-right: 1px solid rgba(255, 215, 0, 0.15) !important;
        backdrop-filter: blur(10px);
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f5e6c8 !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffd700 !important;
        font-family: 'Cinzel', Georgia, serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* Titles & Headings */
    .project-title {
        font-family: 'Cinzel', Georgia, serif !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        color: #ffd700 !important;
        text-align: center !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9), 0 0 20px rgba(255, 215, 0, 0.3) !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    .project-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem !important;
        color: #f0e6c8 !important;
        text-align: center !important;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8) !important;
        margin-bottom: 2rem !important;
    }

    /* Labels styling */
    [data-testid="stWidgetLabel"] p, label p {
        color: #ffd700 !important;
        font-family: 'Cinzel', Georgia, serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Form Fields - Text Input & Select Box */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #111111 !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stTextInput input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 12px rgba(255, 215, 0, 0.4) !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #111111 !important;
        border-radius: 10px !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #111111 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-family: 'Cinzel', Georgia, serif !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-size: 1.05rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.25s ease !important;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }

    /* Chat Container & Bubbles */
    .chat-container {
        background-color: rgba(10, 10, 15, 0.6) !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
        margin-top: 20px !important;
        margin-bottom: 25px !important;
        max-height: 480px !important;
        overflow-y: auto !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.6) !important;
    }
    .bubble-user {
        align-self: flex-end !important;
        background: linear-gradient(135deg, #ffd700 0%, #e6be00 100%) !important;
        color: #121212 !important;
        padding: 12px 18px !important;
        border-radius: 18px 18px 4px 18px !important;
        max-width: 75% !important;
        font-size: 1rem !important;
        font-weight: 550 !important;
        word-break: break-word !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    .bubble-ai {
        align-self: flex-start !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #f7edd3 !important;
        padding: 14px 20px !important;
        border-radius: 18px 18px 18px 4px !important;
        max-width: 80% !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        border: 1px solid rgba(255, 215, 0, 0.25) !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
    }
    .bubble-label {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        opacity: 0.85 !important;
        margin-bottom: 4px !important;
        letter-spacing: 0.5px !important;
        font-family: 'Cinzel', Georgia, serif !important;
    }
    .user-label { text-align: right !important; color: #ffd700 !important; }
    .ai-label   { text-align: left !important;  color: #f5e6c8; !important; }

    /* Memory badge */
    .memory-badge {
        display: inline-block !important;
        background: rgba(255, 215, 0, 0.15) !important;
        border: 1px solid rgba(255, 215, 0, 0.5) !important;
        color: #ffd700 !important;
        border-radius: 20px !important;
        padding: 4px 14px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-top: 6px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")

    mode = st.radio(
        "Select LLM Mode",
        options=["🖥️ Local (Ollama)", "☁️ Cloud (Groq API)"],
        index=0,
        help="Local mode requires Ollama running. Cloud mode uses Groq — free & fast.",
    )

    groq_api_key = None
    groq_model = None

    if mode == "☁️ Cloud (Groq API)":
        st.markdown("### 🔑 Enter your Groq API Key")
        groq_api_key = st.text_input(
            "Groq API Key", type="password", placeholder="gsk_...",
            help="Get your free API key at https://console.groq.com",
        )
        groq_model = st.selectbox(
            "Select Groq Model",
            options=[
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
            ],
            index=0,
        )
        if not groq_api_key:
            st.warning("⚠️ Please enter your Groq API key to use Cloud mode.")
        else:
            st.success("✅ API key received!")

    st.markdown("---")
    st.markdown("### 🧠 Context Memory Window")
    memory_window = st.slider(
        "Remember last N turns", min_value=1, max_value=10, value=5,
        help="How many past Q&A pairs the AI keeps in memory.",
    )
    st.markdown(
        f'<span class="memory-badge">🧠 Remembering last {memory_window} turns</span>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown(
        """
        **📖 How to get a Groq API Key:**
        1. Go to [console.groq.com](https://console.groq.com)
        2. Sign up for free
        3. Create an API key
        4. Paste it above

        *Your key is never stored — sent directly to Groq.*
        """
    )

# ── Session state ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list of (user_msg, ai_msg)

if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

if st.session_state.last_mode != mode:
    st.session_state.chat_history = []
    st.session_state.last_mode = mode

# ── Vector store (cached per mode) ────────────────────────────────────────────
@st.cache_resource
def load_vector_store_local():
    from langchain_ollama import OllamaEmbeddings
    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return FAISS.from_documents(splitter.split_documents(docs), embeddings)


@st.cache_resource
def load_vector_store_hf():
    from langchain_huggingface import HuggingFaceEmbeddings
    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(splitter.split_documents(docs), embeddings)


# ── Context memory window — pure Python, no LangChain memory ──────────────────
def build_prompt(question: str, history: list, context: str, window: int) -> str:
    """Build a prompt that includes the last `window` turns as conversation memory."""
    recent = history[-window:]  # slice to memory window size
    history_text = ""
    for user_q, ai_a in recent:
        history_text += f"Human: {user_q}\nAssistant: {ai_a}\n\n"

    return f"""You are Lord Krishna, the supreme divine guide, sharing profound wisdom from the Bhagavad Gita.
Use the provided Gita passages to answer the user's question with deep spiritual insight and compassion.

CRITICAL INSTRUCTIONS FOR YOUR RESPONSE:
1. You MUST find and quote the exact Sanskrit Shloka (verse) from the Bhagavad Gita that is most related to the user's question.
2. You MUST structure your answer strictly in the following three languages, in this exact order:
   SANSKRIT: (The original relevant Shloka in Devanagari script, followed by your detailed explanation and answer to the user's question in Sanskrit)

   HINDI: (Your detailed explanation and answer to the user's question in Hindi)

   ENGLISH: (Your detailed explanation and answer to the user's question in English)

3. Ensure your tone is divine, encouraging, and deeply philosophical.
4. Do not use markdown bolding (**) for the language labels, just use uppercase text as shown above.

--- Relevant Gita Passages ---
{context}
--- End Passages ---

--- Recent Conversation (last {window} turns) ---
{history_text.strip() if history_text.strip() else "(New conversation — no prior context.)"}
--- End Conversation ---

Answer the following question clearly following the 3-language structure and citing the Shloka:
Human: {question}
Assistant:"""


def get_answer(question: str, history: list, window: int,
               mode: str, groq_api_key=None, groq_model=None) -> str:
    """Retrieve Gita context, build memory-aware prompt, and call the LLM."""

    # 1. Retrieve relevant Gita chunks
    if mode == "🖥️ Local (Ollama)":
        db = load_vector_store_local()
    else:
        db = load_vector_store_hf()

    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    # 2. Build prompt with memory window
    prompt = build_prompt(question, history, context, window)

    # 3. Call the LLM
    if mode == "🖥️ Local (Ollama)":
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(model="mistral")
        return llm.invoke(prompt)
    else:
        # Lazy import so startup never fails if langchain_groq has issues
        try:
            from langchain_groq import ChatGroq
            from langchain_core.messages import HumanMessage
        except ImportError as e:
            return f"❌ Could not load Groq module: {e}. Try: pip install langchain-groq"

        llm = ChatGroq(api_key=groq_api_key, model_name=groq_model, temperature=0.3)
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content


# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown('<div class="blur-container">', unsafe_allow_html=True)
st.markdown(
    '<h1 class="project-title">🕉️ Bhagavad Gita AI — Wisdom from Kurukshetra</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="project-subtitle">Ask questions about Dharma, Karma, Life &amp; Duty — directly from the Gita</p>',
    unsafe_allow_html=True,
)

# ── Chat bubbles display ───────────────────────────────────────────────────────
if st.session_state.chat_history:
    bubbles_html = '<div class="chat-container">'
    for user_msg, ai_msg in st.session_state.chat_history:
        bubbles_html += f"""
        <div style="display:flex;flex-direction:column;align-items:flex-end;">
          <div class="bubble-label user-label">🧍 You</div>
          <div class="bubble-user">{user_msg}</div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-start;">
          <div class="bubble-label ai-label">🙏 Krishna's Wisdom</div>
          <div class="bubble-ai">{ai_msg}</div>
        </div>
        """
    bubbles_html += '</div>'
    st.markdown(bubbles_html, unsafe_allow_html=True)
else:
    st.markdown(
        '<div style="text-align:center;color:rgba(255,255,255,0.5);margin:20px 0;font-size:0.9rem;">'
        '🕉️ Start by asking a question about dharma, karma, duty, or life...</div>',
        unsafe_allow_html=True,
    )

# ── Input ──────────────────────────────────────────────────────────────────────
query = st.text_input(
    "Ask your question to Lord Krishna",
    placeholder="e.g. What is true duty according to the Gita?",
    key="query_input",
)

col1, col2 = st.columns([1, 4])
with col1:
    submit = st.button("🙏 Ask")

if submit:
    if mode == "☁️ Cloud (Groq API)" and not groq_api_key:
        st.error("❌ Please enter your Groq API key in the sidebar.")
    elif not query.strip():
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Seeking wisdom from the Gita..."):
            try:
                answer = get_answer(
                    question=query.strip(),
                    history=st.session_state.chat_history,
                    window=memory_window,
                    mode=mode,
                    groq_api_key=groq_api_key,
                    groq_model=groq_model,
                )
                st.session_state.chat_history.append((query.strip(), answer))
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if mode == "☁️ Cloud (Groq API)":
                    st.info("💡 Make sure your Groq API key is valid. Get one free at https://console.groq.com")

st.markdown('</div>', unsafe_allow_html=True)
