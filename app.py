import os
import pathlib
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

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
          <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari&display=swap" rel="stylesheet">
        </head>
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background(str(BASE_DIR / "Copilot_20250726_004311.png"))

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .project-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }
    .project-subtitle {
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 30px;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: black !important;
        border-radius: 8px !important;
        font-size: 1.5rem !important;
        padding: 10px !important;
    }
    .stButton>button {
        background-color: #ffd700 !important;
        color: black !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.5rem;
    }
    .chat {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-top: 20px;
        white-space: pre-wrap;
        word-break: break-word;
        font-family: "Noto Sans Devanagari", "Mukta", sans-serif;
    }
    input[type="text"] {
        color: black !important;
        background-color: white !important;
        border: 1px solid #ccc !important;
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar: Mode selection & API key input ────────────────────────────────────
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
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get your free API key at https://console.groq.com",
        )
        groq_model = st.selectbox(
            "Select Groq Model",
            options=[
                "llama3-8b-8192",
                "llama3-70b-8192",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
            ],
            index=0,
        )
        if not groq_api_key:
            st.warning("⚠️ Please enter your Groq API key to use Cloud mode.")
        else:
            st.success("✅ API key received!")

    st.markdown("---")
    st.markdown(
        """
        **📖 How to get a Groq API Key:**
        1. Go to [console.groq.com](https://console.groq.com)
        2. Sign up for free
        3. Create an API key
        4. Paste it above

        *Your key is never stored or sent anywhere except directly to Groq.*
        """
    )

# ── Build QA chain based on mode ───────────────────────────────────────────────
@st.cache_resource
def load_vector_store():
    """Load and embed the Gita text — shared across both modes."""
    from langchain_ollama import OllamaEmbeddings
    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    split_docs = splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.from_documents(split_docs, embeddings)
    return db


@st.cache_resource
def load_vector_store_hf():
    """HuggingFace embeddings — used in Cloud mode (no Ollama needed)."""
    from langchain_community.embeddings import HuggingFaceEmbeddings
    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    split_docs = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(split_docs, embeddings)
    return db


def get_qa_chain(mode, groq_api_key=None, groq_model=None):
    if mode == "🖥️ Local (Ollama)":
        from langchain_ollama import OllamaLLM
        db = load_vector_store()
        retriever = db.as_retriever(search_kwargs={"k": 3})
        llm = OllamaLLM(model="mistral")
        return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    else:
        from langchain_groq import ChatGroq
        db = load_vector_store_hf()
        retriever = db.as_retriever(search_kwargs={"k": 3})
        llm = ChatGroq(
            api_key=groq_api_key,
            model_name=groq_model,
            temperature=0.3,
        )
        return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")


# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown('<div class="blur-container">', unsafe_allow_html=True)
st.markdown(
    '<h1 class="project-title">Bhagavad Gita AI - Wisdom from Kurukshetra</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="project-subtitle">Ask questions about Dharma, Karma, Life & Duty - directly from the Gita</p>',
    unsafe_allow_html=True,
)

query = st.text_input(
    "Ask your question to Lord Krishna",
    placeholder="e.g. What is true duty according to the Gita?",
)

if st.button("Submit"):
    if mode == "☁️ Cloud (Groq API)" and not groq_api_key:
        st.error("❌ Please enter your Groq API key in the sidebar before submitting.")
    elif query:
        with st.spinner("Seeking wisdom from the Gita..."):
            try:
                qa_chain = get_qa_chain(mode, groq_api_key, groq_model)
                result = qa_chain.invoke(query)
                st.markdown('<div class="chat">', unsafe_allow_html=True)
                st.markdown(f"**Your Question:** {query}", unsafe_allow_html=True)
                st.markdown(f"**Krishna's Wisdom:** {result['result']}", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if mode == "☁️ Cloud (Groq API)":
                    st.info("💡 Make sure your Groq API key is valid. Get one free at https://console.groq.com")
    else:
        st.warning("Please enter a question before submitting.")

st.markdown('</div>', unsafe_allow_html=True)
