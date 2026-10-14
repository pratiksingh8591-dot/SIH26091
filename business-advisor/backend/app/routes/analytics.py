"""Business intelligence and location analytics endpoints."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services import ml_service

router = APIRouter(prefix="/api", tags=["business intelligence"])


class ClusterFitRequest(BaseModel):
    n_clusters: int = Field(default=3, ge=2, le=8)


class BusinessPredictionRequest(BaseModel):
    features: Dict[str, Any]


@router.post("/clustering/fit")
def fit_clustering(request: ClusterFitRequest) -> Dict[str, Any]:
    try:
        return ml_service.fit_location_clusters(n_clusters=request.n_clusters)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/clustering/results")
def get_clustering_results(
    n_clusters: int = Query(default=3, ge=2, le=8),
) -> Dict[str, Any]:
    try:
        return ml_service.load_or_fit_location_clusters(n_clusters=n_clusters)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/business/predict")
def predict_business(request: BusinessPredictionRequest) -> Dict[str, Any]:
    try:
        return ml_service.predict_business_success(request.features)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/business/model-metrics")
def get_business_model_metrics() -> Dict[str, Any]:
    return ml_service.business_model_metrics()


@router.get("/locations/compare")
def compare_locations(names: List[str] = Query(..., min_length=1, max_length=8)) -> Dict[str, Any]:
    """Compare selected project locations using the current clustering output."""
    try:
        result = ml_service.load_or_fit_location_clusters()
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    requested = {name.strip().casefold() for name in names if name.strip()}
    if not requested:
        raise HTTPException(status_code=422, detail="At least one location name is required.")
    locations = [
        location for location in result["locations"]
        if location["location_name"].casefold() in requested
    ]
    return {
        "locations": locations,
        "not_found": sorted(requested - {location["location_name"].casefold() for location in locations}),
        "feature_columns": result["feature_columns"],
    }
