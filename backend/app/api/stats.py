from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.schemas.stats import DailyStat
from app.crud.stats import get_today_stats
from app.models.issue import Severity, Issue
from datetime import date, datetime, timedelta
import logging
from sqlalchemy import func

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[DailyStat])
def read_stats(db: Session = Depends(get_db)):
    try:
        return get_today_stats(db) or []
    except Exception as e:
        logger.error(f"Error in /api/stats/: {e}")
        return []

@router.get("/daily", response_model=List[DailyStat])
def read_stats_daily(db: Session = Depends(get_db)):
    try:
        return get_today_stats(db) or []
    except Exception as e:
        logger.error(f"Error in /api/stats/daily: {e}")
        return []

@router.get("/severity")
def read_severity_stats(db: Session = Depends(get_db)):
    try:
        results = db.query(Issue.severity, func.count(Issue.id)).filter(func.date(Issue.created_at) == date.today()).group_by(Issue.severity).all()
        return {str(severity): count for severity, count in results}
    except Exception as e:
        logger.error(f"Error in /api/stats/severity: {e}")
        return {}

@router.get("/analytics")
def read_analytics(db: Session = Depends(get_db)):
    try:
        # Get all issues
        all_issues = db.query(Issue).all()
        
        # Calculate counts
        total_issues = len(all_issues)
        open_issues = len([i for i in all_issues if i.status == 'OPEN'])
        in_progress_issues = len([i for i in all_issues if i.status == 'IN_PROGRESS'])
        completed_issues = len([i for i in all_issues if i.status == 'DONE'])
        
        # Priority counts
        high_priority_issues = len([i for i in all_issues if i.priority == 'CRITICAL' or i.priority == 'BLOCKER'])
        medium_priority_issues = len([i for i in all_issues if i.priority == 'MINOR'])
        low_priority_issues = len([i for i in all_issues if i.priority == 'TRIVIAL'])
        
        # Recent issues (last 5)
        recent_issues = db.query(Issue).order_by(Issue.created_at.desc()).limit(5).all()
        
        # Issues by status
        status_counts = {}
        for status in ['OPEN', 'TRIAGED', 'IN_PROGRESS', 'DONE']:
            status_counts[status] = len([i for i in all_issues if i.status == status])
        
        # Issues by severity
        severity_counts = {}
        for severity in ['LOW', 'MEDIUM', 'HIGH']:
            severity_counts[severity] = len([i for i in all_issues if i.severity == severity])
        
        return {
            "total_issues": total_issues,
            "open_issues": open_issues,
            "in_progress_issues": in_progress_issues,
            "completed_issues": completed_issues,
            "high_priority_issues": high_priority_issues,
            "medium_priority_issues": medium_priority_issues,
            "low_priority_issues": low_priority_issues,
            "recent_issues": recent_issues,
            "issues_by_status": status_counts,
            "issues_by_severity": severity_counts
        }
    except Exception as e:
        logger.error(f"Error in /api/stats/analytics: {e}")
        return {
            "total_issues": 0,
            "open_issues": 0,
            "in_progress_issues": 0,
            "completed_issues": 0,
            "high_priority_issues": 0,
            "medium_priority_issues": 0,
            "low_priority_issues": 0,
            "recent_issues": [],
            "issues_by_status": {},
            "issues_by_severity": {}
        }
