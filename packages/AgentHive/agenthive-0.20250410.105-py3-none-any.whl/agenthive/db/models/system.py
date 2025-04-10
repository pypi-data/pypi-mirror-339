"""SQLAlchemy ORM models for system metrics."""
from typing import Dict, Any  # Added import for type hints
from sqlalchemy import Column, Integer, Float
from . import Base
import datetime

class SystemMetricsModel(Base):
    """Model representing system-wide metrics."""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float, nullable=False, index=True, default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp())
    active_workers = Column(Integer, default=0)
    idle_workers = Column(Integer, default=0)
    busy_workers = Column(Integer, default=0)
    pending_tasks = Column(Integer, default=0)
    assigned_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    waiting_tasks = Column(Integer, default=0)
    avg_cpu_usage = Column(Float, default=0.0)
    avg_memory_usage = Column(Float, default=0.0)
    avg_disk_usage = Column(Float, default=0.0)
    task_throughput = Column(Float, default=0.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the metrics to a dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "active_workers": self.active_workers,
            "idle_workers": self.idle_workers,
            "busy_workers": self.busy_workers,
            "pending_tasks": self.pending_tasks,
            "assigned_tasks": self.assigned_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "waiting_tasks": self.waiting_tasks,
            "avg_cpu_usage": self.avg_cpu_usage,
            "avg_memory_usage": self.avg_memory_usage,
            "avg_disk_usage": self.avg_disk_usage,
            "task_throughput": self.task_throughput
        }

__all__ = ['SystemMetricsModel']
