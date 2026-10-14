"""Feasibility service for deterministic business feasibility scoring."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def calculate_feasibility(
    market_data: Dict[str, Any],
    financial_data: Dict[str, Any],
    business_category: str,
    weights: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Calculate deterministic feasibility score based on market and financial data.

    This is a transparent, rule-based scoring system (NOT machine learning).
    Each indicator is normalized to 0-100 and weighted.

    Args:
        market_data: Market analysis data (population, competitors, density, etc.)
        financial_data: Financial analysis data (project cost, loan, scheme, etc.)
        business_category: Business category being analyzed
        weights: Optional custom weights (defaults to standard weights)

    Returns:
        Dict with feasibility_score and individual indicator scores
    """
    if weights is None:
        # Default weights from config
        from app.config.scoring import FEASIBILITY_WEIGHTS
        weights = FEASIBILITY_WEIGHTS

    limitations = []
    scores = {}

    # 1. Demand Score (based on population)
    population = market_data.get("population")
    if population and population > 0:
        # Normalize: Higher population = higher demand
        # Simple linear scale: 0-50k = 0-50, 50k-500k = 50-80, 500k+ = 80-100
        if population < 50000:
            demand_score = (population / 50000) * 50
        elif population < 500000:
            demand_score = 50 + ((population - 50000) / 450000) * 30
        else:
            demand_score = 80 + min(20, (population - 500000) / 500000 * 20)
        scores["demand_score"] = min(100, round(demand_score, 2))
    else:
        scores["demand_score"] = None
        limitations.append("Population data unavailable - demand score not calculated")

    # 2. Competition Score (based on competitor density)
    competitor_density = market_data.get("competitor_density")
    if competitor_density is not None:
        # Lower density = higher score (less competition is better)
        # Assume 0-0.5 density per sq km is good, 0.5-2 is moderate, 2+ is high
        if competitor_density <= 0.5:
            competition_score = 100 - (competitor_density / 0.5) * 20
        elif competitor_density <= 2.0:
            competition_score = 80 - ((competitor_density - 0.5) / 1.5) * 40
        else:
            competition_score = 40 - min(40, (competitor_density - 2.0) / 3.0 * 40)
        scores["competition_score"] = max(0, round(competition_score, 2))
    else:
        scores["competition_score"] = None
        limitations.append("Competitor density unavailable - competition score not calculated")

    # 3. Purchasing Power Score (based on population and location type)
    # For MVP, use a simple heuristic based on population size
    if population and population > 0:
        # Larger population generally indicates better purchasing power infrastructure
        if population > 1000000:
            purchasing_power_score = 85
        elif population > 500000:
            purchasing_power_score = 75
        elif population > 100000:
            purchasing_power_score = 65
        elif population > 50000:
            purchasing_power_score = 55
        else:
            purchasing_power_score = 45
        scores["purchasing_power_score"] = purchasing_power_score
    else:
        scores["purchasing_power_score"] = None
        limitations.append("Purchasing power data unavailable")

    # 4. Market Access Score (based on competitor count and nearest competitor)
    competitor_count = market_data.get("competitor_count", 0)
    nearest_distance = market_data.get("nearest_distance")

    if competitor_count == 0:
        # No competitors found - could be good (untapped market) or bad (no demand)
        market_access_score = 70  # Neutral score
        limitations.append("No competitors found - may indicate untapped market or low demand")
    elif nearest_distance is not None:
        # If nearest competitor is far, that's good for market access
        if nearest_distance > 5:
            market_access_score = 85
        elif nearest_distance > 2:
            market_access_score = 70
        elif nearest_distance > 0.5:
            market_access_score = 55
        else:
            market_access_score = 40
        market_access_score = round(market_access_score, 2)
    else:
        market_access_score = 65  # Default neutral score

    scores["market_access_score"] = market_access_score

    # 5. Supply Score (placeholder for future supply chain analysis)
    # For MVP, assign a neutral score
    scores["supply_score"] = None
    limitations.append("Supply chain data not yet integrated - supply score unavailable")

    # 6. Risk Score (based on competition and capital adequacy)
    project_cost = financial_data.get("project_cost", 0)
    available_margin = financial_data.get("available_margin_capital", 0)

    if project_cost > 0 and available_margin > 0:
        # Calculate capital adequacy
        margin_ratio = (available_margin / project_cost) * 100

        # Higher margin ratio = lower risk
        if margin_ratio >= 15:
            capital_risk = 20  # Low risk
        elif margin_ratio >= 10:
            capital_risk = 40  # Moderate risk
        else:
            capital_risk = 60  # Higher risk

        # Combine with competition risk
        comp_score = scores.get("competition_score", 50) or 50
        competition_risk = 100 - comp_score

        # Overall risk (lower is better, so invert for score)
        overall_risk = (capital_risk * 0.6 + competition_risk * 0.4)
        risk_score = 100 - overall_risk
        scores["risk_score"] = max(0, round(risk_score, 2))
    else:
        scores["risk_score"] = None
        limitations.append("Risk score calculation requires financial data")

    # 7. Capital Fit Score
    if project_cost > 0 and available_margin > 0:
        # How well does available capital fit the project?
        margin_ratio = (available_margin / project_cost) * 100

        # Ideal is 10-15% (meeting the scheme requirement with buffer)
        if 10 <= margin_ratio <= 15:
            capital_fit_score = 100
        elif 8 <= margin_ratio < 10:
            capital_fit_score = 80
        elif 15 < margin_ratio <= 20:
            capital_fit_score = 90
        elif margin_ratio > 20:
            # Too much margin might indicate underutilization
            capital_fit_score = 70
        else:
            # Less than 8% margin is risky
            capital_fit_score = 50
        scores["capital_fit_score"] = round(capital_fit_score, 2)
    else:
        scores["capital_fit_score"] = None
        limitations.append("Capital fit requires financial data")

    # Calculate weighted overall feasibility score
    total_score = 0.0
    total_weight = 0.0

    for indicator, weight in weights.items():
        score = scores.get(indicator)
        if score is not None:
            total_score += score * (weight / 100)
            total_weight += weight

    if total_weight > 0:
        feasibility_score = (total_score / total_weight) * 100
    else:
        feasibility_score = 0.0
        limitations.append("Insufficient data to calculate overall feasibility score")

    # Calculate confidence based on data availability
    available_indicators = sum(1 for s in scores.values() if s is not None)
    total_indicators = len(scores)
    confidence = (available_indicators / total_indicators) * 100 if total_indicators > 0 else 0

    return {
        "feasibility_score": round(feasibility_score, 2),
        "demand_score": scores.get("demand_score"),
        "competition_score": scores.get("competition_score"),
        "purchasing_power_score": scores.get("purchasing_power_score"),
        "market_access_score": scores.get("market_access_score"),
        "supply_score": scores.get("supply_score"),
        "risk_score": scores.get("risk_score"),
        "capital_fit_score": scores.get("capital_fit_score"),
        "confidence": round(confidence, 2),
        "limitations": limitations,
    }
