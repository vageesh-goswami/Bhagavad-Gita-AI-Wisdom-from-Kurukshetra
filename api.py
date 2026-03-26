import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
import pathlib
import uvicorn
from dotenv import load_dotenv

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Bhagavad Gita AI API",
    description="API to get wisdom from the Bhagavad Gita using Ollama or OpenAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = pathlib.Path(__file__).parent

# Get configuration from environment
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

class Question(BaseModel):
    query: str

class Answer(BaseModel):
    query: str
    answer: str

# Global variable to store QA chain
qa_chain = None

@app.on_event("startup")
async def startup_event():
    """Initialize the QA chain on startup"""
    global qa_chain
    print("Loading Bhagavad Gita text and initializing models...")
    print(f"LLM Provider: {LLM_PROVIDER}")

    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    split_docs = splitter.split_documents(docs)

    # Initialize embeddings and LLM based on provider
    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required when using OpenAI provider")

        print(f"Using OpenAI with model: {OPENAI_MODEL}")
        embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=OPENAI_EMBEDDING_MODEL
        )
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=0.7
        )
    else:  # Default to Ollama
        print("Using Ollama with model: mistral")
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        llm = OllamaLLM(model="mistral")

    db = FAISS.from_documents(split_docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    print("QA chain initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Bhagavad Gita AI API - Wisdom from Kurukshetra",
        "endpoints": {
            "/ask": "POST - Ask a question about the Bhagavad Gita",
            "/health": "GET - Check API health status",
            "/docs": "GET - Interactive API documentation"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    if qa_chain is None:
        raise HTTPException(status_code=503, detail="QA chain not initialized")

    provider_info = {
        "status": "healthy",
        "provider": LLM_PROVIDER
    }

    if LLM_PROVIDER == "openai":
        provider_info["model"] = OPENAI_MODEL
        provider_info["embeddings"] = OPENAI_EMBEDDING_MODEL
    else:
        provider_info["model"] = "mistral"
        provider_info["embeddings"] = "nomic-embed-text"

    return provider_info

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """
    Ask a question about the Bhagavad Gita and receive wisdom-based answer

    - **query**: Your question about life, dharma, karma, or any spiritual topic
    """
    if qa_chain is None:
        raise HTTPException(status_code=503, detail="QA chain not initialized")

    if not question.query or question.query.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = qa_chain.invoke(question.query)
        return Answer(query=question.query, answer=result["result"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

if __name__ == "__main__":
    print("Starting Bhagavad Gita AI API...")
    if LLM_PROVIDER == "openai":
        print(f"Using OpenAI with model: {OPENAI_MODEL}")
        print("Make sure OPENAI_API_KEY is set in your .env file")
    else:
        print("Using Ollama (default)")
        print("Make sure Ollama is running with 'mistral' and 'nomic-embed-text' models")
    uvicorn.run(app, host="0.0.0.0", port=8000)
