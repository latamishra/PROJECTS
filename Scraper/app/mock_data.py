# app/mock_data.py

from typing import List, Dict, Any
import random
from app.retailers import get_currency_for_country

def generate_mock_offers(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate mock offers for demonstration purposes."""
    country = product_info.get('country', 'US')
    query = f"{product_info.get('brand', '')} {product_info.get('model', '')} {product_info.get('specs', '')}".strip()
    currency = get_currency_for_country(country)
    
    print(f"Generating mock data for: {query} (country: {country})")
    
    # Sample mock data based on the query
    mock_offers = []
    
    # iPhone examples
    if 'iphone' in query.lower() and '16 pro' in query.lower():
        print("Matched iPhone 16 Pro pattern")
        if country == 'US':
            mock_offers = [
                {
                    "link": "https://www.amazon.com/dp/B0D3J7DKLV",
                    "price": "999.99",
                    "currency": "USD",
                    "productName": "Apple iPhone 16 Pro 128GB Natural Titanium",
                    "source": "Amazon US"
                },
                {
                    "link": "https://www.bestbuy.com/site/apple-iphone-16-pro/6588348.p",
                    "price": "1049.99",
                    "currency": "USD",
                    "productName": "Apple iPhone 16 Pro 128GB - Natural Titanium",
                    "source": "BestBuy"
                },
                {
                    "link": "https://www.walmart.com/ip/Apple-iPhone-16-Pro/12345",
                    "price": "1099.99",
                    "currency": "USD",
                    "productName": "Apple iPhone 16 Pro 128GB Natural Titanium Unlocked",
                    "source": "Walmart"
                }
            ]
    
    # boAt examples
    elif 'boat' in query.lower() and 'airdopes' in query.lower():
        print("Matched boAt Airdopes pattern")
        if country == 'IN':
            mock_offers = [
                {
                    "link": "https://www.amazon.in/boAt-Airdopes-311-Pro/dp/B09EXAMPLE",
                    "price": "2999",
                    "currency": "INR",
                    "productName": "boAt Airdopes 311 Pro TWS Earbuds",
                    "source": "Amazon IN"
                },
                {
                    "link": "https://www.flipkart.com/boat-airdopes-311-pro/p/itm123456",
                    "price": "2799",
                    "currency": "INR",
                    "productName": "boAt Airdopes 311 Pro True Wireless Earbuds",
                    "source": "Flipkart"
                },
                {
                    "link": "https://www.croma.com/boat-airdopes-311-pro/p/12345",
                    "price": "3199",
                    "currency": "INR",
                    "productName": "boAt Airdopes 311 Pro Bluetooth Earbuds",
                    "source": "Croma"
                }
            ]
    
    # Grocery/Food examples
    elif any(food in query.lower() for food in ['banana', 'apple', 'orange', 'milk', 'bread', 'egg', 'organic']):
        print("Matched grocery/food pattern")
        base_retailers = get_retailers_for_country_mock(country)
        grocery_retailers = [
            f"Walmart {country}", f"Target {country}", f"Whole Foods {country}",
            f"Kroger {country}", f"Safeway {country}", f"Amazon Fresh {country}"
        ]
        
        # Use grocery-specific retailers for food items
        if country == 'US':
            retailers = grocery_retailers[:4]
        else:
            retailers = base_retailers[:4]
        
        # Generate realistic grocery prices
        base_price = 2.99 if 'banana' in query.lower() else 4.99
        prices = [base_price, base_price * 1.2, base_price * 0.8, base_price * 1.5]
        
        for i, (retailer, price) in enumerate(zip(retailers, prices)):
            mock_offers.append({
                "link": f"https://www.{retailer.lower().replace(' ', '')}.com/grocery/{query.replace(' ', '-')}/{i+1}",
                "price": f"{price:.2f}",
                "currency": currency,
                "productName": f"{query.title()} - {retailer} Fresh Produce",
                "source": retailer
            })
    
    # Samsung examples
    elif 'samsung' in query.lower() and 'galaxy' in query.lower():
        print("Matched Samsung Galaxy pattern")
        if country == 'GB':
            mock_offers = [
                {
                    "link": "https://www.amazon.co.uk/Samsung-Galaxy-S24-Ultra/dp/B0C12345",
                    "price": "1199.99",
                    "currency": "GBP",
                    "productName": "Samsung Galaxy S24 Ultra 256GB Phantom Black",
                    "source": "Amazon GB"
                },
                {
                    "link": "https://www.currys.co.uk/samsung-galaxy-s24-ultra",
                    "price": "1149.99",
                    "currency": "GBP",
                    "productName": "Samsung Galaxy S24 Ultra 256GB",
                    "source": "Currys"
                }
            ]
    
    # Generic fallback for any query
    if not mock_offers:
        print("No specific pattern matched, generating generic mock data")
        brand = product_info.get('brand', 'Generic')
        model = product_info.get('model', 'Product')
        specs = product_info.get('specs', '')
        
        product_name = f"{brand} {model} {specs}".strip()
        
        # Generate 3 generic offers
        retailers = get_retailers_for_country_mock(country)
        prices = generate_mock_prices(country)
        
        for i, (retailer, price) in enumerate(zip(retailers[:3], prices[:3])):
            mock_offers.append({
                "link": f"https://www.{retailer.lower().replace(' ', '')}.com/product/{i+1}",
                "price": str(price),
                "currency": currency,
                "productName": f"{product_name} - {retailer} Exclusive",
                "source": retailer
            })
    
    print(f"Generated {len(mock_offers)} mock offers")
    return mock_offers

def get_retailers_for_country_mock(country: str) -> List[str]:
    """Get mock retailer names for a country."""
    retailer_map = {
        'US': ['Amazon US', 'BestBuy', 'Walmart', 'Target'],
        'IN': ['Amazon IN', 'Flipkart', 'Myntra', 'Croma'],
        'GB': ['Amazon GB', 'Currys', 'Argos', 'John Lewis'],
        'DE': ['Amazon DE', 'MediaMarkt', 'Conrad', 'Saturn'],
        'FR': ['Amazon FR', 'Fnac', 'Cdiscount', 'Darty'],
        'CA': ['Amazon CA', 'Best Buy CA', 'Walmart CA', 'Canadian Tire'],
        'AU': ['Amazon AU', 'Harvey Norman', 'JB Hi-Fi', 'Big W'],
        'JP': ['Amazon JP', 'Rakuten', 'Yodobashi', 'Bic Camera'],
        'CN': ['Tmall', 'JD.com', 'Suning', 'Gome'],
        'BR': ['Amazon BR', 'MercadoLivre', 'Americanas', 'Shoptime'],
        'MX': ['Amazon MX', 'MercadoLibre', 'Liverpool', 'Palacio de Hierro']
    }
    return retailer_map.get(country, ['Amazon', 'Local Store', 'Online Shop', 'Retailer'])

def generate_mock_prices(country: str) -> List[float]:
    """Generate mock prices based on country."""
    # Base prices with country-specific adjustments
    base_prices = [99.99, 149.99, 199.99, 249.99, 299.99]
    
    # Country-specific multipliers (rough approximation)
    multipliers = {
        'US': 1.0,
        'IN': 80.0,    # USD to INR rough conversion
        'GB': 0.85,    # USD to GBP rough conversion
        'DE': 0.95,    # USD to EUR rough conversion
        'FR': 0.95,    # USD to EUR rough conversion
        'CA': 1.35,    # USD to CAD rough conversion
        'AU': 1.55,    # USD to AUD rough conversion
        'JP': 110.0,   # USD to JPY rough conversion
        'CN': 7.0,     # USD to CNY rough conversion
        'BR': 5.0,     # USD to BRL rough conversion
        'MX': 18.0     # USD to MXN rough conversion
    }
    
    multiplier = multipliers.get(country, 1.0)
    return [round(price * multiplier, 2) for price in base_prices]
