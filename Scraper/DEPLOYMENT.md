# Deployment Guide

## Quick Deploy to Vercel

### Prerequisites
1. GitHub account
2. Vercel account (free)
3. Google Gemini API key

### Steps

1. **Fork this repository** to your GitHub account

2. **Get Google Gemini API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key (you'll need it in step 4)

3. **Deploy to Vercel**
   - Go to [Vercel](https://vercel.com)
   - Click "New Project"
   - Import your forked repository
   - Configure environment variables:
     - Key: `GOOGLE_API_KEY`
     - Value: Your Google Gemini API key

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (2-3 minutes)
   - Get your deployed URL: `https://your-project-name.vercel.app`

### Test Your Deployment

```bash
# Replace with your actual URL
curl -X POST "https://your-project-name.vercel.app/compare" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 15"}'
```

## Alternative: Deploy to Railway

1. **Connect to Railway**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub account
   - Select your forked repository

2. **Set Environment Variables**
   - In Railway dashboard, go to Variables
   - Add: `GOOGLE_API_KEY` = your Gemini API key

3. **Deploy**
   - Railway automatically builds and deploys
   - Get your URL from the Railway dashboard

## Alternative: Deploy to Render

1. **Connect to Render**
   - Go to [Render](https://render.com)
   - Connect your GitHub account
   - Create new Web Service from your repository

2. **Configure**
   - Build Command: `pip install -r requirements.txt && playwright install chromium`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: `GOOGLE_API_KEY` = your key

3. **Deploy**
   - Render builds and deploys automatically
   - Free tier available with some limitations

## Troubleshooting

### Common Issues

1. **Playwright Installation Fails**
   - Some platforms may not support Playwright
   - The app falls back to requests-only scraping

2. **API Rate Limits**
   - Google Gemini free tier has limits
   - App includes fallback parsing without AI

3. **Timeout Errors**
   - Increase timeout in deployment settings
   - Or reduce number of concurrent scrapers

### Environment Variables

Required:
- `GOOGLE_API_KEY`: Your Google Gemini API key

Optional:
- `MAX_REQUESTS_PER_MINUTE`: Rate limiting (default: 60)
- `CONCURRENT_SCRAPERS`: Parallel scrapers (default: 5)
- `ENABLE_CACHING`: Cache results (default: true)

## Success Metrics

Your deployment is working if:
- Health check returns 200: `curl https://your-url/health`
- Countries endpoint works: `curl https://your-url/countries` 
- Price comparison returns results for test queries
- Frontend loads at your base URL
