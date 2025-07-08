from app.mock_data import generate_mock_offers
from app.llm_utils import parse_query_with_llm

# Test mock data generation for boAt
query = "boAt Airdopes 311 Pro"
product_info = parse_query_with_llm(query)
product_info['country'] = 'IN'

print(f"Testing mock data generation for boAt with product_info: {product_info}")

mock_offers = generate_mock_offers(product_info)
print(f"Mock data returned {len(mock_offers)} offers")
for offer in mock_offers:
    print(f"  - {offer}")
