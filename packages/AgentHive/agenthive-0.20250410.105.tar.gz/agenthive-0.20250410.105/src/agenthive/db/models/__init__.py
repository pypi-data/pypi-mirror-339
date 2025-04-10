"""Database models for AgentHive."""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .heartbeat import WorkerEventModel, WorkerHeartbeatModel
from .worker import WorkerModel
from .task import TaskModel
from .system import SystemMetricsModel

__all__ = ['Base', 'WorkerEventModel', 'WorkerHeartbeatModel', 'WorkerModel', 'TaskModel', 'SystemMetricsModel']