from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.llm_utils import parse_query_with_llm
from app.retailers import get_retailers_for_country
from app.scraper import scrape_amazon, scrape_flipkart, scrape_bestbuy

import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryInput(BaseModel):
    country: str
    query: str

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/compare")
async def compare_prices(input: QueryInput):
    print("Received country:", input.country)
    product_info = parse_query_with_llm(input.query)
    retailers = get_retailers_for_country(input.country)
    print("Retailers found:", retailers)
    all_offers = []
    for retailer in retailers:
        offers = retailer["scrape_func"](product_info)
        print("Offers from", retailer["name"], offers)
        all_offers.extend(offers)
    sorted_offers = sorted(all_offers, key=lambda x: float(x["price"]))
    print("Returning offers:", sorted_offers)
    return sorted_offers
