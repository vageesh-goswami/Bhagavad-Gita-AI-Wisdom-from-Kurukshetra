import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
import pathlib

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

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
        unsafe_allow_html=True
    )

BASE_DIR = pathlib.Path(__file__).parent
set_background(str(BASE_DIR / "Copilot_20250726_004311.png"))

@st.cache_resource
def load_qa_chain():
    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    split_docs = splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.from_documents(split_docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    llm = OllamaLLM(model="mistral")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    return qa

qa_chain = load_qa_chain()

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

st.markdown('<div class="blur-container">', unsafe_allow_html=True)

st.markdown(
    '<h1 class="project-title">Bhagavad Gita AI - Wisdom from Kurukshetra</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="project-subtitle">Ask questions about Dharma, Karma, Life & Duty - directly from the Gita</p>',
    unsafe_allow_html=True
)

query = st.text_input("Ask your question to Lord Krishna", placeholder="e.g. What is true duty according to the Gita?")

if st.button("Submit"):
    if query:
        with st.spinner("Thinking..."):
            result = qa_chain.invoke(query)
        st.markdown('<div class="chat">', unsafe_allow_html=True)
        st.markdown(f"**Your Question:** {query}", unsafe_allow_html=True)
        st.markdown(f"**Krishna's Wisdom:** {result['result']}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a question before submitting.")

st.markdown('</div>', unsafe_allow_html=True)
