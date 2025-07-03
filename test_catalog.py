#!/usr/bin/env python3
"""
Test script for the catalog_ai RAG system
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr_optimizer_db.settings')
django.setup()

from catalog_ai.query_rag import ask_ai

def test_catalog_queries():
    """Test various medicine catalog queries"""
    
    # Sample queries an MR might ask
    test_queries = [
        "What is Paracetamol used for?",
        "Tell me about Aspirin dosage",
        "What are the side effects of Ibuprofen?",
        "How should I take Omeprazole?",
        "What is the price of Amoxicillin?",
        "Tell me about diabetes medications",
        "What are pain relief options?",
        "How to use inhalers for asthma?"
    ]
    
    print("🧪 Testing Catalog AI RAG System")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 30)
        
        try:
            response = ask_ai(query)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    # Check if HUGGINGFACE_API_KEY is set
    if not os.getenv("HUGGINGFACE_API_KEY"):
        print("❌ HUGGINGFACE_API_KEY not found in environment variables!")
        print("Please set your HuggingFace API key:")
        print("1. Create a .env file in the project root")
        print("2. Add: HUGGINGFACE_API_KEY=your_api_key_here")
        print("3. Or set it as an environment variable")
        sys.exit(1)
    
    # Check if FAISS index exists
    if not os.path.exists("catalog_ai/medicine_index.faiss"):
        print("❌ FAISS index not found!")
        print("Please run: python catalog_ai/load_catalog.py")
        sys.exit(1)
    
    test_catalog_queries() 