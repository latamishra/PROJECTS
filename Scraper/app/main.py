from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.llm_utils import parse_query_with_llm  # or just llm_utils if in same folder
import os

app = FastAPI()

# Mount the static directory for assets (if you add CSS/JS/images)
app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryInput(BaseModel):
    country: str
    query: str

# Serve the frontend at the root URL
@app.get("/", response_class=FileResponse)
async def serve_frontend():
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/compare")
async def compare_prices(input: QueryInput):
    parsed_query = parse_query_with_llm(input.query)
    # Dummy response for testing
    return [
        {
            "link": "https://apple.com/iphone-16-pro",
            "price": "999",
            "currency": "USD",
            "productName": "Apple iPhone 16 Pro 128GB"
        }
    ]
