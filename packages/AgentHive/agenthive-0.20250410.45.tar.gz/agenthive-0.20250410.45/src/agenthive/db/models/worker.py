"""SQLAlchemy ORM models for workers."""
from typing import Dict, Any  # Added import for type hints
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from . import Base

class WorkerModel(Base):
    """Worker table ORM model."""
    __tablename__ = "workers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(String, nullable=False, unique=True, index=True)
    last_seen = Column(DateTime(timezone=True), index=True)
    registered_at = Column(DateTime(timezone=True), nullable=True, default=None)
    capabilities = Column(JSON, nullable=False, default={})
    configured_capabilities = Column(JSON, nullable=True, default={})
    available_capabilities = Column(JSON, nullable=True, default={})
    tags = Column(JSON, nullable=True, default={})
    hostname = Column(String, nullable=True, default=None)
    ip_address = Column(String, nullable=True, default=None)
    status = Column(String, nullable=False, default="unknown")
    version = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True, default={})  

    heartbeats = relationship("WorkerHeartbeatModel", back_populates="worker", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the worker to a dictionary."""
        return {
            "id": self.id,
            "worker_id": self.worker_id,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "capabilities": self.capabilities,
            "status": self.status,
            "version": self.version,
            "extra_data": self.extra_data
        }

__all__ = ['WorkerModel']
