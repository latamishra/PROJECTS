from app.mock_data import generate_mock_offers
from app.llm_utils import parse_query_with_llm

# Test mock data generation
query = "iPhone 16 Pro, 128GB"
product_info = parse_query_with_llm(query)
product_info['country'] = 'US'

print(f"Testing mock data generation with product_info: {product_info}")

mock_offers = generate_mock_offers(product_info)
print(f"Mock data returned {len(mock_offers)} offers")
for offer in mock_offers:
    print(f"  - {offer}")
