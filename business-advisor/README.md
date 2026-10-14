# SIH Business Advisory System - Hyper-Local Business Feasibility Analysis

**Smart India Hackathon 2026 - Problem Statement #26091**

AI-Driven Scheme Matching for Marginalized Entrepreneurs with Hyper-Local Business Feasibility Analysis

---

## Overview

This application provides location-based business feasibility analysis for rural and marginalized micro-entrepreneurs. It combines:

- **Real competitor data** from OpenStreetMap/Overpass API
- **Geospatial analysis** (distance, density, market positioning)
- **Population estimates** from Census data
- **Financial calculations** (project cost, loan routing, EMI)
- **Deterministic feasibility scoring** (transparent, rule-based)
- **Interactive maps** with React-Leaflet

**Current Status:** MVP with deterministic scoring. Architecture ready for ML/LLM integration.

---

## Architecture

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL with SQLAlchemy ORM (optional for MVP)
- **External APIs:** OpenStreetMap Overpass API
- **Geospatial:** geopy
- **HTTP Client:** httpx

### Frontend
- **Framework:** React 18 + Vite
- **Maps:** Leaflet + React-Leaflet
- **HTTP Client:** Axios
- **Styling:** Custom CSS

---

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL** (optional for MVP - database features work without it)
- **Git**

---

## Installation

### 1. Clone Repository

```bash
cd path/to/SIH26091/business-advisor
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment

**Windows:**
```powershell
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/business_advisor  # Optional
OVERPASS_URL=https://overpass-api.de/api/interpreter
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Note:** `DATABASE_URL` is optional. The application works without a database but won't cache results.

#### Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

API Documentation (Swagger): **http://localhost:8000/docs**

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

#### Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Run Frontend

```bash
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## API Endpoints

### Health Check
```
GET /health
```

Returns backend status.

### Business Categories
```
GET /api/business/categories
```

Returns supported business categories with OSM tag mappings.

### Main Analysis Endpoint
```
POST /api/analyze
```

**Request Body:**
```json
{
  "location": {
    "name": "Pune, Maharashtra",
    "latitude": 18.5204,
    "longitude": 73.8567
  },
  "business": {
    "name": "My Restaurant",
    "category": "restaurant"
  },
  "available_margin_capital": 200000,
  "radius_km": 10
}
```

**Response:** Complete analysis with market data, feasibility scores, and financial roadmap.

### Market Endpoints
```
POST /api/market/competitors
POST /api/market/population
```

Fetch competitor data and population data separately.

### Finance Endpoint
```
POST /api/finance/calculate
```

Calculate financial details from margin capital only.

---

## Financial Formulas

### 1. Project Cost Calculation
```
Available Margin Capital = 10% of Project Cost
Project Cost = Available Margin Capital / 0.10
```

**Example:** ₹2,00,000 margin → ₹20,00,000 project cost

### 2. Loan Calculation
```
Maximum Loan = Project Cost × 0.90
```

**Example:** ₹20,00,000 project cost → ₹18,00,000 loan

### 3. Scheme Routing

| Project Cost | Scheme | Interest Rate | Tenure | Moratorium |
|---|---|---|---|---|
| ≤ ₹1.40 lakh | Micro Finance Scheme | 6.5% p.a. | 3 years | 3 months |
| ₹1.40 lakh < cost ≤ ₹50 lakh | Term Loan Scheme | 8% p.a. | 7 years | 6 months |
| > ₹50 lakh | **Not supported** | — | — | — |

### 4. EMI Calculation

Uses **reducing balance method**:

```
EMI = [P × r × (1 + r)^n] / [(1 + r)^n - 1]

