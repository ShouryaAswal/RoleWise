import json
import os
import time
import sys
import chromadb

DATA_PATH = os.path.join("..", "context", "scraped_data.jsonl")
CHROMA_PATH = os.path.join("..", "context", "chromadb")

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


print("Creating/getting collection...")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.create_collection("shl_assessments")

print("Inserting records into ChromaDB...")
success_count = 0
for idx, rec in enumerate(records):
    try:
        text = rec.get("info_blob", "")
        if text == "":
            print(f"Skipping record {idx}: Empty info_blob")
            continue
            
  
        doc_id = rec.get("Title", f"doc_{idx}")
        
            
        metadata = {
            "title": rec.get("title", ""),
            "detail_url": rec.get("detail_url", ""),
            "test_type": rec.get("test_type", ""),
            "assessment_length": rec.get("assessment_length", ""),
            "info_blob": rec.get("info_blob", "")
        }
        
  
        collection.add(
            
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        success_count += 1
        

        if (idx + 1) % 10 == 0 or idx == len(records) - 1:
            print(f"Processed {idx + 1}/{len(records)} records")
            

        
    except Exception as e:
        print(f"Error processing record {idx}: {e}")


try:
    client = chromadb.PersistentClient(path="../context/chromadb")
except Exception as persist_error:
    print(f"Note: Could not call persist() method: {persist_error}")

print(f"Successfully inserted {success_count} out of {len(records)} records into ChromaDB at {CHROMA_PATH}")