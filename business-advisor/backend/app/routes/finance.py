"""Finance routes for financial calculations."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.models.schemas import FinanceCalculateRequest, FinancialData
from app.services import financial_service

router = APIRouter(prefix="/api/finance", tags=["finance"])


@router.post("/calculate", response_model=FinancialData)
async def calculate_finance(request: FinanceCalculateRequest) -> Dict[str, Any]:
    """Calculate financial details from available margin capital.

    This calculates:
    - Project cost (margin / 0.10)
    - Maximum loan (project_cost * 0.90)
    - Applicable scheme based on project cost
    - Interest rate, tenure, moratorium
    - EMI
    - Complete repayment schedule

    Args:
        request: Request with available_margin_capital

    Returns:
        Complete financial data

    Raises:
        HTTPException: If calculation fails or capital is invalid
    """
    try:
        financial_data = financial_service.calculate_financials(
            available_margin_capital=request.available_margin_capital
        )
        return financial_data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Financial calculation failed: {str(e)}")
