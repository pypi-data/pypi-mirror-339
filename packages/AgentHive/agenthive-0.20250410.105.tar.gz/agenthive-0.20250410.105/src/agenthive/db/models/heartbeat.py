"""SQLAlchemy ORM models for heartbeat system."""
import json
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from . import Base
from ...core.heartbeat.models import HeartbeatData

class WorkerEventModel(Base):
    """Worker event table ORM model."""
    __tablename__ = "worker_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    event = Column(String, nullable=True, default="")
    data = Column(JSON, nullable=True, default={})
    # 修改列名，避免與SQLAlchemy保留字衝突
    extra_data = Column(JSON, nullable=True, default={})

class WorkerHeartbeatModel(Base):
    """Model representing a worker heartbeat."""
    __tablename__ = "worker_heartbeats"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    worker_id = Column(String, ForeignKey("workers.worker_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, nullable=False)
    cpu_percent = Column(Float, nullable=True)
    memory_percent = Column(Float, nullable=True)
    disk_percent = Column(Float, nullable=True)
    current_task_id = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True, default={})

    worker = relationship("WorkerModel", back_populates="heartbeats")

    @classmethod
    def from_heartbeat_data_object_to_dict(cls, data: HeartbeatData) -> Dict[str, Any]:
        """
        Create a WorkerHeartbeat object from a HeartbeatData object.
        
        Args:
            data: HeartbeatData object
            
        Returns:
            WorkerHeartbeat: New WorkerHeartbeat object
        """
        return {
            "timestamp": data.timestamp,
            "worker_id": data.worker_id,
            "status": data.status,
            "current_task_id": data.current_task,
            "cpu_percent": data.resource_usage.get("cpu_percent", 0.0) if data.resource_usage else 0.0,
            "memory_percent": data.resource_usage.get("memory_percent", 0.0) if data.resource_usage else 0.0,
            "disk_percent": data.resource_usage.get("disk_percent", 0.0) if data.resource_usage else 0.0,
            "extra_data": data.stats, #json.dumps(data.stats),
        }

__all__ = ['WorkerEventModel', 'WorkerHeartbeatModel']
