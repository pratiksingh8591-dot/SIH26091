# Quick Start Guide - SIH26091 Business Advisor

## What Has Been Implemented

### ✅ Complete Backend (FastAPI + Python)
- **New Services:**
  - `overpass_service.py` - Fetches real competitor data from OpenStreetMap
  - `geospatial_service.py` - Distance, density, nearest competitor calculations
  - `population_service.py` - Population data (sample data for MVP)
  - `financial_service.py` - Project cost, loan, scheme routing, EMI calculations
  - `feasibility_service.py` - Deterministic feasibility scoring engine

- **New API Routes:**
  - `POST /api/analyze` - Main endpoint for complete analysis
  - `POST /api/market/competitors` - Get competitor data
  - `POST /api/market/population` - Get population data
  - `POST /api/finance/calculate` - Financial calculations
  - `GET /api/business/categories` - Supported business categories

- **Database Models:** SQLAlchemy models ready (optional PostgreSQL)
- **Configuration:** Scoring weights, AI interface for future ML
- **Tests:** pytest tests for financial, geospatial, and Overpass services

### ✅ Complete Frontend (React + Vite)
- **New Components:**
  - `CompetitorMap.jsx` - Interactive Leaflet map with competitor pins
  - `FinancialRoadmap.jsx` - Complete financial breakdown with EMI table
  - `LoadingState.jsx` - Loading animation

- **New Pages:**
  - `LocationSelectionPage.jsx` - Location selection with interactive map
  - `FeasibilityDashboardPage.jsx` - Complete results dashboard

- **Updated:**
  - `App.jsx` - New flow: Home → Location Selection → Loading → Dashboard
  - `api.js` - Axios-based API client with all new endpoints

---

## Next Steps to Run the Application

### 1. Install Backend Dependencies

```bash
cd business-advisor/backend

# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install new dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd business-advisor/frontend

# Install new packages (axios, leaflet, react-leaflet)
npm install
```

### 3. Run Backend

```bash
cd business-advisor/backend
uvicorn app.main:app --reload
```

Backend will start at: **http://localhost:8000**

Check API docs: **http://localhost:8000/docs**

### 4. Run Frontend

```bash
cd business-advisor/frontend
npm run dev
```

Frontend will start at: **http://localhost:5173**

---

## Testing the Application

### Test Scenario 1: Restaurant in Pune

1. Open http://localhost:5173
2. Click "Start Analysis"
3. Enter:
   - Location Name: "Pune, Maharashtra"
   - Click on map near Pune (lat: 18.5204, lon: 73.8567)
   - Business Category: Restaurant
   - Business Name: "My Restaurant"
   - Margin Capital: ₹200,000
   - Radius: 10 km
4. Click "Analyze Business Feasibility"
5. Wait for analysis (fetches real OSM data)
6. View dashboard with:
   - Feasibility score
   - Competitor map with pins
   - Financial roadmap
   - EMI schedule

### Test Scenario 2: Bakery in Mumbai

1. Location: "Mumbai, Maharashtra" (19.0760, 72.8777)
2. Category: Bakery
3. Capital: ₹100,000
4. Radius: 5 km

Expected Results:
- Project Cost: ₹10,00,000
- Loan: ₹9,00,000
- Scheme: **Term Loan Scheme** (8%, 7 years)

### Test Scenario 3: Micro Finance Range

1. Capital: ₹10,000
2. Expected:
   - Project Cost: ₹1,00,000
   - Scheme: **Micro Finance Scheme** (6.5%, 3 years)

---

## API Testing (Without Frontend)

### Using curl:

```bash
# Health check
curl http://localhost:8000/health

# Get business categories
curl http://localhost:8000/api/business/categories

# Full analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "location": {
      "name": "Pune",
      "latitude": 18.5204,
      "longitude": 73.8567
    },
    "business": {
      "name": "My Restaurant",
      "category": "restaurant"
    },
    "available_margin_capital": 200000,
    "radius_km": 10
  }'
```

### Using Swagger UI:

Visit: **http://localhost:8000/docs**

Try the POST /api/analyze endpoint with the example request.

---

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

**Error: "Address already in use"**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

**Database warning:**
- Database is optional. App works without PostgreSQL.
- Set DATABASE_URL in .env to enable caching.

### Frontend Issues

**Error: "Cannot find module"**
```bash
npm install
```

**Blank page:**
- Check browser console for errors
- Verify backend is running at http://localhost:8000
- Check VITE_API_BASE_URL in .env

**Map not showing:**
- Leaflet CSS should load automatically
- Check network tab for blocked resources

**CORS errors:**
- Backend CORS is configured for localhost:5173
- Check backend terminal for CORS logs

---

## What to Expect

### Backend Features Working:
✅ Real competitor data from OpenStreetMap  
✅ Geospatial calculations (distance, density)  
✅ Financial calculations (exact scheme routing)  
✅ Feasibility scoring (deterministic)  
✅ Population estimates (sample data)  
✅ Complete API documentation  

### Frontend Features Working:
✅ Interactive location selection with map  
✅ Business category selection  
✅ Margin capital input  
✅ Loading state during analysis  
✅ Competitor map with pins and radius circle  
✅ Feasibility score dashboard  
✅ Financial roadmap with EMI table  
✅ Data sources and limitations display  

### Known Limitations:
⚠️ OSM data may be incomplete in rural areas  
⚠️ Population data uses Census 2011 baseline  
⚠️ Deterministic scoring (not ML yet)  
⚠️ Supply score not calculated (future)  
⚠️ Database optional (no caching without it)  

---

## File Changes Summary

### New Backend Files (23 files)
- 5 service files (overpass, geospatial, population, financial, feasibility)
- 3 route files (analysis, market, finance)
- 6 database models
- 3 AI interface files
- 1 config file
- 3 test files
- Updated: main.py, schemas.py, business.py, .env.example

### New Frontend Files (6 files)
- 3 components (CompetitorMap, FinancialRoadmap, LoadingState)
- 2 pages (LocationSelectionPage, FeasibilityDashboardPage)
- Updated: App.jsx, api.js, package.json
- New: .env.example

### Updated Documentation
- README.md (complete rewrite)

---

## Next Development Steps

### For Production:
1. Set up PostgreSQL database
2. Add real Census API integration
3. Implement ML feasibility model
4. Add LLM for SWOT generation
5. Add user authentication
6. Add caching layer for Overpass API
7. Add error boundaries in React
8. Add comprehensive error handling

### For Enhancement:
1. Add more business categories
2. Improve population data coverage
3. Add supply chain analysis
4. Add seasonal factors
5. Add Google Places API integration
6. Add export to PDF feature
7. Add comparison between multiple locations

---

## Success Criteria

✅ Backend runs without errors  
✅ Frontend loads and displays UI  
✅ Can select location on map  
✅ Analysis fetches real OSM data  
✅ Financial calculations are accurate  
✅ Competitor map displays correctly  
✅ EMI table shows correct values  
✅ Scheme routing works per specification  

---

## Support Resources

- **API Documentation:** http://localhost:8000/docs
- **Backend Logs:** Check terminal running uvicorn
- **Frontend Logs:** Check browser console (F12)
- **README:** Full documentation in README.md

---

**You're all set! The complete MVP is ready to run.** 🚀
