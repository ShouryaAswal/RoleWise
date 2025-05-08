import chromadb
from llm_utils import generate_answer

def get_top_k_assessments(query, k=3):
    client = chromadb.PersistentClient(path="../context/chromadb")
    collection = client.get_collection("shl_assessments")
    results = collection.query(query_texts=[query], n_results=k)
    return results['documents'], results['metadatas']

def process_query(query):
    docs, metas = get_top_k_assessments(query)
    context = " ".join(docs)
    answer = generate_answer(query, context)
    return {"answer": answer, "top_assessments": metas}