"""Business-related routes."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.models.schemas import BusinessRecommendationRequest, BusinessCategoryInfo
from app.services.business_analysis import recommend_businesses
from app.services import overpass_service

router = APIRouter(prefix="/api", tags=["business"])


@router.get("/businesses")
def list_businesses() -> List[Dict[str, Any]]:
    from app.data.businesses import BUSINESS_DATA

    return BUSINESS_DATA


@router.post("/business/recommend")
def recommend_business(request: BusinessRecommendationRequest) -> List[Dict[str, Any]]:
    user_profile = request.model_dump()
    results = recommend_businesses(user_profile, limit=5)
    if not results:
        raise HTTPException(status_code=404, detail="No suitable business matches found.")
    return results


@router.get("/business/categories", response_model=List[BusinessCategoryInfo])
def get_business_categories() -> List[Dict[str, Any]]:
    """Get list of supported business categories with OSM tag mappings.

    Returns:
        List of business category information including keys, names, and OSM tags
    """
    return overpass_service.get_supported_categories()
