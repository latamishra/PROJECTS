# Universal Price Comparison Tool

A comprehensive price comparison tool that fetches product prices from multiple retailers across different countries using AI-powered query parsing and real-time web scraping.

## 🌐 **Live Demo**

**Hosted URL**: [https://price-comparison-tool.vercel.app](https://price-comparison-tool.vercel.app)

**API Endpoint**: `https://price-comparison-tool.vercel.app/compare`

## 🧪 **Quick Test with cURL**

Test the API directly with these working examples:

### Test Case 1: iPhone 16 Pro (US Market)
```bash
curl -X POST "https://price-comparison-tool.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
```

### Test Case 2: boAt Airdopes (India Market)  
```bash
curl -X POST "https://price-comparison-tool.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "IN", "query": "boAt Airdopes 311 Pro"}'
```

### Test Case 3: Bananas (US Grocery)
```bash
curl -X POST "https://price-comparison-tool.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "bananas"}'
```

### Test Case 4: Samsung Galaxy (UK Market)
```bash
curl -X POST "https://price-comparison-tool.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "GB", "query": "Samsung Galaxy S24 Ultra"}'
```

## ✅ **Expected API Response**

```json
{
  "results": [
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
    }
  ],
  "total_results": 2,
  "country": "US", 
  "query": "iPhone 16 Pro, 128GB",
  "supported_retailers": ["Amazon US", "BestBuy", "Walmart", "Target", "eBay US"],
  "note": null
}
```

- **Multi-Country Support**: Works across 15+ countries including US, India, UK, Germany, France, Canada, Australia, Japan, China, Brazil, Singapore, Malaysia, Thailand, and more
- **Multi-Retailer Coverage**: Scrapes from popular retailers like Amazon, eBay, Flipkart, BestBuy, Walmart, Target, and many others
- **AI-Powered Query Parsing**: Uses Google Gemini AI to intelligently parse product queries and extract relevant information
- **Fuzzy Product Matching**: Ensures scraped products actually match the search query using advanced fuzzy matching
- **Modern Web Interface**: Beautiful, responsive frontend for easy searching
- **Fast Concurrent Scraping**: Parallel scraping for faster results
- **Price Sorting**: Results automatically sorted by price (lowest first)
- **Error Handling**: Robust error handling and fallback mechanisms

## Supported Countries

| Country | Code | Primary Retailers |
|---------|------|-------------------|
| United States | US | Amazon, BestBuy, Walmart, Target, eBay |
| India | IN | Amazon, Flipkart, Myntra, Snapdeal, Croma |
| United Kingdom | GB | Amazon, Currys, Argos, John Lewis, eBay |
| Germany | DE | Amazon, Conrad, MediaMarkt, eBay |
| France | FR | Amazon, Fnac, Cdiscount, eBay |
| Canada | CA | Amazon, BestBuy, Walmart, eBay |
| Australia | AU | Amazon, eBay |
| Japan | JP | Amazon, Rakuten, eBay |
| China | CN | Alibaba, Tmall, JD.com |
| Brazil | BR | MercadoLibre, Amazon |
| Singapore | SG | Amazon, Shopee |
| Malaysia | MY | Shopee |
| Thailand | TH | Shopee |

## API Usage

### Compare Prices Endpoint
```
POST /compare
Content-Type: application/json
```

### Request Format
```json
{
  "country": "US",
  "query": "iPhone 16 Pro, 128GB"
}
```

### Working cURL Examples

#### Test Case 1: iPhone 16 Pro (US) - Required Test Case
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
```

#### Test Case 2: boAt Airdopes (India) - Required Test Case  
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "IN", "query": "boAt Airdopes 311 Pro"}'
```

#### Test Case 3: Bananas (Grocery Testing)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "bananas"}'
```

#### Test Case 4: Samsung Galaxy (UK Market)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "GB", "query": "Samsung Galaxy S24 Ultra"}'
```

#### Additional Test Cases
```bash
# MacBook (Canada)
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "CA", "query": "MacBook Air M2"}'

# Sony Headphones (Germany)  
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "DE", "query": "Sony WH-1000XM5"}'

# Nike Shoes (Australia)
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "AU", "query": "Nike Air Force 1"}'
```

### Other Endpoints

#### Health Check
```bash
curl "http://localhost:8000/health"
```

#### Get Supported Countries
```bash
curl "http://localhost:8000/countries"
```

### Example Response
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

## 🚀 **Deployment Options**

This application can be deployed on multiple platforms:

### Option 1: Vercel (Recommended)
1. Fork this repository to your GitHub account
2. Connect your GitHub account to [Vercel](https://vercel.com)
3. Import the project and set environment variable:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
4. Deploy automatically - Vercel will handle the rest!

### Option 2: Railway
1. Fork this repository
2. Connect to [Railway](https://railway.app)
3. Set the `GOOGLE_API_KEY` environment variable
4. Deploy with one click

### Option 3: Render
1. Fork this repository  
2. Connect to [Render](https://render.com)
3. Use the provided `render.yaml` configuration
4. Set environment variables and deploy

### Option 4: Local Testing
```bash
# Clone and setup
git clone <your-repo-url>
cd Scraper
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install

# Set environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 **Testing the Deployed API**

Replace `https://price-comparison-tool.vercel.app` with your actual deployed URL:

### Health Check
```bash
curl "https://your-deployed-url.vercel.app/health"
```

### Get Supported Countries
```bash
curl "https://your-deployed-url.vercel.app/countries"
```

### Price Comparison Examples
```bash
# Electronics (US)
curl -X POST "https://your-deployed-url.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 15 Pro"}'

# Groceries (US)  
curl -X POST "https://your-deployed-url.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "organic bananas"}'

# Electronics (India)
curl -X POST "https://your-deployed-url.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "IN", "query": "boAt Airdopes 131"}'

# Electronics (UK)
curl -X POST "https://your-deployed-url.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "GB", "query": "MacBook Air M2"}'
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js (for frontend development, optional)
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

6. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t price-comparison-tool .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 -e GOOGLE_API_KEY=your_api_key price-comparison-tool
   ```

## Test Examples

### Working Test Case: iPhone 16 Pro, 128GB (US)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
```

### Working Test Case: boAt Airdopes 311 Pro (India)
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "IN", "query": "boAt Airdopes 311 Pro"}'
```

### Other Test Cases
```bash
# Samsung Galaxy S24 Ultra (UK)
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "GB", "query": "Samsung Galaxy S24 Ultra"}'

# MacBook Pro 14 inch (Germany)
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "DE", "query": "MacBook Pro 14 inch"}'
```

## Architecture

The application is built with:
- **FastAPI**: Modern, fast web framework for building APIs
- **Playwright**: Browser automation for dynamic content scraping
- **BeautifulSoup**: HTML parsing for static content
- **Google Gemini AI**: Intelligent query parsing and product information extraction
- **Pydantic**: Data validation and serialization
- **Concurrent Processing**: Parallel scraping for improved performance

## Key Features

### 1. Intelligent Query Parsing
The system uses Google Gemini AI to parse natural language queries and extract:
- Product brand
- Model/variant
- Specifications
- Product category
- Search keywords

### 2. Advanced Product Matching
Uses fuzzy string matching to ensure scraped products actually match the search query:
- Brand name matching
- Model number verification
- Specification comparison
- Overall similarity scoring

### 3. Robust Error Handling
- Retry mechanisms for failed requests
- Fallback parsers when AI fails
- Graceful degradation for unsupported sites
- Comprehensive logging

### 4. Performance Optimization
- Concurrent scraping across multiple retailers
- Request rate limiting and user agent rotation
- Efficient data structures and algorithms
- Caching mechanisms (future enhancement)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is for educational and research purposes only. Please respect the terms of service of the websites you scrape and implement appropriate rate limiting and caching mechanisms for production use.
