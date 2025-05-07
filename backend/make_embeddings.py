import json
import os
import time
import sys
import chromadb
from sentence_transformers import SentenceTransformer
import pkg_resources

# Paths
DATA_PATH = os.path.join("context", "scraped_data.jsonl")
CHROMA_PATH = os.path.join("context", "chromadb")

# Check ChromaDB version to use appropriate initialization
chromadb_version = pkg_resources.get_distribution("chromadb").version
print(f"ChromaDB version: {chromadb_version}")

# Load embedding model
print("Loading SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read data
print(f"Reading data from {DATA_PATH}...")
records = []
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    print(f"Loaded {len(records)} records")
except FileNotFoundError:
    print(f"Error: {DATA_PATH} not found. Make sure to run the scraper first.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: {DATA_PATH} contains invalid JSON. Check the file format.")
    sys.exit(1)

# Initialize ChromaDB based on version
print(f"Initializing ChromaDB at {CHROMA_PATH}...")
try:
    # For newer versions (using Client with Settings)
    from chromadb.config import Settings
    client_chroma = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH
    ))
    print("Using chromadb.Client with Settings")
except Exception as e1:
    print(f"Error using Settings approach: {e1}")
    try:
        # For newer versions (using PersistentClient with path)
        client_chroma = chromadb.PersistentClient(path=CHROMA_PATH)
        print("Using chromadb.PersistentClient with path")
    except Exception as e2:
        print(f"Error using PersistentClient approach: {e2}")
        # Last resort - for older versions
        try:
            client_chroma = chromadb.Client(chroma_db_impl="duckdb+parquet", 
                                        persist_directory=CHROMA_PATH)
            print("Using legacy chromadb.Client initialization")
        except Exception as e3:
            print(f"All ChromaDB initialization methods failed: {e3}")
            sys.exit(1)

# Create or get collection
print("Creating/getting collection...")
collection = client_chroma.get_or_create_collection("shl_assessments")

# Process and insert records
print("Inserting records into ChromaDB...")
success_count = 0
for idx, rec in enumerate(records):
    try:
        text = rec.get("info_blob", "")
        if not text.strip():
            print(f"Skipping record {idx}: Empty info_blob")
            continue
            
        # Get embedding from sentence-transformers
        embedding = model.encode(text).tolist()  # Make sure it's a list
        
        # Use detail_url as unique id
        doc_id = rec.get("detail_url", f"doc_{idx}")
        if isinstance(doc_id, str) and len(doc_id) > 0:
            # Ensure doc_id is valid by removing problematic characters
            doc_id = doc_id.replace('/', '_').replace(':', '_')[:100]
        else:
            doc_id = f"doc_{idx}"
            
        metadata = {
            "title": rec.get("title", ""),
            "detail_url": rec.get("detail_url", ""),
            "test_type": rec.get("test_type", ""),
            "assessment_length": rec.get("assessment_length", "")
        }
        
        # Add to collection
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        success_count += 1
        
        # Progress indicator
        if (idx + 1) % 10 == 0 or idx == len(records) - 1:
            print(f"Processed {idx + 1}/{len(records)} records")
            
        # Optional: avoid rate limits
        #time.sleep(0.2)
        
    except Exception as e:
        print(f"Error processing record {idx}: {e}")

# Try to persist changes if the method exists
try:
    if hasattr(client_chroma, "persist"):
        client_chroma.persist()
        print("Changes persisted with client_chroma.persist()")
except Exception as persist_error:
    print(f"Note: Could not call persist() method: {persist_error}")

print(f"Successfully inserted {success_count} out of {len(records)} records into ChromaDB at {CHROMA_PATH}")