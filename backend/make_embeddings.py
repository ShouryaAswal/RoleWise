import json
import os
import time
import chromadb
from sentence_transformers import SentenceTransformer

# Paths
DATA_PATH = os.path.join("context", "scraped_data.jsonl")
CHROMA_PATH = os.path.join("context", "chromadb")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read data
records = []
with open(DATA_PATH, "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

# Prepare ChromaDB
# Fix: Changed 'persist_directory' to 'path' which is the correct parameter name
client_chroma = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client_chroma.get_or_create_collection("shl_assessments")

# Prepare and insert embeddings
for idx, rec in enumerate(records):
    text = rec.get("info_blob", "")
    if not text.strip():
        continue
    # Get embedding from sentence-transformers
    embedding = model.encode(text)
    # Use detail_url as unique id
    doc_id = rec.get("detail_url", f"doc_{idx}")
    metadata = {
        "title": rec.get("title", ""),
        "detail_url": rec.get("detail_url", ""),
        "test_type": rec.get("test_type", ""),
        "assessment_length": rec.get("assessment_length", "")
    }
    collection.add(
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    # Optional: avoid rate limits
    time.sleep(0.2)

client_chroma.persist()
print(f"Inserted {len(records)} records into ChromaDB at {CHROMA_PATH}")