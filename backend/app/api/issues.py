from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil

from app.schemas.issue import IssueCreate, IssueOut, IssueUpdate
from app.crud.issue import (
    create_issue,
    get_issues_by_user,
    get_all_issues,
    update_issue,
    get_issue,
    delete_issue
)
from app.api.deps import get_db, get_current_user
from app.models.user import User, Role

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=IssueOut)
def create(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    priority: Optional[str] = Form(None),
    severity: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    file_path = None
    if file:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = file_location

    issue_data = IssueCreate(
        title=title,
        description=description,
        priority=priority,
        severity=severity,
        file_path=file_path
    )

    return create_issue(db, issue_data, reporter_id=user.id)


@router.get("/", response_model=List[IssueOut])
def list_issues(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role == Role.REPORTER:
        return get_issues_by_user(db, user.id)
    return get_all_issues(db)


@router.patch("/{issue_id}", response_model=IssueOut)
def update_status(
    issue_id: int,
    update: IssueUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Strict status workflow enforcement
    allowed_transitions = {
        "OPEN": ["TRIAGED"],
        "TRIAGED": ["IN_PROGRESS"],
        "IN_PROGRESS": ["DONE"],
        "DONE": []
    }
    if update.status and update.status != issue.status:
        current = str(issue.status)
        target = str(update.status)
        if target not in allowed_transitions.get(current, []):
            raise HTTPException(status_code=400, detail=f"Invalid status transition: {current} → {target}")

    if user.role in [Role.MAINTAINER, Role.ADMIN] or issue.reporter_id == user.id:
        return update_issue(db, issue, update)

    raise HTTPException(status_code=403, detail="Not authorized")


@router.get("/{issue_id}", response_model=IssueOut)
def get_single_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    # Only allow access if user is admin/maintainer or reporter of the issue
    if user.role in [Role.MAINTAINER, Role.ADMIN] or issue.reporter_id == user.id:
        return issue
    raise HTTPException(status_code=403, detail="Not authorized")


@router.delete("/{issue_id}", status_code=204)
def delete_issue_endpoint(
    issue_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    deleted = delete_issue(db, issue_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Issue not found")
    return None


@router.patch("/{issue_id}/triage", response_model=IssueOut)
def triage_issue(
    issue_id: int,
    update: IssueUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role not in [Role.MAINTAINER, Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Maintainer or Admin access required")
    
    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Strict status workflow enforcement
    allowed_transitions = {
        "OPEN": ["TRIAGED"],
        "TRIAGED": ["IN_PROGRESS"],
        "IN_PROGRESS": ["DONE"],
        "DONE": []
    }
    if update.status and update.status != issue.status:
        current = str(issue.status)
        target = str(update.status)
        if target not in allowed_transitions.get(current, []):
            raise HTTPException(status_code=400, detail=f"Invalid status transition: {current} → {target}")
    
    return update_issue(db, issue, update)
