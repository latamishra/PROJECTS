from app.llm_utils import parse_query_with_llm
from app.mock_data import generate_mock_offers

# Test banana parsing
queries = ["bananas", "organic bananas", "fresh bananas"]

for query in queries:
    print(f"\n=== Testing: {query} ===")
    product_info = parse_query_with_llm(query)
    product_info['country'] = 'US'
    print(f"Parsed: {product_info}")
    
    # Test mock data generation
    mock_offers = generate_mock_offers(product_info)
    print(f"Mock offers: {len(mock_offers)}")
    for offer in mock_offers[:2]:
        print(f"  - {offer['productName'][:50]}... - {offer['price']} {offer['currency']}")
