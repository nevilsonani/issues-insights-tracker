from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.models.issue import Severity, Status, Priority


class IssueBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: Optional[Severity] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Severity] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None


class IssueOut(IssueBase):
    id: int
    reporter_id: int
    created_at: datetime
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True  # ✅ Use this instead of orm_mode in Pydantic v2
    
    @classmethod
    def from_orm(cls, obj):
        """Custom from_orm to ensure priority has a default value."""
        data = cls.__dict__.copy()
        # Ensure priority is never None
        if hasattr(obj, 'priority') and obj.priority is None:
            obj.priority = 'MINOR'
        if hasattr(obj, 'tags') and isinstance(obj.tags, str):
            data.tags = obj.tags.split(',') if obj.tags else []
        return super().from_orm(obj)