"""Overpass API service for fetching competitor data from OpenStreetMap."""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List

import httpx

# Business category to OSM tag mapping
CATEGORY_TO_OSM_TAG = {
    "bakery": ["shop=bakery"],
    "restaurant": ["amenity=restaurant"],
    "cafe": ["amenity=cafe"],
    "pharmacy": ["amenity=pharmacy"],
    "grocery": ["shop=supermarket", "shop=convenience"],
    "mobile_phone": ["shop=mobile_phone"],
    "clothing": ["shop=clothes"],
    "hardware": ["shop=hardware"],
    "electronics": ["shop=electronics"],
    "beauty_salon": ["shop=beauty", "shop=hairdresser"],
    "repair": ["shop=repair"],
    "general_store": ["shop=general"],
}

REQUEST_TIMEOUT = float(os.getenv("OVERPASS_TIMEOUT_SECONDS", "30"))
MAX_RETRIES = 2
RETRYABLE_STATUS_CODES = {406, 408, 425, 429, 500, 502, 503, 504}


class OverpassUnavailableError(httpx.HTTPError):
    """Raised when all configured Overpass endpoints fail."""

    def __init__(self, message: str, status_codes: List[int] | None = None):
        super().__init__(message)
        self.status_codes = status_codes or []


class CompetitorSearchResult(list):
    """List-compatible competitor result with source completeness metadata."""

    def __init__(self, competitors: List[Dict[str, Any]], status: str, message: str | None = None):
        super().__init__(competitors)
        self.status = status
        self.message = message


def get_overpass_urls() -> List[str]:
    """Return unique configured endpoints in primary-then-fallback order."""
    configured = [
        os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter"),
        *os.getenv(
            "OVERPASS_FALLBACK_URLS",
            "https://overpass.kumi.systems/api/interpreter,"
            "https://overpass.private.coffee/api/interpreter",
        ).split(","),
    ]
    return list(dict.fromkeys(url.strip() for url in configured if url.strip()))


def build_overpass_query(lat: float, lon: float, radius_m: float, business_category: str) -> str:
    """Build an Overpass QL query for fetching competitors.

    Args:
        lat: Latitude of center point
        lon: Longitude of center point
        radius_m: Search radius in meters
        business_category: Business category key from CATEGORY_TO_OSM_TAG

    Returns:
        Overpass QL query string
    """
    tags = CATEGORY_TO_OSM_TAG.get(business_category.lower(), [])

    if not tags:
        # If category not in mapping, return empty result query
        return "[out:json];(node(0)(0,0,0,0););out;"

    # Build query for all tags in the category
    node_queries = []
    way_queries = []

    for tag in tags:
        key, value = tag.split("=", 1)
        node_queries.append(f'node["{key}"="{value}"](around:{radius_m},{lat},{lon})')
        way_queries.append(f'way["{key}"="{value}"](around:{radius_m},{lat},{lon})')

    query_parts = node_queries + way_queries
    query_body = ";".join(query_parts)

    query = f"""
    [out:json][timeout:25];
    (
        {query_body};
    );
    out center;
    """

    return query.strip()


def normalize_competitor(element: Dict[str, Any]) -> Dict[str, Any] | None:
    """Extract competitor data from OSM element.

    Args:
        element: Raw OSM element from Overpass response

    Returns:
        Normalized competitor dict or None if invalid
    """
    tags = element.get("tags", {})
    name = tags.get("name")

    # Get coordinates
    if element.get("type") == "node":
        lat = element.get("lat")
        lon = element.get("lon")
    elif element.get("type") == "way" and "center" in element:
        lat = element["center"].get("lat")
        lon = element["center"].get("lon")
    else:
        return None

    if lat is None or lon is None:
        return None

    # Determine category from tags
    category = "unknown"
    for cat_key, osm_tags in CATEGORY_TO_OSM_TAG.items():
        for osm_tag in osm_tags:
            key, value = osm_tag.split("=")
            if tags.get(key) == value:
                category = cat_key
                break

    osm_id = f"{element.get('type', 'unknown')}/{element.get('id', 'unknown')}"

    return {
        "name": name,
        "latitude": float(lat),
        "longitude": float(lon),
        "category": category,
        "osm_id": osm_id,
        "source": "OpenStreetMap",
    }


async def fetch_competitors(
    latitude: float,
    longitude: float,
    business_category: str,
    radius_km: float,
) -> List[Dict[str, Any]]:
    """Fetch competitors from Overpass API.

    Args:
        latitude: Center latitude
        longitude: Center longitude
        business_category: Business category (e.g., 'bakery', 'restaurant')
        radius_km: Search radius in kilometers

    Returns:
        List of competitor dictionaries

    Raises:
        httpx.HTTPError: If API request fails
        httpx.TimeoutException: If request times out
    """
    radius_m = radius_km * 1000  # Convert km to meters

    query = build_overpass_query(latitude, longitude, radius_m, business_category)

    headers = {
        "Accept": "application/json",
        "User-Agent": os.getenv(
            "OVERPASS_USER_AGENT",
            "SIH26091-BusinessAdvisor/1.0 (contact: maintainers@example.invalid)",
        ),
    }
    failures: List[str] = []
    status_codes: List[int] = []
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
        for endpoint in get_overpass_urls():
            for attempt in range(MAX_RETRIES + 1):
                try:
                    response = await client.post(
                        endpoint,
                        data={"data": query},
                        headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
                    )
                    if response.status_code in RETRYABLE_STATUS_CODES:
                        status_codes.append(response.status_code)
                        raise httpx.HTTPStatusError(
                            f"Overpass returned HTTP {response.status_code}",
                            request=response.request,
                            response=response,
                        )
                    response.raise_for_status()
                    data = response.json()
                    break
                except httpx.TimeoutException as exc:
                    failures.append(f"{endpoint}: timeout")
                    if attempt >= MAX_RETRIES:
                        break
                    await asyncio.sleep(0.5 * (2 ** attempt))
                except httpx.HTTPStatusError as exc:
                    failures.append(f"{endpoint}: HTTP {exc.response.status_code}")
                    if exc.response.status_code not in RETRYABLE_STATUS_CODES or attempt >= MAX_RETRIES:
                        break
                    await asyncio.sleep(0.5 * (2 ** attempt))
                except (httpx.HTTPError, ValueError) as exc:
                    failures.append(f"{endpoint}: {type(exc).__name__}")
                    break
            else:
                continue
            if "data" in locals():
                break
    if "data" not in locals():
        raise OverpassUnavailableError(
            "Overpass competitor search failed for all configured endpoints: "
            + "; ".join(failures),
            status_codes=status_codes,
        )

    elements = data.get("elements", [])
    competitors = []

    for element in elements:
        competitor = normalize_competitor(element)
        if competitor:
            competitors.append(competitor)

    remark = data.get("remark")
    status = "incomplete" if remark else ("found" if competitors else "completed_empty")
    message = str(remark) if remark else None
    return CompetitorSearchResult(competitors, status=status, message=message)


def get_supported_categories() -> List[Dict[str, Any]]:
    """Get list of supported business categories with their OSM mappings.

    Returns:
        List of category info dicts
    """
    categories = []
    for category, tags in CATEGORY_TO_OSM_TAG.items():
        categories.append(
            {
                "key": category,
                "name": category.replace("_", " ").title(),
                "osm_tags": tags,
            }
        )
    return categories
