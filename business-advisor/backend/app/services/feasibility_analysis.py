"""Feasibility analysis service coordinating business assumptions and financial metrics."""

from __future__ import annotations

from typing import Any, Dict

from app.services.business_analysis import recommend_businesses
from app.services.financial_analysis import analyze_financials


def feasibility_analysis(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Return recommended businesses and financial feasibility for the given user profile."""
    recommended = recommend_businesses(user_profile, limit=5)
    top_business = recommended[0] if recommended else {
        "investment_required": 0,
        "estimated_monthly_revenue": 0,
        "estimated_monthly_expenses": 0,
        "estimated_monthly_profit": 0,
        "feasibility_score": 0,
        "risk_level": "High",
    }

    financial = analyze_financials(user_profile, float(top_business["investment_required"]))
    return {
        "recommended_businesses": recommended,
        "financial_analysis": {
            "available_capital": financial["available_capital"],
            "required_investment": financial["required_investment"],
            "loan_required": financial["loan_required"],
            "monthly_profit": financial["monthly_profit"],
            "annual_profit": financial["annual_profit"],
            "break_even_months": financial["break_even_months"],
        },
        "feasibility_score": financial["feasibility_score"],
        "risk_level": financial["risk_level"],
        "recommendation": financial["recommendation"],
    }
