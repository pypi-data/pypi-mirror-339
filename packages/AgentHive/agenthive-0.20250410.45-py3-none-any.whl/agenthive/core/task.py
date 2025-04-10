"""
Task class for py-AgentHive.
"""
import logging
import json
import time
from typing import Dict, Any, Optional, List
import datetime

logger = logging.getLogger(__name__)

class Task:
    """
    A simplified Task class that encapsulates task details in a JSON-serializable format.

    Attributes:
        task_id (str): Unique identifier for the task
        task_type (str): Type of the task (default: 'generic')
        data (Dict[str, Any]): JSON-serializable dictionary containing task details
        status (str): Current status of the task
        created_at (float): Timestamp of task creation
        started_at (Optional[float]): Timestamp when task started
        completed_at (Optional[float]): Timestamp when task completed
        result (Optional[Dict[str, Any]]): Task result
        error (Optional[str]): Error message if task failed
    """
    def __init__(
        self,
        task_id: Optional[str] = None,
        task_type: str = "generic",
        data: Optional[Dict[str, Any]] = None,
        priority: int = 0,
        max_retries: int = 3,
        timeout: Optional[int] = None,
        dependencies: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a Task with JSON-serializable data.

        Args:
            task_id: Unique identifier (auto-generated if None)
            task_type: Type of task (default: 'generic')
            data: Task details as a dictionary (parameters, intermediate state, etc.)
            priority: Task priority
            max_retries: Maximum retry attempts
            timeout: Execution timeout in seconds
            dependencies: List of task IDs this task depends on
            tags: Categorization tags
            metadata: Additional metadata
        """
        self.task_id = task_id or f"task-{int(time.time()*1000)}-{id(self)}"
        self.task_type = task_type
        self.data = data or {}
        self.priority = priority
        self.max_retries = max_retries
        self.timeout = timeout
        self.dependencies = dependencies or []
        self.tags = tags or []
        self.metadata = metadata or {}

        # Task state
        self.status = "pending"
        self.created_at = datetime.datetime.now(datetime.timezone.utc)
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None

        self.raw_data = None

    def mark_as_started(self) -> None:
        """Mark the task as started."""
        self.status = "running"
        self.started_at = datetime.datetime.now(datetime.timezone.utc)

    def mark_as_completed(self, result: Dict[str, Any]) -> None:
        """Mark the task as completed with a result."""
        self.status = "completed"
        self.completed_at = datetime.datetime.now(datetime.timezone.utc)
        self.result = result

    def mark_as_failed(self, error: str) -> None:
        """Mark the task as failed with an error message."""
        self.status = "failed"
        self.completed_at = datetime.datetime.now(datetime.timezone.utc)
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert the task to a JSON-serializable dictionary."""
        data = {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "data": self.data,
            "priority": self.priority,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "metadata": self.metadata,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }

        for key in list(data.keys()):
            if isinstance(data[key], (dict, list)) or data[key] is None:
                data[key] = json.dumps(data[key])
        return data;

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary."""

        for (key, value) in data.items():
            if isinstance(value, str):
                if value == "null":
                    data[key] = None
                    continue

                if (value.startswith("{") and value.endswith("}")) or (value.startswith("[") and value.endswith("]")):
                    try:
                        new_value = json.loads(value)
                        data[key] = new_value
                    except Exception as e:
                        logging.warning(f"Error parsing task data at from_dict: {value}, exception: {e}")

        task = cls(
            task_id=data.get("task_id"),
            task_type=data.get("task_type", "generic"),
            data=data.get("data", {}),
            priority=data.get("priority", 0),
            max_retries=data.get("max_retries", 3),
            timeout=data.get("timeout"),
            dependencies=data.get("dependencies"),
            tags=data.get("tags"),
            metadata=data.get("metadata")
        )
        task.raw_data = data
        task.status = data.get("status", "pending")

        created_at = data.get("created_at")
        if created_at:
            if isinstance(created_at, (int, float)):
                task.created_at = datetime.datetime.fromtimestamp(created_at)
            elif isinstance(created_at, str):
                task.created_at = datetime.datetime.fromisoformat(created_at)
            else:
                task.created_at = datetime.datetime.now(datetime.timezone.utc)
        
        started_at = data.get("started_at")
        if started_at:
            if isinstance(started_at, (int, float)):
                task.started_at = datetime.datetime.fromtimestamp(started_at)
            elif isinstance(started_at, str):
                task.started_at = datetime.datetime.fromisoformat(started_at)
        
        completed_at = data.get("completed_at")
        if completed_at:
            if isinstance(completed_at, (int, float)):
                task.completed_at = datetime.datetime.fromtimestamp(completed_at)
            elif isinstance(completed_at, str):
                task.completed_at = datetime.datetime.fromisoformat(completed_at)

        task.result = data.get("result")
        task.error = data.get("error")
        return task

    def __str__(self) -> str:
        """String representation of the task."""
        return json.dumps(self.to_dict(), indent=2)
