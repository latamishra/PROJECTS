# app/scraper.py

import re
import time
import random
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode, quote_plus
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from fuzzywuzzy import fuzz
from tenacity import retry, stop_after_attempt, wait_exponential

# Constants
MAX_RESULTS_PER_SITE = 10
REQUEST_TIMEOUT = 30
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

def get_random_user_agent() -> str:
    """Get a random user agent."""
    return random.choice(USER_AGENTS)

def clean_price(price_text: str) -> str:
    """Clean price text and extract numeric value."""
    if not price_text:
        return ""
    
    # Remove currency symbols and extract numbers
    price_clean = re.sub(r'[^\d.,]', '', price_text)
    price_clean = re.sub(r'[,]', '', price_clean)  # Remove commas
    
    # Extract first number (price)
    match = re.search(r'[\d.]+', price_clean)
    return match.group() if match else ""

def is_product_match(product_name: str, query_info: Dict[str, Any], threshold: int = 60) -> bool:
    """Check if product name matches the query using fuzzy matching."""
    if not product_name:
        return False
    
    product_name_lower = product_name.lower()
    
    # Check brand match - this is crucial
    brand = query_info.get('brand', '').lower()
    if brand and brand not in product_name_lower:
        print(f"Brand mismatch: '{brand}' not in '{product_name_lower}'")
        return False
    
    # Check model match - for specific models, this is also crucial
    model = query_info.get('model', '').lower()
    if model:
        # Remove common punctuation from model
        model_clean = re.sub(r'[,.]', '', model)
        model_words = model_clean.split()
        
        # Check if all significant model words are present
        significant_words = [word for word in model_words if len(word) > 2 or word.isdigit()]
        if significant_words:
            matches = sum(1 for word in significant_words if word in product_name_lower)
            if matches < len(significant_words) * 0.5:  # At least 50% of model words should match
                print(f"Model mismatch: '{model}' vs '{product_name_lower}' - {matches}/{len(significant_words)} words match")
                return False
    
    # Check specs match
    specs = query_info.get('specs', '').lower()
    if specs:
        # For capacity/storage specs, be more flexible
        if 'gb' in specs or 'tb' in specs:
            # Extract capacity from specs
            capacity_match = re.search(r'(\d+)\s*(gb|tb)', specs)
            if capacity_match:
                capacity = capacity_match.group(1)
                if capacity not in product_name_lower:
                    print(f"Capacity mismatch: '{capacity}' not in '{product_name_lower}'")
                    # Don't return False here, as capacity might be mentioned differently
    
    # Use fuzzy matching for overall similarity
    query_text = f"{brand} {model} {specs}".strip()
    similarity = fuzz.partial_ratio(query_text, product_name_lower)
    
    print(f"Similarity score: {similarity} (threshold: {threshold})")
    return similarity >= threshold

def get_country_domain(country_code: str, base_domain: str) -> str:
    """Get the appropriate domain for a country."""
    domain_map = {
        'amazon': {
            'US': 'amazon.com',
            'IN': 'amazon.in',
            'GB': 'amazon.co.uk',
            'DE': 'amazon.de',
            'FR': 'amazon.fr',
            'CA': 'amazon.ca',
            'AU': 'amazon.com.au',
            'JP': 'amazon.co.jp',
            'BR': 'amazon.com.br',
            'MX': 'amazon.com.mx',
            'SG': 'amazon.sg'
        },
        'ebay': {
            'US': 'ebay.com',
            'GB': 'ebay.co.uk',
            'DE': 'ebay.de',
            'FR': 'ebay.fr',
            'CA': 'ebay.ca',
            'AU': 'ebay.com.au',
            'JP': 'ebay.co.jp'
        }
    }
    
    return domain_map.get(base_domain, {}).get(country_code, f"{base_domain}.com")

