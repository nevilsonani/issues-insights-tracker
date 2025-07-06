# app/models/stats.py

from sqlalchemy import Column, Integer, Date, Enum
from app.db.base import Base
from app.models.issue import Status
from datetime import date

class DailyStats(Base):
    __tablename__ = "daily_stats"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=date.today, index=True)
    status = Column(Enum(Status), nullable=False, index=True)
    count = Column(Integer, default=0)
