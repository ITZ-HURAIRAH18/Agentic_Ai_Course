from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

from langchain_google_genai import (
    GoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Memory
memory = ConversationBufferWindowMemory(k=5)

# Load document
try:
    loader = TextLoader("data.txt")
    documents = loader.load()
except Exception as e:
    raise ValueError(f"Failed to load the file: {e}")

# Embeddings
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

# Text splitter
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)

# Vector store (replacement for VectorstoreIndexCreator)
store = FAISS.from_documents(docs, embedding)

# Chat loop
while True:
    human_message = input("How can I help you today? ")
    if human_message.lower() in ["exit", "quit"]:
        break

    retrieved_docs = store.similarity_search(human_message, k=3)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {human_message}
    """

    response = llm.invoke(prompt)
    print(response)
