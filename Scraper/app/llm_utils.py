import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Now you can access the API key securely
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_query_with_gemini(query: str):
    prompt = (
        "Extract the product details from the following shopping query. "
        "Return as JSON with keys: brand, model, specs (as string), category (if possible). "
        f'Query: "{query}"'
    )
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    import json
    try:
        content = response.text.strip()
        data = json.loads(content)
    except Exception:
        data = {"raw": content}
    return data

def parse_query_with_llm(query: str):
    # Example dummy implementation
    return {
        "brand": "Apple",
        "model": "iPhone 16 Pro",
        "specs": "128GB",
        "category": "smartphone"
    }
