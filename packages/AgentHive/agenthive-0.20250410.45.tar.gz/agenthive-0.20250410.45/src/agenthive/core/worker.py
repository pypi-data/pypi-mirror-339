"""
Base Worker class for py-AgentHive.
"""
import os
import uuid
import time
import json
import logging
import asyncio
import socket
import psutil
import platform
from typing import Dict, Any, Optional, List, Union
from abc import ABC, abstractmethod

from agenthive.core.task import Task
from agenthive.core.heartbeat.constants import HeartbeatStrategy

logger = logging.getLogger(__name__)

class Worker(ABC):
    """
    Abstract base class for all workers in the py-AgentHive framework.

    Workers process tasks based on their task_type. By default, they accept all task types
    (task_type='*') unless explicitly configured otherwise.

    Attributes:
        worker_id (str): Unique identifier for the worker
        coordinator_url (str): URL of the coordinator
        status (str): Current status of the worker
        task_types (Set[str]): Set of task types this worker handles ('*' by default)
        stats (Dict[str, Any]): Worker performance statistics
        resource_usage (Dict[str, Any]): System resource usage metrics
    """
    TASK_TYPES = []

    def __init__(
        self,
        coordinator_url: str,
        worker_id: Optional[str] = None,
        heartbeat_interval: int = 10,
        resource_check_interval: int = 30,
        tags: Optional[List[str]] = None,
        redis_url: Optional[str] = None,
        heartbeat_strategy: Union[str, HeartbeatStrategy] = HeartbeatStrategy.STDOUT
    ):
        """
        Initialize a new Worker.

        Args:
            coordinator_url: URL of the coordinator service
            worker_id: Unique identifier (auto-generated if None)
            heartbeat_interval: Seconds between heartbeat messages
            resource_check_interval: Seconds between resource checks
            tags: Categorization tags
            redis_url: Redis connection URL
            heartbeat_strategy: Strategy for heartbeat reporting
        """
        self.worker_id = worker_id or f"{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:8]}"
        self.coordinator_url = coordinator_url
        self.redis_url = redis_url or "redis://localhost:6379"
        self.heartbeat_strategy = (
            HeartbeatStrategy.from_string(heartbeat_strategy)
            if isinstance(heartbeat_strategy, str)
            else heartbeat_strategy
        )
        self.heartbeat_strategy = HeartbeatStrategy.REDIS

        self.status = "idle"
        self.task_types = set(self.__class__.TASK_TYPES)
        self.available_work_types = list(self.task_types)
        self.heartbeat_interval = heartbeat_interval
        self.resource_check_interval = resource_check_interval
        self.tags = tags or []

        # System info
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname) if self.hostname else "127.0.0.1"
        self.platform = platform.system()
        self.architecture = platform.machine()
        self.python_version = platform.python_version()

        # Stats
        self.stats = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "tasks_succeeded": 0,
            "processing_time": 0.0,
            "last_task_id": None,
            "start_time": time.time(),
            "total_cpu_time": 0.0,
            "peak_memory_usage": 0.0,
        }

        # Resource usage
        self.resource_usage = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "disk_usage_percent": 0.0,
            "load_average": [0.0, 0.0, 0.0],
            "network_io": {"bytes_sent": 0, "bytes_recv": 0},
            "process_count": 0,
            "thread_count": 0,
        }

        # Runtime attributes
        self._running = False
        self._current_task = None
        self._heartbeat_sender = None
        self._resource_monitor_task = None
        self._process = psutil.Process()
        self._completed_tasks = set()
        self._redis = None

    @abstractmethod
    async def setup(self) -> None:
        """Set up the worker before processing tasks."""
        pass

    @abstractmethod
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process a task based on its JSON data.

        Args:
            task: Task to process

        Returns:
            Dict[str, Any]: Processing result
        """
        pass
