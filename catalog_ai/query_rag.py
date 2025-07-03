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

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not set in environment.")


_index = None
_entries = None

def get_index_and_entries():
    global _index, _entries
    if _index is None or _entries is None:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
        _index = faiss.read_index(INDEX_PATH)
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            _entries = json.load(f)
    return _index, _entries

def embed_query(query):
    co = cohere.Client(COHERE_API_KEY)
    response = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return np.array(response.embeddings[0], dtype="float32")

def ask_ai(query):
    index, entries = get_index_and_entries()
    query_vector = embed_query(query).reshape(1, -1)
    D, I = index.search(query_vector, k=3)
    context = "\n\n".join(entries[i]["text"] for i in I[0])

    prompt = f"""You are a helpful medical assistant. Based on the following context, answer the user's question.

Context:
{context}

Question: {query}
Answer:"""

    co = cohere.Client(COHERE_API_KEY)
    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=300000000,
        temperature=0.5
    )
    return response.generations[0].text.strip()

if __name__ == "__main__":
    print("🔍 Ask your medical query below (type 'exit' to quit):\n")
    while True:
        query = input("🧠 Your question: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("👋 Exiting.")
            break
        try:
            answer = ask_ai(query)
            print(f"\n💡 Answer: {answer}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")
