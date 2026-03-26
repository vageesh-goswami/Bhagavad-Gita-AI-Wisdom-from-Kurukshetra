import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
import pathlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

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
else:  # Default to Ollama
    print("Using Ollama with model: mistral")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    llm = OllamaLLM(model="mistral")

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
