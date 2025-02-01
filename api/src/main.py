import math
from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.checkin import Checkin as CheckinModel
from src.schemas.checkin import (
    CheckinAggregate,
    CheckinDaily,
    CheckinPage,
    UserCheckinSummary,
)

from .database import get_db

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message."""
    return {"Hello": "World"}


@app.get("/checkins/", response_model=CheckinPage)
def read_checkins(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=10, le=100),
    db: Session = Depends(get_db),
):
    """
    Get a paginated list of all checkins.

    Parameters:
        page (int): Page number (starts at 1)
        size (int): Number of items per page (10-100)

    Returns:
        CheckinPage: Paginated checkins with total count and page information
    """
    # Calculate offset
    offset = (page - 1) * size

    # Get total count
    total = db.query(CheckinModel).count()

    # Get items for current page
    items = (
        db.query(CheckinModel)
        .order_by(CheckinModel.timestamp.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    # Calculate total pages
    pages = math.ceil(total / size)

    return CheckinPage(
        items=items, total=total, page=page, size=size, pages=pages
    )


@app.get("/checkins/user-summary", response_model=UserCheckinSummary)
def get_user_summary(
    user: str = Query(..., description="Username to get summary for"),
    db: Session = Depends(get_db),
):
    """
    Get a summary of a user's checkins including total hours and projects.

    Parameters:
        user (str): Username to get summary for

    Returns:
        UserCheckinSummary: User's total hours, project list, and project count

    Raises:
        HTTPException: 404 if user not found
    """
    # Get user's data
    result = (
        db.query(
            func.sum(CheckinModel.hours).label("total_hours"),
            func.count(func.distinct(CheckinModel.project)).label(
                "project_count"
            ),
        )
        .filter(CheckinModel.user == user)
        .first()
    )

    if not result or result.total_hours is None:
        raise HTTPException(
            status_code=404, detail=f"No checkins found for user: {user}"
        )

    # Get list of unique projects
    projects = (
        db.query(CheckinModel.project)
        .filter(CheckinModel.user == user)
        .distinct()
        .all()
    )
    project_list = [p[0] for p in projects]

    return UserCheckinSummary(
        total_hours=result.total_hours,
        projects=project_list,
        project_count=result.project_count,
        user=user,
    )


@app.get("/checkins/by-user", response_model=List[CheckinAggregate])
def get_checkins_by_user(db: Session = Depends(get_db)):
    """
    Get aggregated checkin data grouped by user.

    Returns:
        List[CheckinAggregate]: List of user summaries with total hours and project counts
    """
    return (
        db.query(
            func.sum(CheckinModel.hours).label("total_hours"),
            CheckinModel.user.label(
                "project"
            ),  # Reusing project field for user
            func.count(func.distinct(CheckinModel.project)).label(
                "project_count"
            ),  # Count of unique projects
        )
        .group_by(CheckinModel.user)
        .all()
    )


@app.get("/checkins/daily", response_model=List[CheckinDaily])
def get_daily_checkins(db: Session = Depends(get_db)):
    """
    Get daily aggregated checkin data.

    Returns:
        List[CheckinDaily]: Daily summaries with total hours and unique user counts
    """
    db_res = (
        db.query(
            func.sum(CheckinModel.hours).label("total_hours"),
            func.date(CheckinModel.timestamp).label("date"),
            func.count(func.distinct(CheckinModel.user)).label(
                "project_count"
            ),
        )
        .group_by(func.date(CheckinModel.timestamp))
        .all()
    )

    return db_res


@app.get("/checkins/by-date", response_model=CheckinPage)
def get_checkins_by_date(
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
):
    """
    Get paginated checkins filtered by date range and optionally by user.

    Parameters:
        start_date (datetime, optional): Filter checkins from this date
        end_date (datetime, optional): Filter checkins until this date
        user (str, optional): Filter checkins for specific user
        page (int): Page number (starts at 1)
        size (int): Number of items per page (10-100)

    Returns:
        CheckinPage: Paginated checkins with total count and page information
    """
    query = db.query(CheckinModel)

    # Apply date filters if provided
    if start_date:
        query = query.filter(
            func.date(CheckinModel.timestamp) >= start_date.date()
        )
    if end_date:
        query = query.filter(
            func.date(CheckinModel.timestamp) <= end_date.date()
        )

    # Apply user filter if provided
    if user:
        query = query.filter(CheckinModel.user == user)

    # Get total count for pagination
    total = query.count()

    # Calculate offset
    offset = (page - 1) * size

    # Get items for current page
    items = (
        query.order_by(CheckinModel.timestamp.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    # Calculate total pages
    pages = math.ceil(total / size)

    return CheckinPage(
        items=items, total=total, page=page, size=size, pages=pages
    )
