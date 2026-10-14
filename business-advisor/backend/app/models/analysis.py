"""Analysis model."""

from __future__ import annotations

from sqlalchemy import Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Analysis(Base, TimestampMixin):
    """Analysis model for storing completed analysis results."""

    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    business_category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    available_margin_capital: Mapped[float] = mapped_column(Float, nullable=False)
    radius_km: Mapped[float] = mapped_column(Float, nullable=False)

    # Store results as JSON
    market_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    feasibility_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    financial_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Summary fields for easy querying
    feasibility_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    project_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    scheme_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
