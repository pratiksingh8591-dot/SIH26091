"""Scheme matching service using transparent rule-based eligibility checks."""

from __future__ import annotations

from typing import Any, Dict, List

from app.data.schemes import SCHEME_DATA


def _normalize(value: Any) -> str:
    return str(value or "").strip().lower()


def match_schemes(user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return a list of matches with explanation for each scheme."""
    age = int(user_profile.get("age", 0) or 0)
    annual_income = float(user_profile.get("annual_family_income", 0) or 0)
    social_category = _normalize(user_profile.get("social_category"))
    business_category = _normalize(user_profile.get("business_category"))
    gender = _normalize(user_profile.get("gender"))
    loan_requirement = float(user_profile.get("desired_loan_amount", 0) or 0)

    results: List[Dict[str, Any]] = []

    for scheme in SCHEME_DATA:
        matched_conditions: List[str] = []
        failed_conditions: List[str] = []
        score = 0

        minimum_age = scheme.get("minimum_age")
        maximum_age = scheme.get("maximum_age")
        if minimum_age is not None and age < minimum_age:
            failed_conditions.append("Age below minimum eligibility")
        elif maximum_age is not None and age > maximum_age:
            failed_conditions.append("Age above maximum eligibility")
        else:
            matched_conditions.append("Age within eligible range")
            score += 25

        if scheme.get("min_income") is not None and annual_income < scheme["min_income"]:
            failed_conditions.append("Income below eligibility threshold")
        elif scheme.get("max_income") is not None and annual_income > scheme["max_income"]:
            failed_conditions.append("Income exceeds eligibility limit")
        else:
            matched_conditions.append("Income within eligible range")
            score += 25

        eligible_categories = [str(item).strip().lower() for item in scheme.get("eligible_categories", [])]
        if eligible_categories:
            if social_category in eligible_categories or gender in eligible_categories:
                matched_conditions.append("Category eligible")
                score += 20
            else:
                failed_conditions.append("Social category not eligible for this scheme")

        business_categories = [str(item).strip().lower() for item in scheme.get("business_categories", [])]
        if business_categories:
            if business_category and business_category in business_categories:
                matched_conditions.append("Business category supported")
                score += 20
            else:
                failed_conditions.append("Business category not supported")

        if scheme.get("loan_available"):
            if loan_requirement <= 0:
                matched_conditions.append("Loan need is reasonable for scheme")
                score += 10
            else:
                max_loan = scheme.get("max_loan_amount")
                if max_loan is None or loan_requirement <= float(max_loan):
                    matched_conditions.append("Loan requirement within scheme limit")
                    score += 10
                else:
                    failed_conditions.append("Loan requirement exceeds scheme limit")

        eligible = not failed_conditions
        result = {
            "scheme_name": scheme["scheme_name"],
            "eligible": eligible,
            "match_score": min(100, max(0, score)),
            "matched_conditions": matched_conditions,
            "failed_conditions": failed_conditions,
        }
        results.append(result)

    return results
