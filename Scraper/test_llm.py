from app.llm_utils import parse_query_with_llm

# Test LLM parsing
query = "iPhone 16 Pro, 128GB"
print(f"Testing LLM parsing for: {query}")

try:
    product_info = parse_query_with_llm(query)
    print(f"Parsed result: {product_info}")
except Exception as e:
    print(f"Error parsing: {e}")
