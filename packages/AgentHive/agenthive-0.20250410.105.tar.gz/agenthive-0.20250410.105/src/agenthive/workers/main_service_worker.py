"""
Basic Worker implementation for py-AgentHive.
"""
import time
import random
import json
import logging
import httpx
from typing import Dict, Any, Optional, List, Union
import datetime

from agenthive.core.worker import Worker
from agenthive.core.task import Task
from agenthive.core.heartbeat.sender import HeartbeatSender
from agenthive.core.heartbeat.constants import HeartbeatStrategy
from agenthive.core.heartbeat.models import HeartbeatData
from agenthive.core.heartbeat.constants import HeartbeatStrategy
from agenthive.core.in_memory_task_manager import InMemoryTaskManager
from agenthive.core.heartbeat.constants import (
    TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT
)
import asyncio
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

class MainServiceWorker(Worker):
    """
    A Main Service Worker that processes tasks based on their JSON data with sub workers.
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
        heartbeat_strategy: Union[str, HeartbeatStrategy] = HeartbeatStrategy.REDIS,
        worker_classes=None, task_type_registry=None, available_work_types=None):
        super().__init__(
            coordinator_url=coordinator_url, worker_id=worker_id, heartbeat_interval=heartbeat_interval,
            resource_check_interval=resource_check_interval, tags=tags, redis_url=redis_url,
            heartbeat_strategy=heartbeat_strategy
        )
        self._in_memory_task_manager = InMemoryTaskManager(
            redis_url=redis_url
        )

        self.worker_classes = worker_classes or {}
        self.task_type_registry = task_type_registry or {}
        self.available_work_types = available_work_types or ( list(self.task_type_registry.keys()) if self.task_type_registry else [] )

    async def setup(self) -> None:
        """Set up the worker."""
        if not self._redis:
            self._redis = await aioredis.from_url(self.redis_url, decode_responses=True)
            logger.info(f"Worker {self.worker_id} connected to Redis at {self.redis_url}")
        logger.info(f"MainServiceWorker {self.worker_id} setting up...")
        logger.info(f"Task types: {self.task_types}")
        logger.info(f"Worker classes: {self.worker_classes}")
        logger.info(f"Task type registry: {self.task_type_registry}")
        logger.info(f"Available work types: {self.available_work_types}")

        self.task_types = set(self.available_work_types)
        # shuffle task types to avoid all workers processing the same task type
        random.shuffle(self.available_work_types)

        logger.info(f"MainServiceWorker {self.worker_id} set up with task types: {self.available_work_types}")

    async def close(self) -> None:
        """Clean up resources."""
        logger.info(f"MainServiceWorker {self.worker_id} closing...")
        if self._redis:
            await self._redis.close()
        if self._in_memory_task_manager:
            await self._in_memory_task_manager.close()
            self._in_memory_task_manager = None

    async def stop(self) -> None:
        """Stop the worker gracefully."""
        self._running = False
        if self._heartbeat_sender:
            await self._heartbeat_sender.stop()
        await self.close()

    async def _get_next_task(self) -> Task:
        #logger.info(f"Getting next task for worker: {self.available_work_types}'")
        if not self._in_memory_task_manager:
            logger.error("InMemoryTaskManager not initialized.")
            return None
        
        for task_type in self.available_work_types:
            task_ids = await self._in_memory_task_manager.pop_pending_tasks(
                task_type=task_type
            )
            if not task_ids:
                #logger.info(f"No pending tasks found for task type: {task_type}")
                continue

            for task_id in task_ids:
                task_info = await self._in_memory_task_manager.get_task_info(
                    task_id=task_id
                )
                logger.info(f"Task info from InMemoryTaskManager: {task_info}")
                if not task_info:
                    logger.warning(f"Task info not found for task ID: {task_id}")
                    continue

                return Task.from_dict(task_info)

        return None

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process a task based on its JSON data.

        Args:
            task: Task to process

        Returns:
            Dict[str, Any]: Processing result
        """
        #logger.info(f"Processing task {task.task_id} of type {task.task_type}")

        result = {
            "worker_id": self.worker_id,
            "task_id": task.task_id,
            "task_type": task.task_type,
            "started_at": time.time(),
            "completed_at": None,
            "duration": 0,
            "input_data": task.data,
            "output_data": {"status": False, "error": None, "data": None, "started_at": None, "completed_at": None, "duration": 0},
        }
        if task.task_type in self.task_types:
            #logger.warning(f"Processing task {task.task_id} of type {task.task_type} by MainServiceWorker {self.worker_id}")
            task.started_at = datetime.datetime.now(datetime.timezone.utc)
            try:
                worker_classes = self.task_type_registry[task.task_type]
                if worker_classes:
                    worker_class = worker_classes[0]
                    
                    worker_instance = worker_class(
                        coordinator_url=self.coordinator_url,
                        worker_id=f"{self.worker_id}-sub-{task.task_type}"
                    )

                    await self._in_memory_task_manager.set_task_status_to_running(
                        task_id=task.task_id,
                        worker_id=self.worker_id
                    )
                
                    sub_output = await worker_instance.process_task(task)
                    #logger.info(f"Sub worker {worker_class.__name__} processed task {task.task_id} of type {task.task_type} with result:\n\n {sub_output}\n\n")
                    if sub_output and 'output_data' in sub_output and 'status' in sub_output["output_data"] and 'completed_at' in sub_output and 'started_at' in sub_output:
                        result["output_data"] = sub_output["output_data"]
                        result["completed_at"] = time.time()
                        result["duration"] = result["completed_at"] - result["started_at"]
                        result["output_data"]["started_at"] = sub_output["started_at"]
                        result["output_data"]["completed_at"] = sub_output["completed_at"]
                        result["output_data"]["duration"] = result["output_data"]["completed_at"] - result["output_data"]["started_at"]
                    else:
                        result["output_data"]["error"] = f"respnsed data format error:\n {json.dumps(sub_output, indent=4)}"
                    logger.info(f"Sub worker {worker_class.__name__} processed task {task.task_id} with result: {result['output_data']}")
            except Exception as e:
                logger.error(f"Error processing task {task.task_id} of type {task.task_type}: {e}")
                result["output_data"]["error"] = f"Running Exception: {str(e)}"
        else:
            result["output_data"]["error"] = f"Task type {task.task_type} not supported by MainServiceWorker {self.worker_id}"

        return result

    async def run(self) -> None:
        """Start the worker and process tasks."""
        from ..service.worker.main import shutting_down

        self._running = True

        try:
            await self.setup()
            logger.info(f"Worker {self.worker_id} started with task_types: {self.task_types}")
        except Exception as e:
            logger.error(f"Failed to set up worker: {e}")
            self._running = False
            return

        self._heartbeat_sender = HeartbeatSender(
            worker_id=self.worker_id,
            heartbeat_interval=self.heartbeat_interval,
            redis_url=self.redis_url,
            coordinator_url=self.coordinator_url,
            strategy=self.heartbeat_strategy
        )

        #
        # related: agenthive.core.heartbeat.sender._prepare_data
        #
        def get_worker_stats() -> Dict[str, Any]:
            output = {
                "worker_id": self.worker_id,
                "task_types": list(self.task_types),
                "stats": self.stats.copy(),
                "resource_usage": self.resource_usage.copy(),
            }
            output["stats"]["uptime"] = time.time() - self.stats["start_time"]
            output["stats"]["hostname"] = self.hostname

            return output

        await self._heartbeat_sender.start(get_worker_stats)
        self._resource_monitor_task = asyncio.create_task(self._monitor_resources())

        logger.info(f"Worker {self.worker_id} running: {self._running}, shutting_down: {shutting_down}")

        while self._running and not shutting_down:
            try:
                #logger.info(f"Worker {self.worker_id} checking for {self.task_types} tasks...")
                task = await self._get_next_task()
                #logger.info(f"Worker {self.worker_id} got task: {task}")
                if not task:
                    self.status = "idle"
                    await asyncio.sleep(1)
                    continue

                self._current_task = task
                self.status = "busy"
                task.mark_as_started()

                start_time = time.time()
                start_cpu_time = self._process.cpu_times().user + self._process.cpu_times().system

                await self._in_memory_task_manager.update_worker_info(
                    worker_id=self.worker_id,
                    worker_info={
                        "status": self.status,
                        "current_task_id": task.task_id,
                        "last_heartbeat": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    }
                )

                try:
                    await self._process_and_report(task)
                    self.stats["tasks_succeeded"] += 1
                except Exception as e:
                    logger.error(f"Error processing task {task.task_id}: {e}")
                    await self._report_task_failure(task, str(e))
                    self.stats["tasks_failed"] += 1

                processing_time = time.time() - start_time
                end_cpu_time = self._process.cpu_times().user + self._process.cpu_times().system
                cpu_time_used = end_cpu_time - start_cpu_time

                self.stats["processing_time"] += processing_time
                self.stats["total_cpu_time"] += cpu_time_used
                self.stats["tasks_processed"] += 1
                self.stats["last_task_id"] = task.task_id

                current_memory = self._process.memory_info().rss / (1024 * 1024)
                self.stats["peak_memory_usage"] = max(self.stats["peak_memory_usage"], current_memory)

                self._current_task = None
                self.status = "idle"

                await self._in_memory_task_manager.update_worker_info(
                    worker_id=self.worker_id,
                    worker_info={
                        "status": self.status,
                        "current_task_id": None,
                        "last_heartbeat": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    }
                )

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                await asyncio.sleep(5)

        if self._heartbeat_sender:
            await self._heartbeat_sender.stop()
        if self._resource_monitor_task and not self._resource_monitor_task.done():
            self._resource_monitor_task.cancel()
            try:
                await self._resource_monitor_task
            except asyncio.CancelledError:
                pass

        if shutting_down and self._current_task:
            logger.info("Shutting down, waiting for current task to complete (max 30s)...")
            await asyncio.sleep(30)
            if self._current_task:
                await self._report_task_failure(self._current_task, "Interrupted due to shutdown")

        if self._heartbeat_sender:
            await self._heartbeat_sender.stop()
        if self._resource_monitor_task and not self._resource_monitor_task.done():
            self._resource_monitor_task.cancel()
            try:
                await self._resource_monitor_task
            except asyncio.CancelledError:
                pass

        await self.close()
        logger.info(f"Worker {self.worker_id} stopped")

    async def _process_and_report(self, task: Task) -> Dict[str, Any]:
        """Process a task and report the result."""
        result = await self.process_task(task)
        await self._report_task_success(task, result)
        return result

    async def _report_task_success(self, task: Task, result: Dict[str, Any]) -> None:
        """Report successful task processing (placeholder)."""
        if not task:
            logger.error(f"Failed to report task successful: {result}")
            return
        
        task.mark_as_completed(result)

        try:
            report_data = {
                "task_id": task.task_id,
                "worker_id": self.worker_id, 
                "result": result,
                "extra_data": {
                    "task": task.to_dict(),
                    **self.resource_usage,
                    **self.stats,
                }
            }
            #logger.info(f"Reporting task success to coordinator API: {report_data}")
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.coordinator_url}/api/tasks/{task.task_id}/complete", json=report_data)
                if response.status_code != 200:
                    logger.error(f"Failed to report to coordiantor api: task success: {response.status_code} - {response.text}")
                else:
                    logger.info(f"Task {task.task_id} success reported successfully to coordinator API: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error _report_task_success: {e}")    

    async def _report_task_failure(self, task: Task, error: str) -> None:
        """Report task failure (placeholder)."""
        if not task:
            logger.error(f"Failed to report task failure: {error}")
            return
        task.mark_as_failed(error)

        try:
            report_data = {
                "task_id": task.task_id,
                "worker_id": self.worker_id, 
                "error": error,
                "extra_data": {
                    "task": task.to_dict(),
                    **self.resource_usage,
                    **self.stats,
                }
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.coordinator_url}/api/tasks/{task.task_id}/fail", json=report_data)
                if response.status_code != 200:
                    logger.error(f"Failed to report to coordiantor api: task fail: {response.status_code} - {response.text}")
                else:
                    logger.info(f"Task {task.task_id} fail reported successfully to coordinator API: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error _report_task_success: {e}")    

    async def _monitor_resources(self) -> None:
        """Monitor system resources."""
        net_io_start = psutil.net_io_counters()
        last_bytes_sent = net_io_start.bytes_sent
        last_bytes_recv = net_io_start.bytes_recv
        last_check_time = time.time()

        self.resource_usage["hostname"] = self.hostname
        self.resource_usage["ip_address"] = self.ip_address
        self.resource_usage["platform"] = self.platform
        self.resource_usage["architecture"] = self.architecture
        self.resource_usage["python_version"] = self.python_version

        while self._running:
            try:
                self.resource_usage["current_memory_usage"] = self._process.memory_info().rss / (1024 * 1024) # MB
                self.resource_usage["cpu_percent"] = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                self.resource_usage["memory_percent"] = mem.percent
                disk = psutil.disk_usage('/')
                self.resource_usage["disk_usage_percent"] = disk.percent
                if hasattr(os, "getloadavg"):
                    self.resource_usage["load_average"] = os.getloadavg()

                net_io = psutil.net_io_counters()
                current_time = time.time()
                time_elapsed = current_time - last_check_time
                bytes_sent_rate = (net_io.bytes_sent - last_bytes_sent) / time_elapsed
                bytes_recv_rate = (net_io.bytes_recv - last_bytes_recv) / time_elapsed

                self.resource_usage["network_io"] = {
                    "bytes_sent": bytes_sent_rate,
                    "bytes_recv": bytes_recv_rate,
                    "total_sent": net_io.bytes_sent,
                    "total_recv": net_io.bytes_recv
                }

                last_bytes_sent = net_io.bytes_sent
                last_bytes_recv = net_io.bytes_recv
                last_check_time = current_time

                self.resource_usage["process_count"] = len(psutil.pids())
                self.resource_usage["thread_count"] = self._process.num_threads()
                self.resource_usage["timestamp"] = last_check_time
                await asyncio.sleep(self.resource_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
                await asyncio.sleep(self.resource_check_interval)