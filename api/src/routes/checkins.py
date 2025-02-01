from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.checkin import (
    CheckinAggregate,
    CheckinDaily,
    CheckinPage,
    UserCheckinSummary,
)
from src.services import checkins as checkins_service

router = APIRouter(prefix="/checkins", tags=["checkins"])


@router.get("/", response_model=CheckinPage)
async def read_checkins(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=10, le=100),
    db: Session = Depends(get_db),
) -> CheckinPage:
    """Get a paginated list of all checkins."""
    return checkins_service.get_paginated_checkins(db, page, size)


@router.get("/user-summary", response_model=UserCheckinSummary)
async def get_user_summary(
    user: str = Query(..., description="Username to get summary for"),
    db: Session = Depends(get_db),
) -> UserCheckinSummary:
    """Get a summary of a user's checkins."""
    return checkins_service.get_user_checkin_summary(db, user)


@router.get("/by-user", response_model=List[CheckinAggregate])
async def get_checkins_by_user(
    db: Session = Depends(get_db),
) -> List[CheckinAggregate]:
    """Get aggregated checkin data grouped by user."""
    return checkins_service.get_checkins_aggregated_by_user(db)


@router.get("/daily", response_model=List[CheckinDaily])
async def get_daily_checkins(
    db: Session = Depends(get_db),
) -> List[CheckinDaily]:
    """Get daily aggregated checkin data."""
    return checkins_service.get_daily_checkin_stats(db)


@router.get("/by-date", response_model=CheckinPage)
async def get_checkins_by_date(
    start_date: Optional[datetime] = Query(
        None, description="Start date (YYYY-MM-DD)"
    ),
    end_date: Optional[datetime] = Query(
        None, description="End date (YYYY-MM-DD)"
    ),
    user: Optional[str] = Query(None, description="Username to filter by"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=10, le=100),
    db: Session = Depends(get_db),
) -> CheckinPage:
    """Get paginated checkins filtered by date range and optionally by user."""
    return checkins_service.get_filtered_checkins(
        db, page, size, start_date, end_date, user
    )