def get_currency_for_country(country_code: str) -> str:
    """Get currency for country."""
    currency_map = {
        'US': 'USD', 'IN': 'INR', 'GB': 'GBP', 'DE': 'EUR', 'FR': 'EUR',
        'CA': 'CAD', 'AU': 'AUD', 'JP': 'JPY', 'BR': 'BRL', 'MX': 'MXN',
        'SG': 'SGD', 'MY': 'MYR', 'TH': 'THB', 'ID': 'IDR', 'PH': 'PHP',
        'VN': 'VND', 'CN': 'CNY', 'KR': 'KRW', 'CH': 'CHF', 'SE': 'SEK',
        'NO': 'NOK', 'DK': 'DKK', 'FI': 'EUR', 'NL': 'EUR', 'BE': 'EUR',
        'AT': 'EUR', 'IT': 'EUR', 'ES': 'EUR'
    }
    return currency_map.get(country_code, 'USD')

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def make_request(url: str, headers: Optional[Dict] = None) -> requests.Response:
    """Make HTTP request with retry logic."""
    if headers is None:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
    
    print(f"Making request to: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        print(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise

# Amazon Scraper
def scrape_amazon(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Amazon for product prices."""
    country = product_info.get('country', 'US')
    domain = get_country_domain(country, 'amazon')
    currency = get_currency_for_country(country)
    
    # Build search query
    query_parts = [
        product_info.get('brand', ''),
        product_info.get('model', ''),
        product_info.get('specs', '')
    ]
    search_query = ' '.join(filter(None, query_parts))
    
    if not search_query.strip():
        return []
    
    amazon_url = f"https://www.{domain}/s?k={quote_plus(search_query)}"
    print(f"Scraping Amazon {country}: {amazon_url}")
    
    # First try with requests
    try:
        response = make_request(amazon_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        offers = []
        # Look for product containers with various possible selectors
        product_selectors = [
            '[data-component-type="s-search-result"]',
            '.s-result-item',
            '.s-asin',
            '[data-asin]'
        ]
        
        products = []
        for selector in product_selectors:
            products = soup.select(selector)
            if products:
                print(f"Found {len(products)} products using selector: {selector}")
                break
        
        if not products:
            print("No products found with requests, trying with Playwright...")
            return scrape_amazon_playwright(product_info)
        
        for product in products[:MAX_RESULTS_PER_SITE]:
            try:
                # Multiple selectors for product name
                name_selectors = [
                    'h2 a span',
                    '.a-size-medium span',
                    '.a-text-normal',
                    'h2 span',
                    '.s-link-style span',
                    'span[data-component-type="s-search-result"] h2 a span'
                ]
                
                product_name = ""
                for selector in name_selectors:
                    name_element = product.select_one(selector)
                    if name_element:
                        product_name = name_element.get_text(strip=True)
                        break
                
                # Multiple selectors for price
                price_selectors = [
                    '.a-price .a-offscreen',
                    '.a-price-whole',
                    '.a-price-range',
                    '.a-price',
                    'span.a-price-whole',
                    'span.a-price.a-text-price.a-size-medium.apexPriceToPay',
                    '.a-price-range .a-offscreen',
                    '.a-price .a-price-whole',
                    '.a-price .a-price-fraction',
                    '.a-color-price',
                    '.a-price-symbol',
                    '[data-cy="price-recipe"]',
                    '.a-text-price',
                    '.a-size-medium.a-color-price',
                    '.a-size-base.a-color-price',
                    '.a-size-small.a-color-price'
                ]
                
                price_text = ""
                for selector in price_selectors:
                    price_element = product.select_one(selector)
                    if price_element:
                        price_text = price_element.get_text(strip=True)
                        print(f"Found price with selector '{selector}': {price_text}")
                        break
                
                # If no price found, try to find any text that looks like a price
                if not price_text:
                    all_text = product.get_text()
                    price_matches = re.findall(r'\$[\d,]+\.?\d*', all_text)
                    if price_matches:
                        price_text = price_matches[0]
                        print(f"Found price via regex: {price_text}")
                
                # Debug: print all text if no price found
                if not price_text:
                    print(f"No price found for product. All text: {product.get_text()[:200]}...")
                    # Try to find any span with dollar signs or numbers
                    price_spans = product.find_all('span', string=re.compile(r'[\$\d]'))
                    for span in price_spans[:5]:  # Check first 5 spans
                        text = span.get_text(strip=True)
                        if re.search(r'\$[\d,]+\.?\d*', text):
                            price_text = text
                            print(f"Found price in span: {price_text}")
                            break
                
                # Multiple selectors for link
                link_selectors = [
                    'h2 a',
                    '.a-link-normal',
                    'a[href*="/dp/"]',
                    'a[href*="/gp/"]'
                ]
                
                link = ""
                for selector in link_selectors:
                    link_element = product.select_one(selector)
                    if link_element and link_element.get('href'):
                        href = link_element['href']
                        link = f"https://www.{domain}{href}" if href.startswith('/') else href
                        break
                
                if product_name and price_text:
                    print(f"Found product: {product_name[:50]}... - {price_text}")
                    # Check if product matches query
                    if is_product_match(product_name, product_info):
                        price_clean = clean_price(price_text)
                        
                        if price_clean:
                            offers.append({
                                "link": link or amazon_url,
                                "price": price_clean,
                                "currency": currency,
                                "productName": product_name,
                                "source": f"Amazon {country}"
                            })
                        else:
                            print(f"Could not clean price: {price_text}")
                    else:
                        print(f"Product does not match query: {product_name[:50]}...")
                else:
                    if not product_name:
                        print("No product name found")
                    if not price_text:
                        print("No price text found")
                
            except Exception as e:
                print(f"Error processing Amazon product: {e}")
                continue
        
        print(f"Amazon scraper returning {len(offers)} offers")
        return offers[:MAX_RESULTS_PER_SITE]
        
    except Exception as e:
        print(f"Error scraping Amazon with requests: {e}")
        print("Falling back to Playwright scraper...")
        return scrape_amazon_playwright(product_info)

def scrape_amazon_playwright(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fallback Amazon scraper using Playwright."""
    country = product_info.get('country', 'US')
    domain = get_country_domain(country, 'amazon')
    currency = get_currency_for_country(country)
    
    query_parts = [
        product_info.get('brand', ''),
        product_info.get('model', ''),
        product_info.get('specs', '')
    ]
    search_query = ' '.join(filter(None, query_parts))
    
    if not search_query.strip():
        return []
    
    amazon_url = f"https://www.{domain}/s?k={quote_plus(search_query)}"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_extra_http_headers({'User-Agent': get_random_user_agent()})
            
            # Set a shorter timeout
            page.set_default_timeout(15000)
            
            page.goto(amazon_url, wait_until='domcontentloaded')
            
            # Wait briefly for content to load
            try:
                page.wait_for_selector('h2', timeout=10000)
            except:
                pass  # Continue even if selector not found
            
            # Get page content and use BeautifulSoup for parsing
            content = page.content()
            browser.close()
            
            soup = BeautifulSoup(content, 'html.parser')
            offers = []
            
            # Look for any products on the page
            products = soup.find_all(['div', 'article'], limit=20)
            
            for product in products:
                try:
                    # Look for text that might be product names
                    text_elements = product.find_all(['h1', 'h2', 'h3', 'span', 'a'], string=True)
                    product_name = ""
                    
                    for elem in text_elements:
                        text = elem.get_text(strip=True)
                        if len(text) > 10 and any(word in text.lower() for word in search_query.lower().split()):
                            product_name = text
                            break
                    
                    if product_name and len(offers) < 5:
                        # Create a basic offer even without price
                        offers.append({
                            "link": amazon_url,
                            "price": "0",  # Placeholder price
                            "currency": currency,
                            "productName": product_name,
                            "source": f"Amazon {country}"
                        })
                
                except Exception as e:
                    continue
            
            return offers[:MAX_RESULTS_PER_SITE]
            
    except Exception as e:
        print(f"Error scraping Amazon with Playwright: {e}")
        return []

# eBay Scraper
def scrape_ebay(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape eBay for product prices."""
    country = product_info.get('country', 'US')
    domain = get_country_domain(country, 'ebay')
    currency = get_currency_for_country(country)
    
    query_parts = [
        product_info.get('brand', ''),
        product_info.get('model', ''),
        product_info.get('specs', '')
    ]
    search_query = ' '.join(filter(None, query_parts))
    
    if not search_query.strip():
        return []
    
    ebay_url = f"https://www.{domain}/sch/i.html?_nkw={quote_plus(search_query)}"
    
    try:
        response = make_request(ebay_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        offers = []
        items = soup.find_all('div', class_='s-item')
        
        for item in items[:MAX_RESULTS_PER_SITE]:
            try:
                # Get product name
                title_element = item.find('h3', class_='s-item__title')
                if not title_element:
                    continue
                
                product_name = title_element.get_text(strip=True)
                
                # Get price
                price_element = item.find('span', class_='s-item__price')
                if not price_element:
                    continue
                
                price_text = price_element.get_text(strip=True)
                
                # Get link
                link_element = item.find('a', class_='s-item__link')
                if not link_element:
                    continue
                
                link = link_element.get('href', '')
                
                if product_name and price_text and link:
                    if is_product_match(product_name, product_info):
                        price_clean = clean_price(price_text)
                        
                        if price_clean:
                            offers.append({
                                "link": link,
                                "price": price_clean,
                                "currency": currency,
                                "productName": product_name,
                                "source": f"eBay {country}"
                            })
            
            except Exception as e:
                print(f"Error processing eBay item: {e}")
                continue
        
        return offers[:MAX_RESULTS_PER_SITE]
        
    except Exception as e:
        print(f"Error scraping eBay: {e}")
        return []

# Flipkart Scraper (India)
def scrape_flipkart(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Flipkart for product prices."""
    query_parts = [
        product_info.get('brand', ''),
        product_info.get('model', ''),
        product_info.get('specs', '')
    ]
    search_query = ' '.join(filter(None, query_parts))
    
    if not search_query.strip():
        return []
    
    flipkart_url = f"https://www.flipkart.com/search?q={quote_plus(search_query)}"
    
    try:
        response = make_request(flipkart_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        offers = []
        # Multiple possible selectors for Flipkart products
        product_selectors = [
            'div[data-id]',
            '._1AtVbE',
            '._13oc-S',
            '._2kHMtA'
        ]
        
        items = []
        for selector in product_selectors:
            items = soup.select(selector)
            if items:
                break
        
        for item in items[:MAX_RESULTS_PER_SITE]:
            try:
                # Get product name
                name_selectors = ['._4rR01T', '.s1Q9rs', '._2WkVRV', 'a._1fQZEK']
                product_name = ""
                
                for selector in name_selectors:
                    name_element = item.select_one(selector)
                    if name_element:
                        product_name = name_element.get_text(strip=True)
                        break
                
                # Get price
                price_selectors = ['._30jeq3', '._1_WHN1', '.Nx9bqj', '._3tbr2p']
                price_text = ""
                
                for selector in price_selectors:
                    price_element = item.select_one(selector)
                    if price_element:
                        price_text = price_element.get_text(strip=True)
                        break
                
                # Get link
                link_element = item.select_one('a._1fQZEK, a._2UzuFa')
                link = ""
                if link_element and link_element.get('href'):
                    link = "https://www.flipkart.com" + link_element['href']
                
                if product_name and price_text and link:
                    if is_product_match(product_name, product_info):
                        price_clean = clean_price(price_text)
                        
                        if price_clean:
                            offers.append({
                                "link": link,
                                "price": price_clean,
                                "currency": "INR",
                                "productName": product_name,
                                "source": "Flipkart"
                            })
            
            except Exception as e:
                print(f"Error processing Flipkart item: {e}")
                continue
        
        return offers[:MAX_RESULTS_PER_SITE]
        
    except Exception as e:
        print(f"Error scraping Flipkart: {e}")
        return []

# Generic scrapers for other sites
def scrape_bestbuy(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape BestBuy for product prices."""
    return _scrape_generic_site(
        product_info,
        "https://www.bestbuy.com/site/searchpage.jsp?st={}",
        {
            'product_selector': '.sku-item',
            'name_selector': '.sku-title a',
            'price_selector': '.pricing-current-price',
            'link_selector': '.sku-title a'
        },
        "BestBuy",
        "USD"
    )

def scrape_walmart(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Walmart for product prices."""
    return _scrape_generic_site(
        product_info,
        "https://www.walmart.com/search/?query={}",
        {
            'product_selector': '[data-automation-id="product-title"]',
            'name_selector': 'span',
            'price_selector': '[data-automation-id="product-price"]',
            'link_selector': 'a'
        },
        "Walmart",
        get_currency_for_country(product_info.get('country', 'US'))
    )

def scrape_target(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Target for product prices."""
    return _scrape_generic_site(
        product_info,
        "https://www.target.com/s?searchTerm={}",
        {
            'product_selector': '[data-test="product-details"]',
            'name_selector': 'a',
            'price_selector': '[data-test="product-price"]',
            'link_selector': 'a'
        },
        "Target",
        "USD"
    )

def _scrape_generic_site(product_info: Dict[str, Any], url_template: str, 
                        selectors: Dict[str, str], site_name: str, currency: str) -> List[Dict[str, Any]]:
    """Generic scraper for simple sites."""
    query_parts = [
        product_info.get('brand', ''),
        product_info.get('model', ''),
        product_info.get('specs', '')
    ]
    search_query = ' '.join(filter(None, query_parts))
    
    if not search_query.strip():
        return []
    
    url = url_template.format(quote_plus(search_query))
    
    try:
        response = make_request(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        offers = []
        items = soup.select(selectors['product_selector'])
        
        for item in items[:MAX_RESULTS_PER_SITE]:
            try:
                name_element = item.select_one(selectors['name_selector'])
                price_element = item.select_one(selectors['price_selector'])
                link_element = item.select_one(selectors['link_selector'])
                
                if name_element and price_element:
                    product_name = name_element.get_text(strip=True)
                    price_text = price_element.get_text(strip=True)
                    link = link_element.get('href', '') if link_element else ""
                    
                    if is_product_match(product_name, product_info):
                        price_clean = clean_price(price_text)
                        
                        if price_clean:
                            offers.append({
                                "link": link,
                                "price": price_clean,
                                "currency": currency,
                                "productName": product_name,
                                "source": site_name
                            })
            
            except Exception as e:
                print(f"Error processing {site_name} item: {e}")
                continue
        
        return offers[:MAX_RESULTS_PER_SITE]
        
    except Exception as e:
        print(f"Error scraping {site_name}: {e}")
        return []

# Placeholder scrapers for other sites
def scrape_myntra(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Myntra for product prices."""
    return []  # Implement as needed

def scrape_snapdeal(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Snapdeal for product prices."""
    return []  # Implement as needed

def scrape_paytm(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Paytm Mall for product prices."""
    return []  # Implement as needed

def scrape_croma(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Croma for product prices."""
    return []  # Implement as needed

def scrape_reliance_digital(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Reliance Digital for product prices."""
    return []  # Implement as needed

def scrape_currys(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Currys for product prices."""
    return []  # Implement as needed

def scrape_argos(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Argos for product prices."""
    return []  # Implement as needed

def scrape_john_lewis(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape John Lewis for product prices."""
    return []  # Implement as needed

def scrape_conrad(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Conrad for product prices."""
    return []  # Implement as needed

def scrape_mediamarkt(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape MediaMarkt for product prices."""
    return []  # Implement as needed

def scrape_fnac(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Fnac for product prices."""
    return []  # Implement as needed

def scrape_cdiscount(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Cdiscount for product prices."""
    return []  # Implement as needed

def scrape_rakuten(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Rakuten for product prices."""
    return []  # Implement as needed

def scrape_mercadolibre(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape MercadoLibre for product prices."""
    return []  # Implement as needed

def scrape_alibaba(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Alibaba for product prices."""
    return []  # Implement as needed

def scrape_tmall(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Tmall for product prices."""
    return []  # Implement as needed

def scrape_jd(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape JD.com for product prices."""
    return []  # Implement as needed

def scrape_shopee(product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scrape Shopee for product prices."""
    return []  # Implement as needed