Where:
P = loan amount
r = monthly interest rate (annual_rate / 12 / 100)
n = repayment months (total months - moratorium)
```

**Moratorium:** Only interest accrues; no payment required.

**After Moratorium:** Regular EMI starts.

---

## Data Sources

### 1. Competitor Data
- **Source:** OpenStreetMap via Overpass API
- **Coverage:** Varies by region (urban areas have better data)
- **Freshness:** Real-time from OSM
- **Limitation:** Incomplete in rural areas

### 2. Population Data
- **Source:** Census 2011 (sample dataset in MVP)
- **Coverage:** Major cities only in current implementation
- **Freshness:** Baseline from 2011
- **Limitation:** Not current population; requires integration with live Census API

### 3. Geospatial Calculations
- **Method:** Geodesic distance (geopy)
- **Accuracy:** High (accounts for Earth's curvature)

---

## Feasibility Scoring

### Deterministic Scoring Engine

The current implementation uses **transparent rule-based scoring** (NOT machine learning).

### Indicators

1. **Demand Score** (20%)
   - Based on local population
   - Higher population = higher demand potential

2. **Competition Score** (20%)
   - Based on competitor density (competitors per sq km)
   - Lower density = higher score

3. **Purchasing Power Score** (15%)
   - Estimated from population size and urban classification
   - Larger cities = higher purchasing power

4. **Market Access Score** (10%)
   - Based on distance to nearest competitors
   - Farther competitors = better positioning

5. **Supply Score** (10%)
   - *Not yet implemented* (future: supply chain distance analysis)

6. **Risk Score** (15%)
   - Combined: capital adequacy + competition risk
   - Higher margin ratio = lower risk

7. **Capital Fit Score** (10%)
   - How well margin capital matches project requirements
   - Ideal: 10-15% margin ratio

### Overall Feasibility Score
```
Feasibility Score = Σ (Indicator Score × Weight)
```

### Confidence Level
```
Confidence = (Available Indicators / Total Indicators) × 100
```

---

## Current Limitations

1. **Competitor Data Completeness**
   - OSM coverage varies significantly by region
   - Rural areas may have incomplete data
   - Some businesses may not be mapped

2. **Population Data Freshness**
   - Using Census 2011 baseline (sample data)
   - Actual current population may differ
   - Requires integration with live Census API

3. **Deterministic Scoring**
   - Current system uses rule-based heuristics
   - Not trained on historical business success data
   - ML integration planned for future

4. **No ML/LLM Integration**
   - Architecture supports it but not implemented
   - SWOT generation is rule-based
   - Natural language insights not yet available

5. **No Supply Chain Data**
   - Supply score indicator not calculated
   - Requires integration with logistics/supply APIs

6. **Database Optional**
   - Caching and historical analysis require PostgreSQL
   - MVP works without database but loses features

7. **No Authentication**
   - Public API in MVP
   - Production needs user authentication

---

## Future Integration Points

### 1. ML Feasibility Model

**File:** `app/ai/ml_model.py`

Replace rule-based scoring with trained ML model:

```python
class MLFeasibilityModel(FeasibilityModel):
    def __init__(self, model_path: str):
        self.model = load_model(model_path)

    def predict(self, features: dict) -> dict:
        # Use trained model
        return self.model.predict(features)
```

**Data Requirements:**
- Historical business success/failure data
- Market conditions at launch time
- Actual revenue/profitability outcomes

### 2. LLM Report Generator

**File:** `app/ai/llm_report_generator.py`

Generate natural language insights:

```python
def generate_swot_report(analysis_result: dict) -> dict:
    prompt = build_prompt(analysis_result)
    response = call_llm(prompt)
    return parse_swot(response)
```

**Integration:**
- Add to `/analyze` endpoint response
- Generate SWOT, recommendations, market insights
- Explain scores in natural language

### 3. Real-Time Population Data

Replace Census 2011 with live API:
- Government Census API (if available)
- WorldPop API
- Google Demographics API

### 4. Additional Data Sources

- **Supply Chain:** Integrate logistics APIs for supply distance
- **Economic Indicators:** GDP per capita, purchasing power index
- **Google Places:** Supplement OSM competitor data
- **Weather/Climate:** Seasonal business viability

---

## Running Tests

```bash
cd backend
pytest tests/
```

**Test Coverage:**
- Financial calculations (project cost, loan, EMI, scheme routing)
- Geospatial calculations (distance, density)
- Overpass service (query building, parsing)

---

## Development Commands

### Backend

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run on custom port
uvicorn app.main:app --port 8080

# View API docs
# Visit http://localhost:8000/docs
```

### Frontend

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Project Structure

