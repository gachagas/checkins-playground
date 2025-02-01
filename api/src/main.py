from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.checkin import Checkin as CheckinModel
from src.schemas.checkin import Checkin, CheckinAggregate, CheckinDaily

from .database import get_db

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/checkins/", response_model=List[Checkin])
def read_checkins(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    checkins = db.query(CheckinModel).offset(skip).limit(limit).all()
    return checkins


@app.get("/checkins/by-user", response_model=List[CheckinAggregate])
def get_checkins_by_user(db: Session = Depends(get_db)):
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
