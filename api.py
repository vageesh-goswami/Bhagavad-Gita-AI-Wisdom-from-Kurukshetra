import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
import pathlib
import uvicorn
from dotenv import load_dotenv

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Bhagavad Gita AI API",
    description="API to get wisdom from the Bhagavad Gita using multiple LLM providers",
    version="2.0.0"
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

# Provider-specific configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-pro")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

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

    elif LLM_PROVIDER == "google":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required when using Google provider")

        print(f"Using Google Gemini with model: {GOOGLE_MODEL}")
        embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=GOOGLE_API_KEY,
            model=GOOGLE_EMBEDDING_MODEL
        )
        llm = ChatGoogleGenerativeAI(
            google_api_key=GOOGLE_API_KEY,
            model=GOOGLE_MODEL,
            temperature=0.7
        )

    elif LLM_PROVIDER == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required when using Anthropic provider")

        print(f"Using Anthropic Claude with model: {ANTHROPIC_MODEL}")
        # For Anthropic, we'll use OpenAI embeddings as Claude doesn't have embeddings API
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is also required for embeddings when using Anthropic provider")

        embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=OPENAI_EMBEDDING_MODEL
        )
        llm = ChatAnthropic(
            anthropic_api_key=ANTHROPIC_API_KEY,
            model=ANTHROPIC_MODEL,
            temperature=0.7
        )

    else:  # Default to Ollama
        print(f"Using Ollama with model: {OLLAMA_MODEL}")
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)
        llm = OllamaLLM(model=OLLAMA_MODEL)

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
    elif LLM_PROVIDER == "google":
        provider_info["model"] = GOOGLE_MODEL
        provider_info["embeddings"] = GOOGLE_EMBEDDING_MODEL
    elif LLM_PROVIDER == "anthropic":
        provider_info["model"] = ANTHROPIC_MODEL
        provider_info["embeddings"] = OPENAI_EMBEDDING_MODEL + " (for embeddings)"
    else:
        provider_info["model"] = OLLAMA_MODEL
        provider_info["embeddings"] = OLLAMA_EMBEDDING_MODEL

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
    print(f"Provider: {LLM_PROVIDER.upper()}")

    if LLM_PROVIDER == "openai":
        print(f"Using OpenAI with model: {OPENAI_MODEL}")
        print("Make sure OPENAI_API_KEY is set in your .env file")
    elif LLM_PROVIDER == "google":
        print(f"Using Google Gemini with model: {GOOGLE_MODEL}")
        print("Make sure GOOGLE_API_KEY is set in your .env file")
    elif LLM_PROVIDER == "anthropic":
        print(f"Using Anthropic Claude with model: {ANTHROPIC_MODEL}")
        print("Make sure ANTHROPIC_API_KEY and OPENAI_API_KEY are set in your .env file")
    else:
        print(f"Using Ollama with model: {OLLAMA_MODEL}")
        print("Make sure Ollama is running with required models")

    uvicorn.run(app, host="0.0.0.0", port=8000)
