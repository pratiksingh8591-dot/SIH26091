"""Population model."""

from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class PopulationRecord(Base, TimestampMixin):
    """Population record model for storing population data by location."""

    __tablename__ = "population_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="Census 2011")
    year: Mapped[int] = mapped_column(Integer, nullable=False, default=2011)
    area_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # district, city, village
