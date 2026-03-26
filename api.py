import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
import pathlib
import uvicorn

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI(
    title="Bhagavad Gita AI API",
    description="API to get wisdom from the Bhagavad Gita using Ollama LLM",
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

    loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    split_docs = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.from_documents(split_docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = OllamaLLM(model="mistral")
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
    return {"status": "healthy", "model": "mistral", "embeddings": "nomic-embed-text"}

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
    print("Make sure Ollama is running with 'mistral' and 'nomic-embed-text' models")
    uvicorn.run(app, host="0.0.0.0", port=8000)
