#!/usr/bin/env python3

import requests
import json
import sys

def test_api():
    """Test the price comparison API."""
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test countries endpoint
    print("\nTesting countries endpoint...")
    try:
        response = requests.get(f"{base_url}/countries")
        print(f"Countries: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Countries check failed: {e}")
    
    # Test price comparison - US iPhone
    print("\nTesting price comparison - US iPhone...")
    try:
        data = {
            "country": "US",
            "query": "iPhone 16 Pro, 128GB"
        }
        response = requests.post(f"{base_url}/compare", json=data)
        print(f"Price comparison: {response.status_code}")
        result = response.json()
        print(f"Results found: {result.get('total_results', 0)}")
        
        if result.get('results'):
            print("Sample results:")
            for i, offer in enumerate(result['results'][:3]):
                print(f"  {i+1}. {offer.get('productName', 'N/A')} - {offer.get('price', 'N/A')} {offer.get('currency', 'N/A')} ({offer.get('source', 'N/A')})")
        else:
            print("No results found")
            
    except Exception as e:
        print(f"Price comparison failed: {e}")
        return False
    
    # Test price comparison - India boAt
    print("\nTesting price comparison - India boAt...")
    try:
        data = {
            "country": "IN",
            "query": "boAt Airdopes 311 Pro"
        }
        response = requests.post(f"{base_url}/compare", json=data)
        print(f"Price comparison: {response.status_code}")
        result = response.json()
        print(f"Results found: {result.get('total_results', 0)}")
        
        if result.get('results'):
            print("Sample results:")
            for i, offer in enumerate(result['results'][:3]):
                print(f"  {i+1}. {offer.get('productName', 'N/A')} - {offer.get('price', 'N/A')} {offer.get('currency', 'N/A')} ({offer.get('source', 'N/A')})")
        else:
            print("No results found")
            
    except Exception as e:
        print(f"Price comparison failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Universal Price Comparison Tool - API Test")
    print("=" * 50)
    
    success = test_api()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ API tests completed successfully!")
    else:
        print("❌ API tests failed!")
        sys.exit(1)