```
business-advisor/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point
│   │   ├── routes/
│   │   │   ├── analysis.py             # Main /analyze endpoint
│   │   │   ├── market.py               # /market/* endpoints
│   │   │   ├── finance.py              # /finance/* endpoints
│   │   │   ├── business.py             # Business categories
│   │   │   ├── feasibility.py          # Old feasibility endpoint
│   │   │   └── schemes.py              # Scheme matching
│   │   ├── services/
│   │   │   ├── overpass_service.py     # OSM competitor fetching
│   │   │   ├── geospatial_service.py   # Distance/density calculations
│   │   │   ├── population_service.py   # Population data
│   │   │   ├── financial_service.py    # Financial calculations
│   │   │   ├── feasibility_service.py  # Feasibility scoring
│   │   │   ├── business_analysis.py    # Business recommendation
│   │   │   ├── financial_analysis.py   # Financial analysis
│   │   │   └── scheme_matching.py      # Scheme matching
│   │   ├── models/
│   │   │   ├── schemas.py              # Pydantic schemas
│   │   │   ├── location.py             # SQLAlchemy models
│   │   │   ├── business.py
│   │   │   ├── competitor.py
│   │   │   ├── population.py
│   │   │   └── analysis.py
│   │   ├── database/
│   │   │   ├── base.py                 # Base model
│   │   │   └── session.py              # DB session
│   │   ├── config/
│   │   │   └── scoring.py              # Feasibility weights
│   │   ├── ai/
│   │   │   ├── base.py                 # FeasibilityModel interface
│   │   │   └── rule_based_model.py     # Current implementation
│   │   ├── data/
│   │   │   ├── businesses.py           # Sample business data
│   │   │   └── schemes.py              # Sample scheme data
│   │   └── utils/
│   │       └── calculations.py         # Calculation utilities
│   ├── tests/
│   │   ├── test_financial_service.py
│   │   ├── test_geospatial_service.py
│   │   └── test_overpass_service.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx                     # Main app component
│   │   ├── main.jsx                    # Entry point
│   │   ├── services/
│   │   │   └── api.js                  # API client
│   │   ├── pages/
│   │   │   ├── LocationSelectionPage.jsx
│   │   │   └── FeasibilityDashboardPage.jsx
│   │   ├── components/
│   │   │   ├── CompetitorMap.jsx
│   │   │   ├── FinancialRoadmap.jsx
│   │   │   └── LoadingState.jsx
│   │   └── styles.css
│   ├── package.json
│   └── .env.example
└── README.md
```

---

## Example Usage

### 1. Start Backend and Frontend

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. Open Application

Visit: **http://localhost:5173**

### 3. Perform Analysis

1. **Click "Start Analysis"**
2. **Enter Location:**
   - Name: "Pune, Maharashtra"
   - Click on map to set coordinates (or use default)
3. **Select Business:**
   - Category: "Restaurant"
   - Name: "My Restaurant"
4. **Enter Margin Capital:** ₹2,00,000
5. **Set Radius:** 10 km
6. **Click "Analyze Business Feasibility"**

### 4. View Results

**Feasibility Dashboard displays:**
- Overall feasibility score (0-100)
- Individual indicator scores
- Competitor map with pins and metrics
- Financial roadmap with EMI and repayment schedule
- Data sources and limitations

---

## Support

For questions or issues:

- Review API documentation: http://localhost:8000/docs
- Check browser console for frontend errors
- Check terminal for backend errors
- Verify backend is running and accessible

---

## License

This project was developed for Smart India Hackathon 2026.

---

## Contributors

Built for SIH 2026 Problem Statement #26091

---

## Acknowledgments

- **OpenStreetMap contributors** for competitor data
- **Census of India** for population data baseline
- **Smart India Hackathon** for problem statement and opportunity

## Business Intelligence & Location Analytics

The backend now exposes:

- `GET /api/clustering/results?n_clusters=3` and `POST /api/clustering/fit`
- `GET /api/locations/compare?names=Pune&names=Mumbai`
- `POST /api/business/predict`
- `GET /api/business/model-metrics`

K-Means uses the actual records in `backend/app/services/population_service.py`. Invalid
coordinates/populations and duplicate records are removed, population is standardized, and
the fitted centroids determine the Low/Medium/High Population labels. Elbow inertias and a
silhouette score (when the dataset is large enough) are returned. The selected model is
persisted under `backend/data/models/`.

The current project dataset contains only `location_name`, `latitude`, `longitude`,
`population`, and `area_type`. It has no historical business success, profitability,
survival, or performance target. Consequently, the Random Forest endpoints report
`status: unavailable` and do not fabricate a probability or evaluation metric. To enable
prediction, add multiple labelled business records with pre-opening location features,
business category, and a historical outcome column; then connect those records to
`train_business_success_model`.

### Run and test

From the project root on Windows:

```powershell
cd business-advisor\backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

In another terminal:

```powershell
cd business-advisor\frontend
npm install
npm run dev
```

Run backend tests with:

```powershell
cd business-advisor\backend
venv\Scripts\python.exe -m pytest tests -q
```
