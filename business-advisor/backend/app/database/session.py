"""Database session management."""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.base import Base

# Get database URL from environment variable
# For MVP, we'll make it optional and create tables if database is configured
DATABASE_URL = os.getenv("DATABASE_URL", "")

engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database tables."""
    if engine:
        Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency for FastAPI."""
    if not SessionLocal:
        raise RuntimeError("Database not configured. Set DATABASE_URL environment variable.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
