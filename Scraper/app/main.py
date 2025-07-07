
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class QueryInput(BaseModel):
    country: str
    query: str

@app.post("/compare")
async def compare_prices(input: QueryInput):
    # Placeholder response
    return {"message": f"Received query for {input.query} in {input.country}"}
