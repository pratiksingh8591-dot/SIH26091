"""Geospatial service for distance and density calculations."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from geopy.distance import geodesic


def distance_between_points(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using geodesic calculation.

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Distance in kilometers
    """
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    distance = geodesic(point1, point2).kilometers
    return round(distance, 2)


def filter_by_radius(
    competitors: List[Dict[str, Any]],
    center_lat: float,
    center_lon: float,
    radius_km: float,
) -> List[Dict[str, Any]]:
    """Filter competitors within a given radius.

    Args:
        competitors: List of competitor dicts with 'latitude' and 'longitude'
        center_lat: Center latitude
        center_lon: Center longitude
        radius_km: Radius in kilometers

    Returns:
        Filtered list of competitors within radius
    """
    filtered = []
    for competitor in competitors:
        lat = competitor.get("latitude")
        lon = competitor.get("longitude")
        if lat is None or lon is None:
            continue

        distance = distance_between_points(center_lat, center_lon, lat, lon)
        if distance <= radius_km:
            # Add distance to competitor data
            competitor_with_distance = competitor.copy()
            competitor_with_distance["distance_km"] = distance
            filtered.append(competitor_with_distance)

    return filtered


def average_competitor_distance(
    competitors: List[Dict[str, Any]],
    center_lat: float,
    center_lon: float,
) -> Optional[float]:
    """Calculate average distance from center to all competitors.

    Args:
        competitors: List of competitor dicts with 'latitude' and 'longitude'
        center_lat: Center latitude
        center_lon: Center longitude

    Returns:
        Average distance in kilometers or None if no competitors
    """
    if not competitors:
        return None

    total_distance = 0.0
    count = 0

    for competitor in competitors:
        lat = competitor.get("latitude")
        lon = competitor.get("longitude")
        if lat is None or lon is None:
            continue

        distance = distance_between_points(center_lat, center_lon, lat, lon)
        total_distance += distance
        count += 1

    if count == 0:
        return None

    return round(total_distance / count, 2)


def nearest_competitor(
    competitors: List[Dict[str, Any]],
    center_lat: float,
    center_lon: float,
) -> Optional[Dict[str, Any]]:
    """Find the nearest competitor to the center point.

    Args:
        competitors: List of competitor dicts with 'latitude' and 'longitude'
        center_lat: Center latitude
        center_lon: Center longitude

    Returns:
        Nearest competitor dict with 'distance_km' added, or None if no competitors
    """
    if not competitors:
        return None

    nearest = None
    min_distance = float("inf")

    for competitor in competitors:
        lat = competitor.get("latitude")
        lon = competitor.get("longitude")
        if lat is None or lon is None:
            continue

        distance = distance_between_points(center_lat, center_lon, lat, lon)
        if distance < min_distance:
            min_distance = distance
            nearest = competitor.copy()
            nearest["distance_km"] = distance

    return nearest


def competitor_density(competitor_count: int, radius_km: float) -> float:
    """Calculate competitor density as competitors per square kilometer.

    Args:
        competitor_count: Number of competitors
        radius_km: Radius in kilometers

    Returns:
        Density as competitors per square kilometer
    """
    if radius_km <= 0:
        return 0.0

    # Calculate area (π * r²)
    area_sq_km = math.pi * (radius_km ** 2)

    if area_sq_km == 0:
        return 0.0

    density = competitor_count / area_sq_km
    return round(density, 4)


def calculate_all_distances(
    competitors: List[Dict[str, Any]],
    center_lat: float,
    center_lon: float,
) -> List[Dict[str, Any]]:
    """Add distance_km field to all competitors.

    Args:
        competitors: List of competitor dicts with 'latitude' and 'longitude'
        center_lat: Center latitude
        center_lon: Center longitude

    Returns:
        List of competitors with distance_km added
    """
    result = []
    for competitor in competitors:
        lat = competitor.get("latitude")
        lon = competitor.get("longitude")
        if lat is None or lon is None:
            continue

        competitor_with_distance = competitor.copy()
        competitor_with_distance["distance_km"] = distance_between_points(
            center_lat, center_lon, lat, lon
        )
        result.append(competitor_with_distance)

    return result
