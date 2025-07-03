import os
import json
import faiss
import numpy as np
import cohere
from dotenv import load_dotenv

load_dotenv()

INDEX_PATH = "catalog_ai/medicine_index.faiss"
DATA_PATH = "catalog_ai/medicine_data.json"
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def embed_texts(texts):
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY not set in environment.")
    co = cohere.Client(COHERE_API_KEY)

    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return np.array(response.embeddings, dtype="float32")
    except Exception as e:
        print(f"Error embedding texts: {e}")
        return np.empty((0, 384), dtype="float32")  # adjust dimension if needed

def build_index():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        entries = json.load(f)

    texts = [entry["text"] for entry in entries]
    vectors = embed_texts(texts)

    if vectors.size == 0:
        print("No vectors generated. Exiting.")
        return

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)

    print(f"Index built with {len(vectors)} entries.")

if __name__ == "__main__":
    build_index()
