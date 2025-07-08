# API Testing Commands

## Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

## Get Supported Countries
```bash
curl -X GET "http://localhost:8000/countries"
```

## Price Comparison Examples

### Required Test Case 1: iPhone 16 Pro, 128GB (US)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
```

### Required Test Case 2: boAt Airdopes 311 Pro (India)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "IN", "query": "boAt Airdopes 311 Pro"}'
```

### Additional Test Cases

#### Samsung Galaxy S24 Ultra (UK)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "GB", "query": "Samsung Galaxy S24 Ultra"}'
```

#### MacBook Pro 14 inch (Germany)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "DE", "query": "MacBook Pro 14 inch"}'
```

#### Nike Air Force 1 (Canada)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "CA", "query": "Nike Air Force 1"}'
```

## PowerShell Examples (Windows)

### Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
```

### Price Comparison
```powershell
$body = '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
Invoke-WebRequest -Uri "http://localhost:8000/compare" -Method POST -Body $body -ContentType "application/json"
```

## Expected Response Format

```json
{
  "results": [
    {
      "link": "https://www.amazon.com/...",
      "price": "999.99",
      "currency": "USD",
      "productName": "Apple iPhone 16 Pro 128GB",
      "source": "Amazon US"
    },
    {
      "link": "https://www.bestbuy.com/...",
      "price": "1049.99",
      "currency": "USD",
      "productName": "iPhone 16 Pro 128GB - Natural Titanium",
      "source": "BestBuy"
    }
  ],
  "total_results": 2,
  "country": "US",
  "query": "iPhone 16 Pro, 128GB",
  "supported_retailers": ["Amazon US", "BestBuy", "Walmart", "Target", "eBay US"]
}
```

## Frontend Access

The web interface is available at: `http://localhost:8000`

## Running the Server

```bash
# Activate virtual environment
.\scrape_venv\Scripts\activate

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`
