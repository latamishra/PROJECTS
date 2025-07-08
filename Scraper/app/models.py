# app/models.py

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    """Model for parsed product information."""
    brand: str = Field(default="", description="Product brand")
    model: str = Field(default="", description="Product model")
    specs: str = Field(default="", description="Product specifications")
    category: str = Field(default="general", description="Product category")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")
    country: str = Field(default="US", description="Target country")

class PriceOffer(BaseModel):
    """Model for a price offer from a retailer."""
    link: str = Field(description="Link to the product")
    price: str = Field(description="Product price")
    currency: str = Field(description="Currency code")
    productName: str = Field(description="Product name")
    source: str = Field(description="Retailer source")
    
class SearchQuery(BaseModel):
    """Model for search query input."""
    country: str = Field(description="Country code (e.g., US, IN)")
    query: str = Field(description="Product search query")

class SearchResponse(BaseModel):
    """Model for search response."""
    results: List[PriceOffer]
    total_results: int
    country: str
    query: str
    supported_retailers: List[str]
    search_time: Optional[float] = None
    note: Optional[str] = None
    
class RetailerInfo(BaseModel):
    """Model for retailer information."""
    name: str
    priority: int
    country_code: str
    supported_categories: List[str] = Field(default_factory=list)
    
class CountryInfo(BaseModel):
    """Model for country information."""
    code: str
    name: str
    currency: str
    supported_retailers: List[str]
