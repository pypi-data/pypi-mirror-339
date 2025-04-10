"""SQLAlchemy ORM models for tasks."""
from typing import Dict, Any  # Added import for type hints
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.mutable import MutableDict
from . import Base
import datetime

class TaskModel(Base):
    """Model representing a task in the system."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String(100), unique=True, nullable=False, index=True)
    task_type = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="pending", index=True)
    priority = Column(Integer, default=0, index=True)
    data = Column(JSON, nullable=False, default=dict)
    result = Column(JSON, nullable=True)
    error = Column(JSON, nullable=True)
    extra_data = Column(JSON, nullable=True)
    assigned_to = Column(String(100), nullable=True)
    attempts = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime(timezone=True), index=True, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True, default=lambda: datetime.datetime.now(datetime.timezone.utc), 
                      onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the task to a dictionary."""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "status": self.status,
            "priority": self.priority,
            "data": self.data,
            "result": self.result,
            "error": self.error,
            "extra_data": self.extra_data,
            "assigned_to": self.assigned_to,
            "attempts": self.attempts,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "updated_at": self.updated_at
        }

__all__ = ['TaskModel']
