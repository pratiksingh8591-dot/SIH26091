"""Calculation utilities for business feasibility and financial analysis."""

from __future__ import annotations

from typing import Any, Dict


def round_money(value: float) -> float:
    return round(float(value), 2)


def calculate_financials(
    available_capital: float,
    required_investment: float,
    monthly_revenue: float,
    monthly_expenses: float,
    desired_loan_amount: float = 0,
) -> Dict[str, Any]:
    """Compute core business and financing metrics."""
    loan_requirement = max(0.0, float(required_investment) - float(available_capital))
    effective_loan = max(0.0, float(desired_loan_amount))
    monthly_profit = float(monthly_revenue) - float(monthly_expenses)
    annual_profit = monthly_profit * 12
    break_even_months = 0
    if monthly_profit > 0 and required_investment > 0:
        break_even_months = round((required_investment / monthly_profit), 2)

    return {
        "available_capital": round_money(available_capital),
        "required_investment": round_money(required_investment),
        "loan_required": round_money(max(loan_requirement, effective_loan)),
        "monthly_revenue": round_money(monthly_revenue),
        "monthly_expenses": round_money(monthly_expenses),
        "monthly_profit": round_money(monthly_profit),
        "annual_profit": round_money(annual_profit),
        "break_even_months": break_even_months,
    }


def calculate_affordability(available_capital: float, loan_required: float, monthly_household_expenses: float) -> float:
    """Return a normalized affordability score between 0 and 100."""
    if available_capital <= 0:
        return 0.0
    base = (available_capital / max(loan_required + available_capital, 1)) * 100
    household_pressure = max(0.0, 100 - (monthly_household_expenses / max(available_capital, 1)) * 100)
    return max(0.0, min(100.0, (base * 0.7) + (household_pressure * 0.3)))


def determine_risk_level(score: float) -> str:
    if score >= 75:
        return "Low"
    if score >= 45:
        return "Medium"
    return "High"


def calculate_feasibility_score(
    available_capital: float,
    required_investment: float,
    monthly_revenue: float,
    monthly_expenses: float,
    user_experience: int,
    loan_required: float,
    monthly_household_expenses: float,
    weights: Dict[str, float],
) -> Dict[str, Any]:
    """Compute a transparent feasibility score based on weighted factors."""
    capital_ratio = 0.0
    if required_investment > 0:
        capital_ratio = min(100.0, (available_capital / required_investment) * 100)

    monthly_profit = monthly_revenue - monthly_expenses
    profitability_ratio = 0.0
    if monthly_revenue > 0:
        profitability_ratio = min(100.0, (monthly_profit / monthly_revenue) * 100)

    affordability_score = calculate_affordability(available_capital, loan_required, monthly_household_expenses)

    risk_value = 0.0
    if monthly_revenue > 0:
        risk_value = max(0.0, 100.0 - ((monthly_expenses / monthly_revenue) * 100))

    experience_score = min(100.0, user_experience * 20)

    total = (
        (capital_ratio * weights.get("capital_adequacy", 25) / 100)
        + (profitability_ratio * weights.get("expected_profitability", 25) / 100)
        + (affordability_score * weights.get("loan_affordability", 20) / 100)
        + (risk_value * weights.get("risk", 15) / 100)
        + (experience_score * weights.get("business_experience", 15) / 100)
    )

    final_score = max(0.0, min(100.0, total))
    level = determine_risk_level(final_score)

    if final_score >= 70:
        recommendation = "Feasible"
    elif final_score >= 45:
        recommendation = "Needs review"
    else:
        recommendation = "Not feasible"

    return {
        "feasibility_score": round_money(final_score),
        "risk_level": level,
        "recommendation": recommendation,
    }
