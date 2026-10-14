"""Analysis routes for main business analysis endpoint."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services import (
    feasibility_service,
    financial_service,
    geospatial_service,
    overpass_service,
    population_service,
    ml_service,
)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_business(request: AnalyzeRequest) -> Dict[str, Any]:
    """Complete business feasibility analysis.

    This is the main endpoint that combines:
    - Competitor data from OpenStreetMap
    - Geospatial calculations
    - Population data
    - Financial calculations (project cost, loan, scheme, EMI)
    - Feasibility scoring

    Args:
        request: Analysis request with location, business, capital, radius

    Returns:
        Complete analysis response with market, feasibility, and financial data

    Raises:
        HTTPException: If analysis fails or inputs are invalid
    """
    data_sources = []
    limitations = []

    # 1. Fetch competitors from Overpass API
    competitor_search_status = "unavailable"
    competitor_search_message = None
    try:
        competitors = await overpass_service.fetch_competitors(
            latitude=request.location.latitude,
            longitude=request.location.longitude,
            business_category=request.business.category,
            radius_km=request.radius_km,
        )
        data_sources.append("OpenStreetMap/Overpass API")
        competitor_search_status = getattr(
            competitors,
            "status",
            "found" if competitors else "completed_empty",
        )
        competitor_search_message = getattr(competitors, "message", None)

        if not competitors:
            limitations.append(
                f"No competitors found for {request.business.category} within {request.radius_km} km. "
                "This may indicate an untapped market or incomplete OSM data for this region."
            )
        elif competitor_search_status == "incomplete":
            limitations.append(
                "Overpass returned an incomplete result; competitor counts may be understated."
            )
    except overpass_service.OverpassUnavailableError as e:
        # Don't fail the entire analysis if Overpass is unavailable
        competitors = []
        competitor_search_status = "unavailable"
        competitor_search_message = str(e)
        limitations.append(
            "Competitor data unavailable because the OpenStreetMap search failed. "
            "Zero competitors must not be interpreted as a confirmed empty market."
        )
    except Exception as e:
        competitors = []
        competitor_search_status = "unavailable"
        competitor_search_message = str(e)
        limitations.append(f"Competitor data unavailable: {str(e)}")

    # 2. Calculate geospatial metrics
    competitors_with_distance = geospatial_service.calculate_all_distances(
        competitors,
        request.location.latitude,
        request.location.longitude,
    )

    competitor_count = len(competitors_with_distance)
    density = geospatial_service.competitor_density(competitor_count, request.radius_km)
    avg_distance = geospatial_service.average_competitor_distance(
        competitors_with_distance,
        request.location.latitude,
        request.location.longitude,
    )
    nearest = geospatial_service.nearest_competitor(
        competitors_with_distance,
        request.location.latitude,
        request.location.longitude,
    )
    nearest_distance = nearest["distance_km"] if nearest else None

    # 3. Get population data
    try:
        population_data = population_service.get_population_within_radius(
            latitude=request.location.latitude,
            longitude=request.location.longitude,
            radius_km=request.radius_km,
        )
        population = population_data.get("population")
        population_source = population_data.get("source")
        population_note = population_data.get("note")

        if population:
            data_sources.append(population_source)
        else:
            limitations.append("Population data unavailable for this location")
    except Exception as e:
        population = None
        population_source = None
        population_note = f"Error fetching population data: {str(e)}"
        limitations.append(population_note)

    # 4. Calculate financial data
    try:
        financial_data = financial_service.calculate_financials(
            available_margin_capital=request.available_margin_capital
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Financial calculation failed: {str(e)}")

    # 5. Calculate feasibility
    market_data_for_scoring = {
        "population": population,
        "competitor_count": competitor_count,
        "competitor_density": density,
        "average_distance": avg_distance,
        "nearest_distance": nearest_distance,
    }

    try:
        feasibility_data = feasibility_service.calculate_feasibility(
            market_data=market_data_for_scoring,
            financial_data=financial_data,
            business_category=request.business.category,
        )
        limitations.extend(feasibility_data.get("limitations", []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feasibility calculation failed: {str(e)}")

    # 6. Add ML analytics without making the existing analysis dependent on it.
    analytics = None
    try:
        clustering = ml_service.load_or_fit_location_clusters()
        selected = min(
            clustering["locations"],
            key=lambda location: (
                (location["latitude"] - request.location.latitude) ** 2
                + (location["longitude"] - request.location.longitude) ** 2
            ),
        )
        analytics = {
            "clustering": {"selected_location": selected, **clustering},
            "business_prediction": ml_service.business_model_metrics(),
        }
    except (RuntimeError, ValueError) as exc:
        limitations.append(f"Location analytics unavailable: {str(exc)}")

    # 7. Build response
    return {
        "input": request.dict(),
        "market": {
            "population": population,
            "population_source": population_source,
            "population_note": population_note,
            "competitors": competitors_with_distance,
            "competitor_count": competitor_count,
            "competitor_density": density,
            "average_distance": avg_distance,
            "nearest_distance": nearest_distance,
            "competitor_search_status": competitor_search_status,
            "competitor_search_message": competitor_search_message,
        },
        "feasibility": feasibility_data,
        "financial": financial_data,
        "data_sources": data_sources,
        "limitations": list(set(limitations)),  # Remove duplicates
        "analytics": analytics,
    }
