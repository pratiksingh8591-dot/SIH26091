"""Tests for Overpass service."""

import asyncio
import pytest
import httpx
from app.services import overpass_service


def test_build_overpass_query():
    """Test Overpass query building."""
    query = overpass_service.build_overpass_query(19.0760, 72.8777, 5000, "restaurant")

    assert '["amenity"="restaurant"]' in query
    assert '["amenity=restaurant"]' not in query
    assert "around:5000" in query
    assert "19.076" in query
    assert "72.8777" in query


def test_build_overpass_query_unsupported_category():
    """Test query building with unsupported category."""
    query = overpass_service.build_overpass_query(19.0760, 72.8777, 5000, "unsupported")

    # Should return empty result query
    assert "node(0)" in query or len(query) < 100


def test_normalize_competitor_node():
    """Test normalizing a node element."""
    element = {
        "type": "node",
        "id": 123,
        "lat": 19.0800,
        "lon": 72.8800,
        "tags": {
            "name": "Test Restaurant",
            "amenity": "restaurant"
        }
    }

    result = overpass_service.normalize_competitor(element)

    assert result is not None
    assert result["name"] == "Test Restaurant"
    assert result["latitude"] == 19.0800
    assert result["longitude"] == 72.8800
    assert result["category"] == "restaurant"
    assert result["source"] == "OpenStreetMap"


def test_normalize_competitor_way():
    """Test normalizing a way element."""
    element = {
        "type": "way",
        "id": 456,
        "center": {
            "lat": 19.0800,
            "lon": 72.8800
        },
        "tags": {
            "name": "Test Shop",
            "shop": "bakery"
        }
    }

    result = overpass_service.normalize_competitor(element)

    assert result is not None
    assert result["name"] == "Test Shop"
    assert result["latitude"] == 19.0800
    assert result["category"] == "bakery"


def test_normalize_competitor_missing_coords():
    """Test normalizing element with missing coordinates."""
    element = {
        "type": "node",
        "id": 123,
        "tags": {"name": "Test"}
    }

    result = overpass_service.normalize_competitor(element)
    assert result is None


def test_get_supported_categories():
    """Test getting supported categories."""
    categories = overpass_service.get_supported_categories()

    assert len(categories) > 0
    assert all("key" in cat for cat in categories)
    assert all("name" in cat for cat in categories)
    assert all("osm_tags" in cat for cat in categories)

    # Check some expected categories
    category_keys = [cat["key"] for cat in categories]
    assert "restaurant" in category_keys
    assert "bakery" in category_keys
    assert "pharmacy" in category_keys


def test_category_mapping():
    """Test that category mapping is properly defined."""
    mapping = overpass_service.CATEGORY_TO_OSM_TAG

    assert "restaurant" in mapping
    assert "bakery" in mapping
    assert isinstance(mapping["restaurant"], list)
    assert len(mapping["restaurant"]) > 0


def test_overpass_urls_include_primary_and_fallbacks(monkeypatch):
    monkeypatch.setenv("OVERPASS_URL", "https://primary.example/api")
    monkeypatch.setenv(
        "OVERPASS_FALLBACK_URLS",
        "https://fallback.example/api,https://primary.example/api",
    )

    assert overpass_service.get_overpass_urls() == [
        "https://primary.example/api",
        "https://fallback.example/api",
    ]


def test_fetch_retries_406_then_uses_fallback(monkeypatch):
    class FakeResponse:
        def __init__(self, status_code, payload=None):
            self.status_code = status_code
            self.request = httpx.Request("POST", "https://example.test")
            self._payload = payload

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "failed", request=self.request, response=self
                )

        def json(self):
            return self._payload

    class FakeClient:
        calls = []

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, endpoint, **kwargs):
            self.calls.append(endpoint)
            if endpoint.startswith("https://primary"):
                return FakeResponse(406)
            return FakeResponse(200, {"elements": []})

    monkeypatch.setenv("OVERPASS_URL", "https://primary.example/api")
    monkeypatch.setenv("OVERPASS_FALLBACK_URLS", "https://fallback.example/api")
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: FakeClient())

    result = asyncio.run(
        overpass_service.fetch_competitors(19.07, 72.87, "restaurant", 5)
    )

    assert result == []
    assert "https://fallback.example/api" in FakeClient.calls


def test_fetch_raises_unavailable_after_failed_endpoints(monkeypatch):
    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, endpoint, **kwargs):
            request = httpx.Request("POST", endpoint)
            response = httpx.Response(503, request=request)
            raise httpx.HTTPStatusError("failed", request=request, response=response)

    monkeypatch.setenv("OVERPASS_URL", "https://primary.example/api")
    monkeypatch.setenv("OVERPASS_FALLBACK_URLS", "")
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: FakeClient())

    with pytest.raises(overpass_service.OverpassUnavailableError):
        asyncio.run(
            overpass_service.fetch_competitors(19.07, 72.87, "restaurant", 5)
        )


def test_competitor_search_result_preserves_incomplete_status():
    result = overpass_service.CompetitorSearchResult(
        [{"name": "Example"}],
        status="incomplete",
        message="timeout",
    )

    assert isinstance(result, list)
    assert result.status == "incomplete"
    assert result.message == "timeout"
