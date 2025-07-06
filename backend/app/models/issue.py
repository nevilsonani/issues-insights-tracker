from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum


class Severity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Status(str, enum.Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Priority(str, enum.Enum):
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    MINOR = "MINOR"
    TRIVIAL = "TRIVIAL"


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_path = Column(String, nullable=True)
    severity = Column(Enum(Severity), default=Severity.LOW)
    status = Column(Enum(Status), default=Status.OPEN)
    priority = Column(Enum(Priority), nullable=False, default=Priority.MINOR)  # ✅ Required priority with default

    reporter_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    tags = Column(String, nullable=True)  # Comma-separated tags

    reporter = relationship("User")
    