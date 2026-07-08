"""
seed_vector_store.py
--------------------
Loads food nutrition data and dietary guidelines into ChromaDB
for RAG-based retrieval by the Nutrition Knowledge Agent.

Usage:
    python scripts/seed_vector_store.py

Requirements:
    pip install chromadb langchain ibm-watsonx-ai
"""

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependencies — install via: pip install chromadb langchain ibm-watsonx-ai
# ---------------------------------------------------------------------------
try:
    import chromadb
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Run: pip install chromadb langchain langchain-community ibm-watsonx-ai")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "food_database"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "food_nutrition_kb"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

DATA_FILES = [
    DATA_DIR / "usda_foods_sample.json",
    DATA_DIR / "disease_diet_guidelines.json",
]


def load_json_documents(filepath: Path) -> list[dict]:
    """Load a JSON file and return a list of document dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Normalize: if the file is a list, use as-is; if dict, wrap in list
    return data if isinstance(data, list) else [data]


def doc_to_text(doc: dict) -> str:
    """Convert a document dict to a plain-text string for embedding."""
    return "\n".join(f"{k}: {v}" for k, v in doc.items() if v is not None)


def seed():
    print(f"[INFO] Initialising ChromaDB at: {CHROMA_DIR}")
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Drop + recreate for a clean seed
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"[INFO] Dropped existing collection '{COLLECTION_NAME}'")
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)
    print(f"[INFO] Created collection '{COLLECTION_NAME}'")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    total_docs = 0
    for filepath in DATA_FILES:
        if not filepath.exists():
            print(f"[WARN] File not found, skipping: {filepath}")
            continue

        print(f"[INFO] Loading: {filepath.name}")
        raw_docs = load_json_documents(filepath)

        for i, raw in enumerate(raw_docs):
            text = doc_to_text(raw)
            chunks = splitter.split_text(text)

            ids = [f"{filepath.stem}_{i}_{j}" for j in range(len(chunks))]
            metadatas = [{"source": filepath.name, "doc_index": i} for _ in chunks]

            collection.add(documents=chunks, metadatas=metadatas, ids=ids)
            total_docs += len(chunks)

        print(f"[INFO] Loaded {len(raw_docs)} records from {filepath.name}")

    print(f"\n[SUCCESS] Vector store seeded with {total_docs} chunks into '{COLLECTION_NAME}'")


if __name__ == "__main__":
    seed()
