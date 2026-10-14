"""Market data routes for competitors and population."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.models.schemas import MarketCompetitorsRequest, MarketPopulationRequest
from app.services import geospatial_service, overpass_service, population_service

router = APIRouter(prefix="/api/market", tags=["market"])


@router.post("/competitors")
async def get_competitors(request: MarketCompetitorsRequest) -> Dict[str, Any]:
    """Fetch competitor data from OpenStreetMap.

    Args:
        request: Location, business category, and radius

    Returns:
        Dict with competitors list and metrics

    Raises:
        HTTPException: If request fails
    """
    try:
        competitors = await overpass_service.fetch_competitors(
            latitude=request.latitude,
            longitude=request.longitude,
            business_category=request.business_category,
            radius_km=request.radius_km,
        )

        # Calculate distances
        competitors_with_distance = geospatial_service.calculate_all_distances(
            competitors,
            request.latitude,
            request.longitude,
        )

        # Calculate metrics
        competitor_count = len(competitors_with_distance)
        density = geospatial_service.competitor_density(competitor_count, request.radius_km)
        avg_distance = geospatial_service.average_competitor_distance(
            competitors_with_distance,
            request.latitude,
            request.longitude,
        )
        nearest = geospatial_service.nearest_competitor(
            competitors_with_distance,
            request.latitude,
            request.longitude,
        )
        nearest_distance = nearest["distance_km"] if nearest else None

        return {
            "competitors": competitors_with_distance,
            "competitor_count": competitor_count,
            "search_status": getattr(
                competitors,
                "status",
                "found" if competitors_with_distance else "completed_empty",
            ),
            "search_message": getattr(
                competitors,
                "message",
                "Search completed successfully; no mapped competitors were found."
                if not competitors_with_distance
                else "Search completed successfully.",
            ),
            "competitor_density": density,
            "average_distance": avg_distance,
            "nearest_distance": nearest_distance,
            "source": "OpenStreetMap",
        }

    except overpass_service.OverpassUnavailableError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Competitor data is temporarily unavailable.",
                "search_status": "unavailable",
                "reason": str(e),
            },
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch competitors: {str(e)}")


@router.post("/population")
async def get_population(request: MarketPopulationRequest) -> Dict[str, Any]:
    """Get population data for a location.

    Args:
        request: Location and radius

    Returns:
        Dict with population data and source information

    Raises:
        HTTPException: If request fails
    """
    try:
        population_data = population_service.get_population_within_radius(
            latitude=request.latitude,
            longitude=request.longitude,
            radius_km=request.radius_km,
        )
        return population_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch population data: {str(e)}")
