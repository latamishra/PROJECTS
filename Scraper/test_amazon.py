from app.scraper import scrape_amazon
from app.llm_utils import parse_query_with_llm

# Test Amazon scraping directly
query = "iPhone 16 Pro, 128GB"
product_info = parse_query_with_llm(query)
product_info['country'] = 'US'

print(f"Testing Amazon scraping with product_info: {product_info}")

offers = scrape_amazon(product_info)
print(f"Amazon returned {len(offers)} offers")
for offer in offers:
    print(f"  - {offer}")
