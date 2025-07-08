# app/retailers.py

from app.scraper import scrape_amazon, scrape_flipkart, scrape_bestbuy

COUNTRY_ALIASES = {
    "India": "IN",
    "United States": "US",
    "USA": "US",
    "UK": "GB",
    # add more as needed
}

RETAILER_REGISTRY = {
    "IN": [
        {"name": "Amazon IN", "scrape_func": scrape_amazon},
        {"name": "Flipkart", "scrape_func": scrape_flipkart},
    ],
    "US": [
        {"name": "Amazon US", "scrape_func": scrape_amazon},
        {"name": "BestBuy", "scrape_func": scrape_bestbuy},
    ],
    # add more as needed
}

def get_retailers_for_country(country_code):
    code = COUNTRY_ALIASES.get(country_code, country_code).upper()
    return RETAILER_REGISTRY.get(code, [])
