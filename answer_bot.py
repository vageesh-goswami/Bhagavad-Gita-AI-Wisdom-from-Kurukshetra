import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
import pathlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

BASE_DIR = pathlib.Path(__file__).parent

print("Loading Bhagavad Gita text...")
print(f"LLM Provider: {LLM_PROVIDER}")
loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
doc = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
docs = text_splitter.split_documents(doc)

# Initialize embeddings and LLM based on provider
if LLM_PROVIDER == "openai":
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not found in .env file.")
        print("Please set it to use OpenAI provider or change LLM_PROVIDER to 'ollama'")
        exit(1)

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
        print("ERROR: GOOGLE_API_KEY not found in .env file.")
        print("Please set it to use Google provider or change LLM_PROVIDER to 'ollama'")
        exit(1)

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
        print("ERROR: ANTHROPIC_API_KEY not found in .env file.")
        print("Please set it to use Anthropic provider or change LLM_PROVIDER to 'ollama'")
        exit(1)

    # For Anthropic, we'll use OpenAI embeddings as Claude doesn't have embeddings API
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is also required for embeddings when using Anthropic provider.")
        exit(1)

    print(f"Using Anthropic Claude with model: {ANTHROPIC_MODEL}")
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

db = FAISS.from_documents(docs, embeddings)

retriever = db.as_retriever(search_kwargs={"k": 3})

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

print("\nWelcome to the Bhagavad Gita AI Bot")
print("Ask any question about life, karma, duty, or Gita's teachings.")
print("Type 'exit' to quit.\n")

while True:
    query = input("Ask a question from Gita (or type 'exit'): ")
    if query.lower() == "exit":
        print("Thank you for using our bot")
        break
    result = qa.invoke(query)
    print("\nAnswer:", result["result"])
    print("\n" + "--" * 50)
