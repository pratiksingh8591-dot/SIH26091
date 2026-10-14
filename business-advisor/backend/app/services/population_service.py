"""Population service for retrieving population data."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.services import geospatial_service

# Sample population data for MVP
# In production, this should come from a database or CSV file with real Census data
SAMPLE_POPULATION_DATA = [
    {
        "location_name": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "population": 12442373,
        "area_type": "city",
    },
    {
        "location_name": "Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "population": 3124458,
        "area_type": "city",
    },
    {
        "location_name": "Delhi",
        "latitude": 28.7041,
        "longitude": 77.1025,
        "population": 11034555,
        "area_type": "city",
    },
    {
        "location_name": "Bangalore",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "population": 8443675,
        "area_type": "city",
    },
    {
        "location_name": "Hyderabad",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "population": 6993262,
        "area_type": "city",
    },
    {
        "location_name": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "population": 4646732,
        "area_type": "city",
    },
    {
        "location_name": "Kolkata",
        "latitude": 22.5726,
        "longitude": 88.3639,
        "population": 4496694,
        "area_type": "city",
    },
]


def get_population_within_radius(
    latitude: float,
    longitude: float,
    radius_km: float,
) -> Dict[str, Any]:
    """Get population data within a given radius.

    For MVP, uses sample data. In production, this should query a database
    with actual Census data or government population statistics.

    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius in kilometers

    Returns:
        Dict with population, source, and confidence information
    """
    # Find population records within radius
    matching_records = []

    for record in SAMPLE_POPULATION_DATA:
        record_lat = record.get("latitude")
        record_lon = record.get("longitude")

        if record_lat is None or record_lon is None:
            continue

        distance = geospatial_service.distance_between_points(
            latitude, longitude, record_lat, record_lon
        )

        if distance <= radius_km:
            matching_records.append(
                {
                    "location_name": record["location_name"],
                    "population": record["population"],
                    "distance_km": distance,
                    "area_type": record.get("area_type", "unknown"),
                }
            )

    # If we found matching records, aggregate population
    if matching_records:
        # For MVP, we'll use the closest record's population
        # In production, more sophisticated aggregation would be needed
        closest_record = min(matching_records, key=lambda x: x["distance_km"])

        return {
            "population": closest_record["population"],
            "source": "Census 2011 (Sample Data)",
            "confidence": "baseline",
            "location_name": closest_record["location_name"],
            "distance_from_center_km": closest_record["distance_km"],
            "note": "Population estimate based on nearest major city. For production use, integrate with actual Census API or detailed district-level data.",
        }

    # No matching records found
    return {
        "population": None,
        "source": "Census 2011 (Sample Data)",
        "confidence": "unavailable",
        "note": "No population data available for this location. Add more population records to the database.",
    }


def get_population_estimate_simple(latitude: float, longitude: float) -> Optional[int]:
    """Get simple population estimate for a location.

    Returns just the population number or None if unavailable.

    Args:
        latitude: Latitude
        longitude: Longitude

    Returns:
        Population estimate or None
    """
    # Use a default radius of 50 km for simple estimate
    result = get_population_within_radius(latitude, longitude, radius_km=50)
    return result.get("population")
