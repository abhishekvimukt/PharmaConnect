#!/usr/bin/env python3
"""
Test script for the catalog_ai API endpoint
"""

import requests
import json

def test_catalog_api():
    """Test the catalog API endpoint"""
    
    # API endpoint URL (adjust if your server runs on different port)
    base_url = "http://localhost:8000"
    api_url = f"{base_url}/catalog_ai/query/"
    
    # Sample queries an MR might ask
    test_queries = [
        "What is Paracetamol used for?",
        "Tell me about Aspirin dosage",
        "What are the side effects of Ibuprofen?",
        "How should I take Omeprazole?",
        "What is the price of Amoxicillin?"
    ]
    
    print("🌐 Testing Catalog AI API Endpoint")
    print("=" * 50)
    print(f"API URL: {api_url}")
    print()
    
    for i, query in enumerate(test_queries, 1):
        print(f"📝 Query {i}: {query}")
        print("-" * 40)
        
        try:
            # Make POST request to the API
            response = requests.post(
                api_url,
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {result.get('response', 'No response')}")
            else:
                print(f"❌ Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure your Django server is running!")
            print("Run: python manage.py runserver")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
        print()

if __name__ == "__main__":
    test_catalog_api() 