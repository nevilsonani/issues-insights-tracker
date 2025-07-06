# app/schemas/stats.py

from datetime import date
from pydantic import BaseModel

class DailyStat(BaseModel):
    date: date
    status: str
    count: int

    class Config:
        from_attributes = True  # Required for SQLAlchemy model conversion in Pydantic v2
