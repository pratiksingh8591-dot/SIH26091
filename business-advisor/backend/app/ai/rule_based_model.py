"""Rule-based feasibility model implementation.

This is the current MVP implementation using deterministic scoring rules.
In the future, this can be replaced by a trained ML model (ml_model.py)
without changing the API interface.
"""

from __future__ import annotations

from typing import Any, Dict

from app.ai.base import FeasibilityModel
from app.services.feasibility_service import calculate_feasibility


class RuleBasedFeasibilityModel(FeasibilityModel):
    """Rule-based feasibility model using transparent deterministic scoring."""

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict feasibility using rule-based scoring.

        Args:
            features: Dict with 'market_data', 'financial_data', 'business_category'

        Returns:
            Dict with feasibility scores
        """
        market_data = features.get("market_data", {})
        financial_data = features.get("financial_data", {})
        business_category = features.get("business_category", "")

        return calculate_feasibility(
            market_data=market_data,
            financial_data=financial_data,
            business_category=business_category,
        )


# Future: Placeholder for ML model
# class MLFeasibilityModel(FeasibilityModel):
#     """Machine learning-based feasibility model."""
#
#     def __init__(self, model_path: str):
#         self.model = load_model(model_path)
#
#     def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
#         # Use trained ML model for prediction
#         pass
