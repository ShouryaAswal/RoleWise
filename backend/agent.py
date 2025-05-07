import chromadb
from chromadb.config import Settings
from backend.model import call_openai
import os

# Updated to match the collection name used in make_embeddings.py
CHROMA_COLLECTION = "shl_assessments"
CHROMA_PATH = os.path.join("context", "chromadb")

def retrieve_context(query, top_k=3):
    chroma_client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH
    ))
    collection = chroma_client.get_collection(CHROMA_COLLECTION)
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    docs = results['documents'][0]
    return "\n".join(docs)

def agent_qa(query):
    context = retrieve_context(query)
    prompt = f"Answer the following question using the provided context.\nContext:\n{context}\nQuestion: {query}"
    return call_openai(prompt, context=None)

# Example usage:
# answer = agent_qa("What is ...?")