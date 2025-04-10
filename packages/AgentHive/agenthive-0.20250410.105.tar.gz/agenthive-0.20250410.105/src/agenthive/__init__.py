"""
AgentHive is a flexible, Python-based service framework for managing distributed task execution.
"""

from agenthive.version import __version__
from agenthive.core.task import Task
from agenthive.core.worker import Worker
from agenthive.core.coordinator import Coordinator

__all__ = ["__version__", "Task", "Worker", "Coordinator"]
