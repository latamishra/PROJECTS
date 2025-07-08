from app.llm_utils import parse_query_with_llm

# Check the parsing for both queries
queries = ["iPhone 16 Pro, 128GB", "boAt Airdopes 311 Pro"]

for query in queries:
    print(f"\n=== Parsing: {query} ===")
    product_info = parse_query_with_llm(query)
    print(f"Parsed: {product_info}")
    
    # Build the query string as done in mock_data.py
    query_str = f"{product_info.get('brand', '')} {product_info.get('model', '')} {product_info.get('specs', '')}".strip()
    print(f"Query string for mock data: '{query_str}'")
    print(f"iPhone check: {'iphone' in query_str.lower() and '16 pro' in query_str.lower()}")
    print(f"boAt check: {'boat' in query_str.lower() and 'airdopes' in query_str.lower()}")
