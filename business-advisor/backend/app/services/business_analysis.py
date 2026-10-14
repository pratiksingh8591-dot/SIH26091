"""Business recommendation logic."""

from __future__ import annotations

from typing import Any, Dict, List

from app.data.businesses import BUSINESS_DATA
from app.utils.calculations import calculate_feasibility_score, determine_risk_level

SCORE_WEIGHTS = {
    "capital_adequacy": 25,
    "expected_profitability": 25,
    "loan_affordability": 20,
    "risk": 15,
    "business_experience": 15,
}


def recommend_businesses(user_profile: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
    """Recommend businesses by comparing user capital and business requirements."""
    available_capital = float(user_profile.get("available_capital", 0) or 0)
    loan_required = float(user_profile.get("desired_loan_amount", 0) or 0)
    monthly_household_expenses = float(user_profile.get("monthly_household_expenses", 0) or 0)
    user_experience = int(user_profile.get("experience", 0) or 0)
    preferred_category = (user_profile.get("business_category") or "").strip()
    preferred_name = (user_profile.get("preferred_business") or "").strip()

    scored_businesses: List[Dict[str, Any]] = []

    for business in BUSINESS_DATA:
        required_investment = float(business["minimum_investment"])
        if available_capital > 0 and required_investment > available_capital * 1.5:
            continue

        if preferred_category and business["category"].lower() != preferred_category.lower():
            # Allow category preferences to help ranking but don't discard unrelated businesses.
            category_bonus = 0
        else:
            category_bonus = 15

        if preferred_name and business["business_name"].lower() == preferred_name.lower():
            name_bonus = 20
        else:
            name_bonus = 0

        monthly_revenue = float(business["estimated_monthly_revenue"])
        monthly_expenses = float(business["estimated_monthly_expenses"])
        monthly_profit = monthly_revenue - monthly_expenses
        profitability = max(0, min(100, (monthly_profit / max(monthly_revenue, 1)) * 100))
        capital_fit = max(0, min(100, (available_capital / max(required_investment, 1)) * 100))
        experience_fit = min(100, user_experience * 20)
        risk_penalty = 0
        if business["risk_level"] == "High":
            risk_penalty = 10
        elif business["risk_level"] == "Medium":
            risk_penalty = 5

        overall_score = (
            capital_fit * 0.3
            + profitability * 0.25
            + experience_fit * 0.2
            + category_bonus
            + name_bonus
            - risk_penalty
        )

        fee = calculate_feasibility_score(
            available_capital=available_capital,
            required_investment=required_investment,
            monthly_revenue=monthly_revenue,
            monthly_expenses=monthly_expenses,
            user_experience=user_experience,
            loan_required=loan_required,
            monthly_household_expenses=monthly_household_expenses,
            weights=SCORE_WEIGHTS,
        )

        scored_businesses.append(
            {
                "business_name": business["business_name"],
                "investment_required": int(required_investment),
                "estimated_monthly_revenue": int(monthly_revenue),
                "estimated_monthly_expenses": int(monthly_expenses),
                "estimated_monthly_profit": int(monthly_profit),
                "feasibility_score": fee["feasibility_score"],
                "risk_level": determine_risk_level(fee["feasibility_score"]),
                "match_score": round(max(0, min(100, overall_score)), 2),
            }
        )

    scored_businesses.sort(key=lambda item: (item["match_score"], item["feasibility_score"]), reverse=True)
    return scored_businesses[:limit]
