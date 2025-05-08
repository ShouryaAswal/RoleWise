import chromadb
from llm_utils import generate_answer

def print_collections():
    client = chromadb.PersistentClient(path="../context/chromadb")
    print("Available collections:", [c.name for c in client.list_collections()])

def get_top_k_assessments(query, k=3):
    client = chromadb.PersistentClient(path="../context/chromadb")
    collection = client.get_collection('shl_assessments')
    results = collection.query(query_texts=[query], n_results=k)
    return results['documents'], results['metadatas']

def process_query(query):
    docs, metas = get_top_k_assessments(query)
    answers = []
    for context, meta_item in zip(docs[0], metas[0]):
        # Use info_blob from metadata as context
        info_blob = meta_item.get("info_blob", "")
        title = meta_item.get("title", "Unknown Assessment")
        url = meta_item.get("detail_url", "#")
        answer = generate_answer(query, info_blob)
        answers.append({
            "title": title,
            "url": url,
            "llm_answer": answer
        })
    return {"answers": answers}

if __name__ == "__main__":
    print_collections()