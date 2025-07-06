# app/crud/stats.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.stats import DailyStats
from app.models.issue import Issue
from app.schemas.stats import DailyStat  # Optional if used for response schema

def record_daily_stats(db: Session):
    """
    Deletes today's existing stats (if any) and records fresh counts of issues by status.
    """
    # Remove existing stats for today
    db.query(DailyStats).filter(DailyStats.date == date.today()).delete()
    db.commit()

    # Count issues grouped by status
    results = (
        db.query(Issue.status, func.count(Issue.id))
        .filter(func.date(Issue.created_at) == date.today())  # Optional: limit to today
        .group_by(Issue.status)
        .all()
    )

    # Store stats in DailyStats table
    for status, count in results:
        stat = DailyStats(date=date.today(), status=status, count=count)
        db.add(stat)

    db.commit()


def get_today_stats(db: Session):
    """
    Returns list of DailyStats entries for today.
    """
    return db.query(DailyStats).filter(DailyStats.date == date.today()).all()
