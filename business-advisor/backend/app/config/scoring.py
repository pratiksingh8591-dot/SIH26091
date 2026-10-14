"""Scoring configuration for feasibility analysis."""

from __future__ import annotations

# Weights for feasibility indicators (should sum to 100)
FEASIBILITY_WEIGHTS = {
    "demand_score": 20,
    "competition_score": 20,
    "purchasing_power_score": 15,
    "market_access_score": 10,
    "supply_score": 10,
    "risk_score": 15,
    "capital_fit_score": 10,
}

# Maximum expected competitor density (competitors per sq km)
# Used for normalizing competition scores
MAX_EXPECTED_DENSITY = 5.0

# Population thresholds for demand scoring
POPULATION_THRESHOLDS = {
    "low": 50000,
    "medium": 500000,
    "high": 1000000,
}
