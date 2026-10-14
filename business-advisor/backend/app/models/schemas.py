"""Pydantic schemas for API validation."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class EntrepreneurProfile(BaseModel):
    age: int = Field(..., ge=18, le=100)
    gender: str = Field(..., min_length=1)
    social_category: str = Field(..., min_length=1)
    annual_family_income: float = Field(..., ge=0)
    education: str = Field(..., min_length=1)
    experience: int = Field(..., ge=0, le=60)
    state: str = Field(..., min_length=1)
    district: str = Field(..., min_length=1)
    city_or_village: str = Field(..., min_length=1)
    pincode: str = Field(..., min_length=4, max_length=10)
    available_capital: float = Field(..., ge=0)
    desired_loan_amount: float = Field(..., ge=0)
    monthly_household_expenses: float = Field(..., ge=0)
    business_category: str = Field(..., min_length=1)
    preferred_business: str = Field(..., min_length=1)
    expected_monthly_income: float = Field(..., ge=0)
    risk_preference: str = Field(..., min_length=1)

    @field_validator("gender", "social_category", "education", "state", "district", "city_or_village")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value: str) -> str:
        return value.strip()


class BusinessRecommendationRequest(BaseModel):
    available_capital: float = Field(..., ge=0)
    business_category: Optional[str] = None
    preferred_business: Optional[str] = None
    experience: int = Field(default=0, ge=0, le=60)
    desired_loan_amount: float = Field(default=0, ge=0)
    monthly_household_expenses: float = Field(default=0, ge=0)


class FeasibilityRequest(BaseModel):
    available_capital: float = Field(..., ge=0)
    desired_loan_amount: float = Field(..., ge=0)
    monthly_household_expenses: float = Field(..., ge=0)
    expected_monthly_income: float = Field(..., ge=0)
    business_category: str = Field(..., min_length=1)
    preferred_business: str = Field(..., min_length=1)
    experience: int = Field(..., ge=0, le=60)


class SchemeMatchingRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    annual_family_income: float = Field(..., ge=0)
    social_category: str = Field(..., min_length=1)
    gender: str = Field(..., min_length=1)
    business_category: str = Field(..., min_length=1)
    desired_loan_amount: float = Field(..., ge=0)


class HealthResponse(BaseModel):
    status: str
    message: str


# ============================================================================
# NEW SCHEMAS FOR LOCATION-BASED ANALYSIS
# ============================================================================


class LocationInput(BaseModel):
    """Location input for analysis."""

    name: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BusinessInput(BaseModel):
    """Business type input for analysis."""

    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)


class AnalyzeRequest(BaseModel):
    """Main request schema for location-based business analysis."""

    location: LocationInput
    business: BusinessInput
    available_margin_capital: float = Field(..., gt=0, description="Available margin capital in rupees")
    radius_km: float = Field(default=10, ge=1, le=50, description="Analysis radius in kilometers")


class CompetitorData(BaseModel):
    """Competitor information."""

    name: Optional[str] = None
    latitude: float
    longitude: float
    category: str
    distance_km: float
    source: str = "OpenStreetMap"
    osm_id: Optional[str] = None


class MarketData(BaseModel):
    """Market analysis data."""

    population: Optional[int] = None
    population_source: Optional[str] = None
    population_note: Optional[str] = None
    competitors: List[CompetitorData]
    competitor_count: int
    competitor_density: float
    average_distance: Optional[float] = None
    nearest_distance: Optional[float] = None
    competitor_search_status: str = "unknown"
    competitor_search_message: Optional[str] = None


class FeasibilityData(BaseModel):
    """Feasibility analysis scores."""

    feasibility_score: float
    demand_score: Optional[float] = None
    competition_score: Optional[float] = None
    purchasing_power_score: Optional[float] = None
    market_access_score: Optional[float] = None
    supply_score: Optional[float] = None
    risk_score: Optional[float] = None
    capital_fit_score: Optional[float] = None
    confidence: float
    limitations: List[str]


class RepaymentScheduleItem(BaseModel):
    """Single month in repayment schedule."""

    month: int
    payment: float
    principal: float
    interest: float
    balance: float


class FinancialData(BaseModel):
    """Financial analysis data."""

    available_margin_capital: float
    project_cost: float
    maximum_loan: float
    scheme_name: str
    interest_rate: float
    tenure_years: int
    moratorium_months: int
    emi: float
    repayment_schedule: List[RepaymentScheduleItem]


class AnalyzeResponse(BaseModel):
    """Complete analysis response."""

    input: AnalyzeRequest
    market: MarketData
    feasibility: FeasibilityData
    financial: FinancialData
    data_sources: List[str]
    limitations: List[str]
    analytics: Optional[Dict[str, Any]] = None


class FinanceCalculateRequest(BaseModel):
    """Request for financial calculation only."""

    available_margin_capital: float = Field(..., gt=0)


class MarketCompetitorsRequest(BaseModel):
    """Request for competitor data."""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    business_category: str = Field(..., min_length=1)
    radius_km: float = Field(default=10, ge=1, le=50)


class MarketPopulationRequest(BaseModel):
    """Request for population data."""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=10, ge=1, le=50)


class BusinessCategoryInfo(BaseModel):
    """Business category information."""

    key: str
    name: str
    osm_tags: List[str]
