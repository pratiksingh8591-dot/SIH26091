"""Scheme-related routes."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from app.data.schemes import SCHEME_DATA
from app.models.schemas import SchemeMatchingRequest
from app.services.scheme_matching import match_schemes

router = APIRouter(prefix="/api", tags=["schemes"])


@router.get("/schemes")
def list_schemes() -> List[Dict[str, Any]]:
    return SCHEME_DATA


@router.post("/schemes/match")
def match_schemes_route(request: SchemeMatchingRequest) -> List[Dict[str, Any]]:
    user_profile = request.model_dump()
    return match_schemes(user_profile)
