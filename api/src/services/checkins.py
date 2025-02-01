import math
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.checkin import Checkin as CheckinModel
from src.schemas.checkin import (
    CheckinAggregate,
    CheckinDaily,
    CheckinPage,
    UserCheckinSummary,
)


def get_paginated_checkins(db: Session, page: int, size: int) -> CheckinPage:
    """Get a paginated list of all checkins."""
    offset = (page - 1) * size
    total = db.query(CheckinModel).count()
    items = (
        db.query(CheckinModel)
        .order_by(CheckinModel.timestamp.desc())
        .offset(offset)
        .limit(size)
        .all()
    )
    pages = math.ceil(total / size)
    return CheckinPage(
        items=items, total=total, page=page, size=size, pages=pages
    )


def get_user_checkin_summary(db: Session, user: str) -> UserCheckinSummary:
    """Get a summary of a user's checkins."""
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


def get_checkins_aggregated_by_user(
    db: Session,
) -> List[CheckinAggregate]:
    """Get aggregated checkin data grouped by user."""
    return (
        db.query(
            func.sum(CheckinModel.hours).label("total_hours"),
            CheckinModel.user.label("project"),
            func.count(func.distinct(CheckinModel.project)).label(
                "project_count"
            ),
        )
        .group_by(CheckinModel.user)
        .all()
    )


def get_daily_checkin_stats(db: Session) -> List[CheckinDaily]:
    """Get daily aggregated checkin data."""
    return (
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


def get_filtered_checkins(
    db: Session,
    page: int,
    size: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    user: Optional[str] = None,
) -> CheckinPage:
    """Get paginated checkins filtered by date range and user."""
    query = db.query(CheckinModel)

    if start_date:
        query = query.filter(
            func.date(CheckinModel.timestamp) >= start_date.date()
        )
    if end_date:
        query = query.filter(
            func.date(CheckinModel.timestamp) <= end_date.date()
        )
    if user:
        query = query.filter(CheckinModel.user == user)

    total = query.count()
    offset = (page - 1) * size
    items = (
        query.order_by(CheckinModel.timestamp.desc())
        .offset(offset)
        .limit(size)
        .all()
    )
    pages = math.ceil(total / size)

    return CheckinPage(
        items=items, total=total, page=page, size=size, pages=pages
    )
