"""Route layer for feasibility and full analysis."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from app.models.schemas import EntrepreneurProfile, FeasibilityRequest
from app.services.business_analysis import recommend_businesses
from app.services.financial_analysis import analyze_financials
from app.services.scheme_matching import match_schemes

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/feasibility")
def calculate_feasibility(request: FeasibilityRequest) -> Dict[str, Any]:
    required_investment = float(request.preferred_business and 100000 or 0)
    financial = analyze_financials(
        user_profile=request.model_dump(),
        required_investment=required_investment,
    )
    return {
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


@router.post("/analyze")
def full_analysis(request: EntrepreneurProfile) -> Dict[str, Any]:
    user_profile = request.model_dump()
    recommended = recommend_businesses(user_profile, limit=5)
    top_business = recommended[0] if recommended else {
        "investment_required": 0,
        "estimated_monthly_revenue": 0,
        "estimated_monthly_expenses": 0,
        "estimated_monthly_profit": 0,
    }
    financial = analyze_financials(user_profile, float(top_business["investment_required"]))
    matches = match_schemes(user_profile)

    return {
        "user_profile": user_profile,
        "recommended_businesses": recommended,
        "financial_analysis": {
            "available_capital": financial["available_capital"],
            "required_investment": financial["required_investment"],
            "loan_required": financial["loan_required"],
            "monthly_profit": financial["monthly_profit"],
            "annual_profit": financial["annual_profit"],
            "break_even_months": financial["break_even_months"],
        },
        "scheme_matches": matches,
    }
