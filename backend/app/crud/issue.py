from sqlalchemy.orm import Session
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate
from datetime import datetime


def create_issue(db: Session, issue: IssueCreate, reporter_id: int) -> Issue:
    tags_str = None
    if issue.tags:
        tags_str = ','.join(issue.tags)
    db_issue = Issue(**issue.dict(exclude_unset=True, exclude={"tags"}), tags=tags_str, reporter_id=reporter_id, created_at=datetime.utcnow())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issue(db: Session, issue_id: int) -> Issue | None:
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if issue and issue.tags:
        issue.tags = issue.tags.split(',')
    elif issue:
        issue.tags = []
    return issue


def get_issues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Issue).offset(skip).limit(limit).all()


get_all_issues = get_issues


def get_issues_by_user(db: Session, user_id: int):
    return db.query(Issue).filter(Issue.reporter_id == user_id).all()


def update_issue(db: Session, db_issue: Issue, updates: IssueUpdate) -> Issue:
    update_data = updates.dict(exclude_unset=True)
    tags = update_data.pop("tags", None)
    for key, value in update_data.items():
        setattr(db_issue, key, value)
    if tags is not None:
        db_issue.tags = ','.join(tags)
    db.commit()
    db.refresh(db_issue)
    if db_issue.tags:
        db_issue.tags = db_issue.tags.split(',')
    else:
        db_issue.tags = []
    return db_issue


def delete_issue(db: Session, issue_id: int) -> bool:
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if issue:
        db.delete(issue)
        db.commit()
        return True
    return False
