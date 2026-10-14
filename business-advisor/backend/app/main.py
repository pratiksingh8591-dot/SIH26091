"""FastAPI application entry point."""

from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router
from app.routes.business import router as business_router
from app.routes.feasibility import router as feasibility_router
from app.routes.finance import router as finance_router
from app.routes.market import router as market_router
from app.routes.schemes import router as schemes_router
from app.routes.analytics import router as analytics_router

load_dotenv()

app = FastAPI(
    title="Business Advisor API",
    version="2.0.0",
    description="Hyper-local business feasibility analysis for marginalized entrepreneurs",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

for origin in os.getenv("CORS_ORIGINS", "").split(","):
    if origin.strip():
        origins.append(origin.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        from app.database.session import init_db
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization skipped or failed: {e}")
        print("Set DATABASE_URL environment variable to enable database features")


@app.get("/health")
def health() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Business advisor backend is running.",
        "version": "2.0.0",
    }


# Include all routers
app.include_router(analysis_router)  # New: /api/analyze
app.include_router(market_router)  # New: /api/market/*
app.include_router(finance_router)  # New: /api/finance/*
app.include_router(business_router)  # Updated with /api/business/categories
app.include_router(schemes_router)
app.include_router(feasibility_router)
app.include_router(analytics_router)
