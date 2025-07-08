# app/retailers.py

from app.scraper import (
    scrape_amazon, scrape_flipkart, scrape_bestbuy, scrape_ebay,
    scrape_walmart, scrape_target, scrape_myntra, scrape_snapdeal,
    scrape_paytm, scrape_croma, scrape_reliance_digital, scrape_currys,
    scrape_argos, scrape_john_lewis, scrape_conrad, scrape_mediamarkt,
    scrape_fnac, scrape_cdiscount, scrape_rakuten, scrape_mercadolibre,
    scrape_alibaba, scrape_tmall, scrape_jd, scrape_shopee
)

COUNTRY_ALIASES = {
    "India": "IN",
    "United States": "US",
    "USA": "US",
    "America": "US",
    "UK": "GB",
    "United Kingdom": "GB",
    "Britain": "GB",
    "Germany": "DE",
    "Deutschland": "DE",
    "France": "FR",
    "Spain": "ES",
    "Italy": "IT",
    "Canada": "CA",
    "Australia": "AU",
    "Japan": "JP",
    "China": "CN",
    "Brazil": "BR",
    "Mexico": "MX",
    "Singapore": "SG",
    "Malaysia": "MY",
    "Thailand": "TH",
    "Indonesia": "ID",
    "Philippines": "PH",
    "Vietnam": "VN",
    "South Korea": "KR",
    "Netherlands": "NL",
    "Belgium": "BE",
    "Switzerland": "CH",
    "Austria": "AT",
    "Sweden": "SE",
    "Norway": "NO",
    "Denmark": "DK",
    "Finland": "FI",
}

RETAILER_REGISTRY = {
    "US": [
        {"name": "Amazon US", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "BestBuy", "scrape_func": scrape_bestbuy, "priority": 2},
        {"name": "Walmart", "scrape_func": scrape_walmart, "priority": 3},
        {"name": "Target", "scrape_func": scrape_target, "priority": 4},
        {"name": "eBay US", "scrape_func": scrape_ebay, "priority": 5},
    ],
    "IN": [
        {"name": "Amazon IN", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "Flipkart", "scrape_func": scrape_flipkart, "priority": 2},
        {"name": "Myntra", "scrape_func": scrape_myntra, "priority": 3},
        {"name": "Snapdeal", "scrape_func": scrape_snapdeal, "priority": 4},
        {"name": "Paytm Mall", "scrape_func": scrape_paytm, "priority": 5},
        {"name": "Croma", "scrape_func": scrape_croma, "priority": 6},
        {"name": "Reliance Digital", "scrape_func": scrape_reliance_digital, "priority": 7},
    ],
    "GB": [
        {"name": "Amazon UK", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "Currys", "scrape_func": scrape_currys, "priority": 2},
        {"name": "Argos", "scrape_func": scrape_argos, "priority": 3},
        {"name": "John Lewis", "scrape_func": scrape_john_lewis, "priority": 4},
        {"name": "eBay UK", "scrape_func": scrape_ebay, "priority": 5},
    ],
    "DE": [
        {"name": "Amazon DE", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "Conrad", "scrape_func": scrape_conrad, "priority": 2},
        {"name": "MediaMarkt", "scrape_func": scrape_mediamarkt, "priority": 3},
        {"name": "eBay DE", "scrape_func": scrape_ebay, "priority": 4},
    ],
    "FR": [
        {"name": "Amazon FR", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "Fnac", "scrape_func": scrape_fnac, "priority": 2},
        {"name": "Cdiscount", "scrape_func": scrape_cdiscount, "priority": 3},
        {"name": "eBay FR", "scrape_func": scrape_ebay, "priority": 4},
    ],
    "CA": [
        {"name": "Amazon CA", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "BestBuy CA", "scrape_func": scrape_bestbuy, "priority": 2},
        {"name": "Walmart CA", "scrape_func": scrape_walmart, "priority": 3},
        {"name": "eBay CA", "scrape_func": scrape_ebay, "priority": 4},
    ],
    "AU": [
        {"name": "Amazon AU", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "eBay AU", "scrape_func": scrape_ebay, "priority": 2},
    ],
    "JP": [
        {"name": "Amazon JP", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "Rakuten", "scrape_func": scrape_rakuten, "priority": 2},
        {"name": "eBay JP", "scrape_func": scrape_ebay, "priority": 3},
    ],
    "CN": [
        {"name": "Alibaba", "scrape_func": scrape_alibaba, "priority": 1},
        {"name": "Tmall", "scrape_func": scrape_tmall, "priority": 2},
        {"name": "JD.com", "scrape_func": scrape_jd, "priority": 3},
    ],
    "SG": [
        {"name": "Amazon SG", "scrape_func": scrape_amazon, "priority": 1},
        {"name": "Shopee SG", "scrape_func": scrape_shopee, "priority": 2},
    ],
    "MY": [
        {"name": "Shopee MY", "scrape_func": scrape_shopee, "priority": 1},
    ],
    "TH": [
        {"name": "Shopee TH", "scrape_func": scrape_shopee, "priority": 1},
    ],
    "ID": [
        {"name": "Shopee ID", "scrape_func": scrape_shopee, "priority": 1},
    ],
    "PH": [
        {"name": "Shopee PH", "scrape_func": scrape_shopee, "priority": 1},
    ],
    "VN": [
        {"name": "Shopee VN", "scrape_func": scrape_shopee, "priority": 1},
    ],
    "BR": [
        {"name": "MercadoLibre", "scrape_func": scrape_mercadolibre, "priority": 1},
        {"name": "Amazon BR", "scrape_func": scrape_amazon, "priority": 2},
    ],
    "MX": [
        {"name": "MercadoLibre MX", "scrape_func": scrape_mercadolibre, "priority": 1},
        {"name": "Amazon MX", "scrape_func": scrape_amazon, "priority": 2},
    ],
}

def get_retailers_for_country(country_code: str) -> list:
    """Get list of retailers for a specific country."""
    code = COUNTRY_ALIASES.get(country_code, country_code).upper()
    retailers = RETAILER_REGISTRY.get(code, [])
    
    # Sort by priority (lower number = higher priority)
    return sorted(retailers, key=lambda x: x.get('priority', 999))

def get_supported_countries() -> list:
    """Get list of all supported countries."""
    return list(RETAILER_REGISTRY.keys())

def get_currency_for_country(country_code: str) -> str:
    """Get the primary currency for a country."""
    currency_map = {
        "US": "USD", "IN": "INR", "GB": "GBP", "DE": "EUR", "FR": "EUR",
        "ES": "EUR", "IT": "EUR", "CA": "CAD", "AU": "AUD", "JP": "JPY",
        "CN": "CNY", "BR": "BRL", "MX": "MXN", "SG": "SGD", "MY": "MYR",
        "TH": "THB", "ID": "IDR", "PH": "PHP", "VN": "VND", "KR": "KRW",
        "NL": "EUR", "BE": "EUR", "CH": "CHF", "AT": "EUR", "SE": "SEK",
        "NO": "NOK", "DK": "DKK", "FI": "EUR"
    }
    code = COUNTRY_ALIASES.get(country_code, country_code).upper()
    return currency_map.get(code, "USD")
