import requests
import json

def test_api_endpoint(country, query):
    """Test the API endpoint with detailed logging"""
    url = "http://localhost:8000/compare"
    data = {"country": country, "query": query}
    
    print(f"\n=== Testing {country} - {query} ===")
    print(f"URL: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, json=data, timeout=120)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Keys: {list(result.keys())}")
            print(f"Results: {len(result.get('results', []))}")
            print(f"Total Results: {result.get('total_results', 0)}")
            print(f"Note: {result.get('note', 'None')}")
            
            if result.get('results'):
                print("Sample results:")
                for i, offer in enumerate(result['results'][:3]):
                    print(f"  {i+1}. {offer.get('productName', 'N/A')[:50]}...")
                    print(f"      Price: {offer.get('price', 'N/A')} {offer.get('currency', 'N/A')}")
                    print(f"      Source: {offer.get('source', 'N/A')}")
            else:
                print("No results found")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

# Test both queries
test_api_endpoint("US", "iPhone 16 Pro, 128GB")
test_api_endpoint("IN", "boAt Airdopes 311 Pro")
