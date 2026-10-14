"""Tests for geospatial service."""

import pytest
from app.services import geospatial_service


def test_distance_between_points():
    """Test distance calculation between two points."""
    # Mumbai to Pune (approximate)
    mumbai = (19.0760, 72.8777)
    pune = (18.5204, 73.8567)

    distance = geospatial_service.distance_between_points(*mumbai, *pune)

    # Distance should be around 120-150 km
    assert 100 < distance < 200
    assert isinstance(distance, float)


def test_distance_same_point():
    """Test distance when points are the same."""
    distance = geospatial_service.distance_between_points(19.0760, 72.8777, 19.0760, 72.8777)
    assert distance == 0


def test_filter_by_radius():
    """Test filtering competitors by radius."""
    center_lat, center_lon = 19.0760, 72.8777

    competitors = [
        {"name": "Close", "latitude": 19.0800, "longitude": 72.8800},
        {"name": "Far", "latitude": 20.0000, "longitude": 74.0000},
        {"name": "Medium", "latitude": 19.1000, "longitude": 72.9000},
    ]

    filtered = geospatial_service.filter_by_radius(competitors, center_lat, center_lon, 10)

    # Should include close and medium, exclude far
    assert len(filtered) <= len(competitors)
    assert all("distance_km" in comp for comp in filtered)


def test_average_competitor_distance():
    """Test average distance calculation."""
    center_lat, center_lon = 19.0760, 72.8777

    competitors = [
        {"latitude": 19.0800, "longitude": 72.8800},
        {"latitude": 19.0900, "longitude": 72.8900},
    ]

    avg_distance = geospatial_service.average_competitor_distance(competitors, center_lat, center_lon)

    assert avg_distance is not None
    assert avg_distance > 0
    assert isinstance(avg_distance, float)


def test_average_competitor_distance_empty():
    """Test average distance with no competitors."""
    avg_distance = geospatial_service.average_competitor_distance([], 19.0760, 72.8777)
    assert avg_distance is None


def test_nearest_competitor():
    """Test finding nearest competitor."""
    center_lat, center_lon = 19.0760, 72.8777

    competitors = [
        {"name": "Far", "latitude": 19.2000, "longitude": 72.9000},
        {"name": "Close", "latitude": 19.0800, "longitude": 72.8800},
        {"name": "Medium", "latitude": 19.1500, "longitude": 72.8900},
    ]

    nearest = geospatial_service.nearest_competitor(competitors, center_lat, center_lon)

    assert nearest is not None
    assert nearest["name"] == "Close"
    assert "distance_km" in nearest


def test_nearest_competitor_empty():
    """Test nearest competitor with no competitors."""
    nearest = geospatial_service.nearest_competitor([], 19.0760, 72.8777)
    assert nearest is None


def test_competitor_density():
    """Test competitor density calculation."""
    # 10 competitors in 5 km radius
    density = geospatial_service.competitor_density(10, 5)

    # Density = competitors / (π * r²)
    # Density = 10 / (π * 25) ≈ 0.127
    assert 0.1 < density < 0.2
    assert isinstance(density, float)


def test_competitor_density_zero_radius():
    """Test density with zero radius."""
    density = geospatial_service.competitor_density(10, 0)
    assert density == 0


def test_calculate_all_distances():
    """Test adding distances to all competitors."""
    center_lat, center_lon = 19.0760, 72.8777

    competitors = [
        {"name": "A", "latitude": 19.0800, "longitude": 72.8800},
        {"name": "B", "latitude": 19.0900, "longitude": 72.8900},
    ]

    result = geospatial_service.calculate_all_distances(competitors, center_lat, center_lon)

    assert len(result) == 2
    assert all("distance_km" in comp for comp in result)
    assert all(comp["distance_km"] > 0 for comp in result)
