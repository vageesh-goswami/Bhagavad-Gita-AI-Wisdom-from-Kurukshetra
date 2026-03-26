import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

print("Loading Bhagavad Gita text...")
loader = TextLoader(str(BASE_DIR / "gita2.txt"), encoding="utf-8")
doc = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
docs = text_splitter.split_documents(doc)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = FAISS.from_documents(docs, embeddings)

retriever = db.as_retriever(search_kwargs={"k": 3})

llm = OllamaLLM(model="mistral")

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
