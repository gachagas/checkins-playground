from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class Checkin(BaseModel):
    user: str
    timestamp: datetime
    hours: float
    project: str


class CheckinAggregate(BaseModel):
    total_hours: float
    project: str
    project_count: int = Field(description="Number of unique projects")


class CheckinDaily(BaseModel):
    date: datetime
    project_count: int = Field(description="Number of unique projects per day")
    total_hours: float


class UserCheckinSummary(BaseModel):
    total_hours: float
    projects: list[str]
    project_count: int
    user: str


class CheckinPage(BaseModel):
    items: list[Checkin]
    total: int
    page: int
    size: int
    pages: int
