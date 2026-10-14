"""Financial analysis and business feasibility calculations."""

from __future__ import annotations

from typing import Any, Dict

from app.utils.calculations import calculate_feasibility_score, calculate_financials

SCORE_WEIGHTS = {
    "capital_adequacy": 25,
    "expected_profitability": 25,
    "loan_affordability": 20,
    "risk": 15,
    "business_experience": 15,
}


def analyze_financials(user_profile: Dict[str, Any], required_investment: float) -> Dict[str, Any]:
    """Compute financial metrics and feasibility for the user's chosen business profile."""
    available_capital = float(user_profile.get("available_capital", 0) or 0)
    desired_loan_amount = float(user_profile.get("desired_loan_amount", 0) or 0)
    monthly_household_expenses = float(user_profile.get("monthly_household_expenses", 0) or 0)
    expected_monthly_income = float(user_profile.get("expected_monthly_income", 0) or 0)
    experience = int(user_profile.get("experience", 0) or 0)

    monthly_revenue = expected_monthly_income
    monthly_expenses = max(0.0, monthly_household_expenses + (required_investment * 0.12 / 12))
    financials = calculate_financials(
        available_capital=available_capital,
        required_investment=required_investment,
        monthly_revenue=monthly_revenue,
        monthly_expenses=monthly_expenses,
        desired_loan_amount=desired_loan_amount,
    )

    feasibility = calculate_feasibility_score(
        available_capital=available_capital,
        required_investment=required_investment,
        monthly_revenue=monthly_revenue,
        monthly_expenses=monthly_expenses,
        user_experience=experience,
        loan_required=financials["loan_required"],
        monthly_household_expenses=monthly_household_expenses,
        weights=SCORE_WEIGHTS,
    )

    return {
        **financials,
        **feasibility,
    }
