"""
Basic Worker implementation for py-AgentHive.
"""
import logging
import datetime
import time
import asyncio
from typing import Dict, Any

from agenthive.core.worker import Worker
from agenthive.core.task import Task

logger = logging.getLogger(__name__)

class TimeReportWorker(Worker):
    """
    A basic worker that processes tasks based on their JSON data.
    """
    TASK_TYPES = ['time_report']  # Accept all task types by default

    async def setup(self) -> None:
        """Set up the worker."""
        pass

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process a task based on its JSON data.

        Args:
            task: Task to process

        Returns:
            Dict[str, Any]: Processing result
        """
        logger.debug(f"Processing task {task.task_id} of type {task.task_type}")
        
        # Example processing: Echo back the task data with worker info
        result = {
            "worker_id": self.worker_id,
            "task_id": task.task_id,
            "task_type": task.task_type,
            "message": f"Processed by {__class__.__name__} ({__name__}), {self.worker_id} with task type {task.task_type} at {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
            "input_data": task.data,
            "started_at": time.time(),
            "completed_at": None,
            "duration": 0,
            "output_data": {"status": False, "error": None, "data": None},
        }
        try:
            await asyncio.sleep(10)
            result["output_data"]["status"] = True
            result["output_data"]["data"] = time.time()
            result["completed_at"] = time.time()
            result["duration"] = result["completed_at"] - result["started_at"]
        except Exception as e:
            result["output_data"]["error"] = str(e)
            logger.error(f"Error processing task {task.task_id} of type {task.task_type} at TimeReportWorker: {e}")

        return result
