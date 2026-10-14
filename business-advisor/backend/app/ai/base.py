"""Base interface for feasibility models.

This abstract class defines the interface that all feasibility models must implement.
This allows the system to swap between different implementations (rule-based, ML, etc.)
without changing the API layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class FeasibilityModel(ABC):
    """Abstract base class for feasibility prediction models."""

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict feasibility based on input features.

        Args:
            features: Dict containing market_data, financial_data, and business_category

        Returns:
            Dict with feasibility_score and individual indicator scores
        """
        pass
