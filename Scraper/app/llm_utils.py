import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_query_with_gemini(query: str) -> Dict[str, Any]:
    """Parse product query using Gemini AI to extract structured information."""
    prompt = f"""
    Extract product details from the following shopping query. Return ONLY valid JSON with these keys:
    - brand: string (product brand/manufacturer)
    - model: string (specific model name/number)
    - specs: string (key specifications like storage, color, size)
    - category: string (product category like smartphone, laptop, headphones)
    - keywords: array of strings (search keywords)
    
    Query: "{query}"
    
    Example format:
    {{
        "brand": "Apple",
        "model": "iPhone 16 Pro",
        "specs": "128GB",
        "category": "smartphone",
        "keywords": ["iPhone", "16", "Pro", "128GB", "Apple"]
    }}
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Remove markdown code blocks if present
        content = re.sub(r'```json\n?', '', content)
        content = re.sub(r'```\n?', '', content)
        
        data = json.loads(content)
        
        # Validate required fields
        if not isinstance(data, dict):
            raise ValueError("Response is not a dictionary")
            
        return data
        
    except Exception as e:
        print(f"Error parsing with Gemini: {e}")
        return fallback_parse(query)

def fallback_parse(query: str) -> Dict[str, Any]:
    """Fallback parser when Gemini API fails."""
    query_lower = query.lower()
    
    # Common brand patterns
    brands = {
        'apple': ['iphone', 'ipad', 'macbook', 'airpods'],
        'samsung': ['galaxy', 'note', 'tab'],
        'sony': ['wh-', 'wf-', 'playstation'],
        'boat': ['airdopes', 'rockerz'],
        'oneplus': ['nord', 'pro'],
        'google': ['pixel', 'nest'],
        'microsoft': ['surface', 'xbox'],
        'hp': ['pavilion', 'envy', 'spectre'],
        'dell': ['inspiron', 'xps', 'alienware'],
        'nike': ['air', 'zoom', 'react'],
        'adidas': ['ultraboost', 'nmd', 'stan smith']
    }
    
    # Category patterns
    categories = {
        'smartphone': ['iphone', 'galaxy', 'pixel', 'phone', 'mobile'],
        'laptop': ['macbook', 'laptop', 'notebook', 'thinkpad'],
        'headphones': ['airpods', 'airdopes', 'headphones', 'earbuds'],
        'tablet': ['ipad', 'tab', 'tablet'],
        'smartwatch': ['watch', 'series'],
        'shoes': ['nike', 'adidas', 'air', 'boost'],
        'gaming': ['playstation', 'xbox', 'nintendo'],
        'grocery': ['banana', 'apple', 'orange', 'milk', 'bread', 'egg', 'organic', 'fresh']
    }
    
    detected_brand = None
    detected_category = None
    
    # Detect brand
    for brand, products in brands.items():
        if brand in query_lower or any(prod in query_lower for prod in products):
            detected_brand = brand.title()
            break
    
    # Detect category
    for category, keywords in categories.items():
        if any(keyword in query_lower for keyword in keywords):
            detected_category = category
            break
    
    # Extract model and specs - clean up punctuation
    words = re.findall(r'\b[\w\d]+\b', query)  # Extract words and numbers only
    model_parts = []
    specs_parts = []
    
    for word in words:
        if re.match(r'\d+gb', word.lower()):
            specs_parts.append(word)
        elif re.match(r'\d+', word):
            model_parts.append(word)
        elif word.lower() not in ['the', 'a', 'an', 'and', 'or', 'for']:
            model_parts.append(word)
    
    return {
        "brand": detected_brand or "",
        "model": " ".join(model_parts[:3]),  # Limit to first 3 parts
        "specs": " ".join(specs_parts),
        "category": detected_category or "general",
        "keywords": words[:5]  # First 5 words as keywords
    }

def parse_query_with_llm(query: str) -> Dict[str, Any]:
    """Main parsing function that tries Gemini first, then falls back."""
    if os.getenv("GOOGLE_API_KEY"):
        return parse_query_with_gemini(query)
    else:
        print("No Google API key found, using fallback parser")
        return fallback_parse(query)
