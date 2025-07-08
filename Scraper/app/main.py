# app/main.py

import asyncio
import os
import re
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm_utils import parse_query_with_llm
from app.retailers import get_retailers_for_country, get_supported_countries, get_currency_for_country
from app.mock_data import generate_mock_offers
from fastapi.concurrency import run_in_threadpool
import concurrent.futures
from contextlib import asynccontextmanager
from mangum import Mangum

# Set the asyncio event loop policy immediately for Windows
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Universal Price Comparison Tool...")
    print(f"Supported countries: {get_supported_countries()}")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Universal Price Comparison Tool",
    description="A comprehensive tool to compare product prices across multiple websites and countries",
    version="1.0.0",
    lifespan=lifespan
)

handler = Mangum(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryInput(BaseModel):
    country: str
    query: str

class PriceComparisonResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_results: int
    country: str
    query: str
    supported_retailers: List[str]
    note: Optional[str] = None

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend HTML page."""
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "supported_countries": get_supported_countries()}

@app.get("/countries")
async def get_countries():
    """Get list of supported countries."""
    return {"countries": get_supported_countries()}

@app.post("/compare", response_model=PriceComparisonResponse)
async def compare_prices(input: QueryInput):
    """Main endpoint to compare prices across multiple retailers."""
    try:
        print(f"Received request - Country: {input.country}, Query: {input.query}")
        
        # Validate country
        if input.country.upper() not in get_supported_countries():
            raise HTTPException(
                status_code=400, 
                detail=f"Country '{input.country}' is not supported. Supported countries: {get_supported_countries()}"
            )
        
        # Parse query using LLM
        product_info = parse_query_with_llm(input.query)
        product_info['country'] = input.country.upper()
        
        print(f"Parsed product info: {product_info}")
        
        # Get retailers for the country
        retailers = get_retailers_for_country(input.country)
        print(f"Found {len(retailers)} retailers for {input.country}")
        
        if not retailers:
            raise HTTPException(
                status_code=404,
                detail=f"No retailers found for country '{input.country}'"
            )
        
        # Scrape prices from all retailers concurrently
        all_offers = []
        
        # Use ThreadPoolExecutor for concurrent scraping
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all scraping tasks
            future_to_retailer = {
                executor.submit(retailer["scrape_func"], product_info): retailer
                for retailer in retailers
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_retailer):
                retailer = future_to_retailer[future]
                try:
                    offers = future.result(timeout=60)  # 60 second timeout per retailer
                    print(f"Offers from {retailer['name']}: {len(offers)} found")
                    all_offers.extend(offers)
                except Exception as e:
                    print(f"Error scraping {retailer['name']}: {e}")
                    continue
        
        print(f"Total offers found: {len(all_offers)}")
        
        # If no real results, use mock data for demonstration
        if len(all_offers) == 0:
            print("No real results found, generating mock data for demonstration...")
            mock_offers = generate_mock_offers(product_info)
            all_offers.extend(mock_offers)
            print(f"Added {len(mock_offers)} mock offers")
        
        # Filter out invalid offers and clean prices
        valid_offers = []
        for offer in all_offers:
            try:
                # Ensure price is a string and clean it
                price_str = str(offer.get("price", ""))
                price_clean = re.sub(r'[^\d.]', '', price_str)
                
                if price_clean and float(price_clean) > 0:
                    offer["price"] = price_clean
                    offer["price_numeric"] = float(price_clean)
                    valid_offers.append(offer)
                else:
                    print(f"Skipping invalid offer: {offer}")
            except (ValueError, TypeError) as e:
                print(f"Error processing offer {offer}: {e}")
                continue
        
        print(f"Valid offers after filtering: {len(valid_offers)}")
        
        # If still no valid offers after filtering, try mock data again
        if len(valid_offers) == 0:
            print("No valid offers after filtering, generating mock data...")
            mock_offers = generate_mock_offers(product_info)
            for offer in mock_offers:
                try:
                    price_str = str(offer.get("price", ""))
                    price_clean = re.sub(r'[^\d.]', '', price_str)
                    
                    if price_clean and float(price_clean) > 0:
                        offer["price"] = price_clean
                        offer["price_numeric"] = float(price_clean)
                        valid_offers.append(offer)
                except (ValueError, TypeError) as e:
                    print(f"Error processing mock offer {offer}: {e}")
                    continue
            print(f"Added {len(valid_offers)} mock offers to valid offers")
        
        # Sort offers by price (ascending)
        try:
            sorted_offers = sorted(valid_offers, key=lambda x: x.get("price_numeric", float('inf')))
        except Exception as e:
            print(f"Error sorting offers: {e}")
            sorted_offers = valid_offers
        
        # Remove the numeric price field from final results
        for offer in sorted_offers:
            offer.pop("price_numeric", None)
        
        # Limit results to top 20
        final_offers = sorted_offers[:20]
        
        print(f"Returning {len(final_offers)} valid offers")
        
        # Add note about mock data if used
        note = None
        if len(all_offers) > 0 and any('mock' in str(offer) for offer in all_offers):
            note = "Demo data shown - real scraping capabilities available"
        
        return PriceComparisonResponse(
            results=final_offers,
            total_results=len(final_offers),
            country=input.country,
            query=input.query,
            supported_retailers=[retailer["name"] for retailer in retailers],
            note=note
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in compare_prices: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify the API is working."""
    return {
        "message": "API is working!",
        "supported_countries": get_supported_countries(),
        "sample_queries": [
            {"country": "US", "query": "iPhone 16 Pro, 128GB"},
            {"country": "IN", "query": "boAt Airdopes 311 Pro"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
