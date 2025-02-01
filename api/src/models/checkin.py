from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel


class Checkin(BaseModel):
    __tablename__ = "checkins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user: Mapped[str] = mapped_column(String, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    hours: Mapped[float] = mapped_column(Float)
    project: Mapped[str] = mapped_column(String, index=True)


# TODO INCREMENT BY UUID
