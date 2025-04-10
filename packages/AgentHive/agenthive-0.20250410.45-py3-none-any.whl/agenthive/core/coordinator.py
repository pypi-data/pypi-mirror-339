"""
Coordinator class for py-AgentHive.
"""
import os
import time
import json
import uuid
import logging
import asyncio
import socket
from typing import Dict, Any, Optional, List, Type, Set, Tuple, Callable
import datetime

import redis.asyncio as redis

from agenthive.core.task import Task
from agenthive.core.heartbeat.manager import HeartbeatManager
from agenthive.core.heartbeat.monitor import HeartbeatMonitor
from agenthive.core.heartbeat.models import HeartbeatData
from agenthive.core.heartbeat.constants import HeartbeatEventType
from agenthive.db.adapters.base import BaseDBAdapter
from agenthive.utils.datetime_utils import convert_to_timestamp, convert_to_datetime
from agenthive.core.in_memory_task_manager import InMemoryTaskManager
from agenthive.utils.health import get_system_metrics

logger = logging.getLogger(__name__)

class Coordinator:
    """
    Coordinator class for managing tasks and workers in the py-AgentHive framework.
    
    The coordinator is responsible for:
    - Accepting and distributing tasks to workers
    - Tracking worker status and capabilities
    - Monitoring task status and handling retries
    - Storing task results and metrics
    - Collecting worker heartbeats and system metrics
    
    This implementation is designed for high availability, avoiding local state
    and using Redis and database as the source of truth.
    
    Attributes:
        redis_url (str): URL of the Redis instance for task queue and worker tracking
        db_url (Optional[str]): URL of the database for persistent storage
    """
    
    def __init__(self, 
                 redis_url: str,
                 db_url: Optional[str] = None,
                 worker_timeout: int = 60,
                 storage_backend: str = "redis",
                 metrics_enabled: bool = True,
                 metrics_retention: int = 24*60*60,  # Default 1 day retention
                 db_adapter: Optional[BaseDBAdapter] = None):
        """
        Initialize a new Coordinator.
        
        Args:
            redis_url: URL of the Redis instance
            db_url: URL of the database for persistent storage (optional)
            worker_timeout: Timeout in seconds for worker heartbeats
            storage_backend: Storage backend to use ("redis" or "postgresql")
            metrics_enabled: Whether to collect and store metrics
            metrics_retention: How long to keep metrics data (in seconds)
            db_adapter: Database adapter (optional, will be created from db_url if not provided)
        """
        self.redis_url = redis_url
        self.db_url = db_url
        self.worker_timeout = worker_timeout
        self.storage_backend = storage_backend
        self.metrics_enabled = metrics_enabled
        self.metrics_retention = metrics_retention
        
        # Runtime attributes
        self._running = False
        self._start_time = time.time()
        self._instance_id = f"{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:8]}"
        
        # Redis client
        self._redis_client = None
        
        # Database adapter
        self._db_adapter = db_adapter
        
        # Heartbeat components
        self._heartbeat_manager = None
        self._heartbeat_monitor = None
        
        # Task hooks - these are needed for callback functionality
        # but they only exist in the local instance and don't affect HA
        self._on_task_complete_hooks = []
        self._on_task_failed_hooks = []
        self._on_worker_join_hooks = []
        self._on_worker_leave_hooks = []

        self._in_memory_task_manager = None
    
    async def initialize(self) -> None:
        """
        Initialize the coordinator.
        
        This method connects to Redis and the database (if configured),
        and sets up the necessary data structures.
        """
        logger.info(f"Initializing coordinator with Redis at {self.redis_url}")
        
        # Initialize Redis client
        self._redis_client = redis.from_url(self.redis_url)

        self._in_memory_task_manager = InMemoryTaskManager(
            redis_url=self.redis_url,
        )
        
        # Initialize database adapter if configured
        if self.db_url and not self._db_adapter:
            try:
                logger.debug(f"Initializing database adapter for {self.db_url}")
                # Try to import the adapter factory
                try:
                    from agenthive.db.adapters.sqlalchemy import SQLAlchemyAdapter
                    # Create adapter based on database URL
                    self._db_adapter = SQLAlchemyAdapter(self.db_url)
                except ImportError:
                    self._db_adapter = None
                
                # Connect to the database if adapter was created
                if self._db_adapter:
                    await self._db_adapter.connect()
                    logger.info("Database adapter connected successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database adapter: {e}")
                self._db_adapter = None

        # Initialize heartbeat manager
        self._heartbeat_manager = HeartbeatManager(
            redis_client=self._redis_client,
            worker_timeout=self.worker_timeout,
            metrics_enabled=self.metrics_enabled
        )
        await self._heartbeat_manager.initialize()
        
        # Register heartbeat callbacks
        self._heartbeat_manager.on_worker_active(self._handle_worker_active)
        self._heartbeat_manager.on_worker_inactive(self._handle_worker_inactive)
        
        # Initialize heartbeat monitor
        self._heartbeat_monitor = HeartbeatMonitor(
            redis_url=self.redis_url,
            worker_timeout_seconds=self.worker_timeout,
            db_adapter=self._db_adapter  # Pass the database adapter
        )

        self._heartbeat_monitor.register_heartbeat_callback(self._handle_worker_heartbeat)
        
        # Announce this Coordinator instance as active
        await self._announce_coordinator_startup()
        
        self._running = True
        
        logger.debug("Coordinator initialized successfully")

    async def _announce_coordinator_startup(self) -> None:
        """
        Announce this coordinator instance to other instances.
        This allows existing instances to pause certain operations
        until the new instance has completed initialization.
        """
        if not self._redis_client:
            return
        
        # Publish startup event
        startup_event = {
            "event": "coordinator_starting",
            "instance_id": self._instance_id,
            "hostname": socket.gethostname(),
            "pid": os.getpid(),
            "timestamp": time.time()
        }
        
        await self._redis_client.publish("coordinator_events", json.dumps(startup_event))
        
        # Add instance to active coordinators set
        await self._redis_client.hset(
            "active_coordinators",
            self._instance_id,
            json.dumps({"status": "starting", "start_time": time.time()})
        )
        
        # Publish ready event
        ready_event = {
            "event": "coordinator_ready",
            "instance_id": self._instance_id,
            "timestamp": time.time()
        }
        
        await self._redis_client.publish("coordinator_events", json.dumps(ready_event))
        
        # Update status
        await self._redis_client.hset(
            "active_coordinators",
            self._instance_id,
            json.dumps({
                "status": "ready", 
                "start_time": time.time(),
                "hostname": socket.gethostname(),
                "pid": os.getpid()
            })
        )
        
        # Set expiration time to prevent stale status on crash
        await self._redis_client.expire(f"active_coordinators:{self._instance_id}", 300)  # 5 minute timeout
        
        # Start periodic status update coroutine
        asyncio.create_task(self._update_active_status())

    async def _update_active_status(self) -> None:
        """
        Periodically update this coordinator instance's active status.
        """
        while self._running:
            try:
                # Update every 60 seconds
                await asyncio.sleep(60)
                
                if self._redis_client:
                    # Update active status and extend expiration time
                    await self._redis_client.hset(
                        "active_coordinators", 
                        self._instance_id,
                        json.dumps({
                            "status": "active",
                            "start_time": self._start_time,
                            "last_updated": time.time(),
                            "hostname": socket.gethostname(),
                            "pid": os.getpid()
                        })
                    )
                    # Extend expiration time
                    await self._redis_client.expire(f"active_coordinators:{self._instance_id}", 300)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error updating coordinator active status: {e}")

    async def _load_tasks_from_database(self, max_initial_tasks: int = 100) -> int:
        """
        Load incomplete tasks from the database to Redis.
        This ensures task state is correctly restored after system restart.
        """
        if not self._db_adapter or not hasattr(self._db_adapter, 'get_pending_tasks'):
            logger.error("Cannot load tasks from database: adapter unavailable or missing get_pending_tasks method")
            return 0
        
        try:
            # Get all incomplete (pending, assigned) tasks from database
            logger.info("Loading pending tasks from database to Redis...")
            pending_tasks = await self._db_adapter.get_pending_tasks(max_initial_tasks)
            
            if not pending_tasks:
                logger.info("No pending tasks to load")
                return 0
            
            logger.info(f"\n\nLoaded {len(pending_tasks)} pending tasks from database\n\n")

            loaded_count = await self._in_memory_task_manager.add_and_check_multiple_tasks_exists(
                tasks=pending_tasks,
            )
            logger.info(f"\n\nSuccessfully loaded {loaded_count} tasks from database to Redis\n\n")
            return loaded_count
        except Exception as e:
            logger.error(f"Error loading tasks from database: {e}")
        return 0

    async def start(self) -> None:
        """
        Start the coordinator.
        
        This method starts the coordinator services, including the worker monitoring
        task and the task scheduling task.
        """
        if not self._running:
            await self.initialize()
        
        logger.debug("Starting coordinator services")
        
        # Start heartbeat monitor
        await self._heartbeat_monitor.start()
        
        # Start heartbeat manager
        await self._heartbeat_manager.start_monitoring()
        
        # Start task scheduling task
        asyncio.create_task(self._schedule_tasks())
        
        # Start metrics collection if enabled
        if self.metrics_enabled:
            asyncio.create_task(self._collect_metrics())
        
        logger.info("Coordinator services started")
    
    async def stop(self) -> None:
        """
        Stop the coordinator.
        
        This method stops all coordinator services gracefully.
        """
        logger.debug("Stopping coordinator")
        self._running = False
        
        # Mark coordinator as stopping in Redis
        if self._redis_client:
            try:
                await self._redis_client.hset(
                    "active_coordinators",
                    self._instance_id,
                    json.dumps({
                        "status": "stopping",
                        "start_time": self._start_time,
                        "stop_time": time.time()
                    })
                )
                
                # Publish shutdown event
                shutdown_event = {
                    "event": "coordinator_stopping",
                    "instance_id": self._instance_id,
                    "timestamp": time.time()
                }
                await self._redis_client.publish("coordinator_events", json.dumps(shutdown_event))
                
                # Remove from active coordinators after a brief delay
                await asyncio.sleep(1)
                await self._redis_client.hdel("active_coordinators", self._instance_id)
            except Exception as e:
                logger.error(f"Error updating coordinator status on shutdown: {e}")
        
        # Stop heartbeat services
        if self._heartbeat_monitor:
            await self._heartbeat_monitor.stop()
        
        if self._heartbeat_manager:
            await self._heartbeat_manager.stop_monitoring()
        
        # Close Redis connection
        if self._redis_client:
            await self._redis_client.close()
        
        # Close database adapter
        if self._db_adapter:
            try:
                await self._db_adapter.close()
                logger.info("Database adapter closed successfully")
            except Exception as e:
                logger.error(f"Error closing database adapter: {e}")
        
        # Stop in-memory task manager
        if self._in_memory_task_manager:
            self._in_memory_task_manager = None

        logger.info("Coordinator stopped")
    
    async def submit_task(self, task: Task) -> str:
        """
        Submit a task for processing.
        
        Args:
            task: The task to submit
            
        Returns:
            str: The task ID
        """
        logger.debug(f"Submitting task: {task}")

        if not self._in_memory_task_manager:
            logger.error("In-memory task manager not available, cannot submit task")
            return None

        # Store the task
        task_data = task.to_dict()
        task_id = task.task_id
        
        logger.debug(f"Task data: {task_data}")

        if await self._in_memory_task_manager.add_and_check_multiple_tasks_exists([task_data]) == None:
            logger.error(f"Duplicate task ID {task_id} detected in in-memory task manager")
            return None
        
        # Store in database if available
        if self._db_adapter and hasattr(self._db_adapter, 'save_task'):
            try:
                logger.debug(f"Storing task in database: {task_data}")
                # Use db_adapter to store task
                await self._db_adapter.save_task(task_data)
                
                # Task was stored in DB, so mark as synced
                if self._redis_client:
                    await self._redis_client.delete(f"task:{task_id}:needs_sync")
            except Exception as e:
                logger.error(f"Error storing task in database: {e}")
        
        logger.debug(f"Task {task_id} submitted with priority {task.priority}")
        
        return task_id
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task.
        
        Args:
            task_id: ID of the task to check
            
        Returns:
            Dict[str, Any]: Task status information
        """
        # Try to get from Redis first
        if self._redis_client:
            task_data = await self._redis_client.hgetall(f"task:{task_id}")
            if task_data:
                return {k.decode('utf-8'): self._try_decode_json(v) 
                        if isinstance(v, bytes) else v 
                        for k, v in task_data.items()}
        
        # Try to get from database if available
        if self._db_adapter and hasattr(self._db_adapter, 'get_task'):
            try:
                task_data = await self._db_adapter.get_task(task_id)
                if task_data:
                    # Sync to Redis if we found it in the database but not in Redis
                    if self._redis_client:
                        # Convert to string format for Redis hset
                        redis_data = {}
                        for k, v in task_data.items():
                            if isinstance(v, (dict, list)):
                                redis_data[k] = json.dumps(v)
                            elif v is None:
                                redis_data[k] = ""
                            else:
                                redis_data[k] = str(v)
                        
                        await self._redis_client.hset(f"task:{task_id}", mapping=redis_data)
                        
                        # Add to appropriate set based on status
                        status = task_data.get("status", "pending")
                        if status == "completed" and "completed_at" in task_data:
                            await self._redis_client.zadd("tasks:completed", {task_id: task_data["completed_at"]})
                        elif status == "failed" and "failed_at" in task_data:
                            await self._redis_client.zadd("tasks:failed", {task_id: task_data["failed_at"]})
                        elif status == "pending":
                            await self._redis_client.zadd("tasks:pending", {task_id: task_data.get("priority", 0)})
                        
                    return task_data
            except Exception as e:
                logger.error(f"Error getting task status from database: {e}")
        
        return {"status": "unknown", "error": "Task not found"}
    
    def _try_decode_json(self, value):
        """Helper method to try decoding JSON values."""
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    async def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the result of a completed task.
        
        Args:
            task_id: ID of the task to get the result for
            
        Returns:
            Optional[Dict[str, Any]]: Task result, or None if the task is not completed
        """
        # Try to get from Redis first
        if self._in_memory_task_manager:
            task_data = self._in_memory_task_manager.get_task_info(task_id)
            if task_data:
                return task_data["result"] if "result" in task_data else None

        # Try to get from database if available
        if self._db_adapter and hasattr(self._db_adapter, 'get_task'):
            try:
                task_data = await self._db_adapter.get_task(task_id)
                if task_data and "result" in task_data:
                    return task_data["result"]
            except Exception as e:
                logger.error(f"Error getting task result from database: {e}")
        
        return None
    
    async def register_worker(self, worker_id: str, capabilities: List[str],
                             configured_capabilities: List[str], 
                             available_capabilities: List[str],
                             hostname: str, ip_address: str, 
                             tags: Optional[List[str]] = None) -> bool:
        """
        Register a worker with the coordinator.
        
        Args:
            worker_id: Worker ID
            capabilities: List of task types this worker can handle
            configured_capabilities: List of task types configured for this worker
            available_capabilities: List of all available task types
            hostname: Worker's hostname
            ip_address: Worker's IP address
            tags: Optional tags for categorizing the worker
            
        Returns:
            bool: True if registration was successful
        """
        # Create Redis worker info dictionary

        capabilities=list(set(capabilities))
        configured_capabilities=list(set(configured_capabilities))
        available_capabilities=list(set(available_capabilities))

        keyvalue_worker_info = {
            "worker_id": worker_id,
            "status": "idle",
            "current_task": None,
            "resource_usage": {},
            "last_heartbeat": datetime.datetime.now(datetime.timezone.utc),
            "registered_at": datetime.datetime.now(datetime.timezone.utc),

            "capabilities": capabilities,
            "configured_capabilities": configured_capabilities,
            "available_capabilities": available_capabilities,
        }

        base_worker_info = {
            **keyvalue_worker_info,
            "hostname": hostname,
            "ip_address": ip_address,
            "tasks_processed": 0,
            "tags": tags or [],
        }

        await self._in_memory_task_manager.register_worker(
            worker_id=worker_id, 
            worker_info=keyvalue_worker_info,
            capabilities=capabilities,
        )

        # Store in database if available
        if self._db_adapter and hasattr(self._db_adapter, 'save_worker'):
            try:
                # Use db_adapter to store worker
                await self._db_adapter.save_worker(base_worker_info)
            except Exception as e:
                logger.error(f"Error storing worker in database: {e}")
        
        # Run worker join hooks
        for hook in self._on_worker_join_hooks:
            try:
                hook(worker_id, base_worker_info)
            except Exception as e:
                logger.error(f"Error in worker join hook: {e}")
        
        logger.info(f"Worker {worker_id} registered with capabilities: {capabilities}")
        return True

    async def worker_heartbeat(self, worker_id: str, status: str, 
                              current_task: Optional[str] = None,
                              resource_usage: Optional[Dict[str, Any]] = None,
                              stats: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update worker heartbeat information.
        
        Args:
            worker_id: Worker ID
            status: Worker status (idle, busy, etc.)
            current_task: ID of task currently being processed (if any)
            resource_usage: System resource usage metrics
            stats: Other worker statistics
            
        Returns:
            bool: True if heartbeat was processed successfully
        """

        # Create heartbeat data
        heartbeat = HeartbeatData(
            worker_id=worker_id,
            status=status,
            current_task=current_task,
            resource_usage=resource_usage or {},
            stats=stats or {}
        )

        # Process heartbeat using the heartbeat manager
        if self._heartbeat_manager:
            return await self._heartbeat_manager.process_heartbeat(heartbeat)
        
        logger.warning(f"Heartbeat manager not available, skipping heartbeat processing for worker {worker_id}")
        return False
    
    async def report_task_complete(self, worker_id: str, task_id: str,
                                  result: Dict[str, Any], extra_data: Dict[str, Any] = None) -> bool:
        """
        Report that a task has been completed.
        
        Args:
            worker_id: ID of the worker that completed the task
            task_id: ID of the completed task
            result: Result of the task
            
        Returns:
            bool: True if the report was accepted, False otherwise
        """
        #logger.info(f"Reporting task completion for task {task_id} by worker {worker_id}, result: {result}")
        if not worker_id or not task_id:
            logger.error("Worker ID and task ID must be provided")
            return False
        
        if self._db_adapter and hasattr(self._db_adapter, 'update_task'):
            #logger.info(f"Updating task status in database for task {task_id}")
            update_data = {
                "status": "completed",
                "result": result["output_data"] if result and 'output_data' in result else result,
                "assigned_to": worker_id,
                "completed_at": datetime.datetime.now(datetime.timezone.utc),
            }
            if extra_data:
                update_data["extra_data"] = extra_data

            if result and 'started_at' in result:
                update_data["started_at"] = convert_to_datetime(result["started_at"])

            #logger.info(f"Updating task status in database for task {task_id}, data: {update_data}")
            update_result = await self._db_adapter.update_task(
                task_id=task_id, update_data=update_data
            )
            if not update_result:
                logger.error(f"Failed to report_task_complete in database for task {task_id}, update_data: {update_data}")
                return False

        if not self._in_memory_task_manager:
            logger.error("In-memory task manager not available, cannot report task completion at report_task_complete")
            return False
        
        await self._in_memory_task_manager.set_task_status_to_done(task_id=task_id)

        return True
    
    async def report_task_failure(self, worker_id: str, task_id: str,
                                 error: str, extra_data: Dict[str, Any] = None) -> bool:
        """
        Report that a task has failed.
        
        Args:
            worker_id: ID of the worker that attempted the task
            task_id: ID of the failed task
            error: Error message
            
        Returns:
            bool: True if the report was accepted, False otherwise
        """
        # Use distributed lock to ensure atomic operation

        if not worker_id or not task_id:
            logger.error("Worker ID and task ID must be provided")
            return False
        
        if self._db_adapter and hasattr(self._db_adapter, 'update_task'):
            #logger.info(f"Updating task status in database for task {task_id}")
            update_data = {
                "status": "failed",
                "assigned_to": worker_id,
                "error": [error],
                "completed_at": datetime.datetime.now(datetime.timezone.utc),
            }
            
            if extra_data:
                update_data["extra_data"] = extra_data

            update_result = await self._db_adapter.update_task(
                task_id=task_id, update_data=update_data
            )
            if not update_result:
                logger.error(f"Failed to report_task_failure to database for task {task_id}, update_data: {update_data}")
                return False

        if not self._in_memory_task_manager:
            logger.error("In-memory task manager not available, cannot report task completion at report_task_failure")
            return False
        
        await self._in_memory_task_manager.set_task_status_to_done(task_id=task_id)
        return True
    
    async def get_next_task(self, worker_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the next task for a worker to process.
        
        Args:
            worker_id: ID of the worker requesting a task
            
        Returns:
            Optional[Dict[str, Any]]: Task data, or None if no suitable task is available
        """
        # Verify worker exists in Redis
        if self._redis_client:
            exists = await self._redis_client.exists(f"worker:{worker_id}")
            if not exists:
                logger.error(f"Task request from unregistered worker: {worker_id}")
                return None
        else:
            logger.error("Redis client not available, cannot assign tasks")
            return None
        
        # Get worker capabilities from Redis
        worker_capabilities = []
        
        if self._redis_client:
            caps_data = await self._redis_client.hget(f"worker:{worker_id}", "capabilities")
            if caps_data:
                try:
                    worker_capabilities = json.loads(caps_data.decode('utf-8') if isinstance(caps_data, bytes) else caps_data)
                except json.JSONDecodeError:
                    logger.error(f"Error parsing worker capabilities: {caps_data}")
                    worker_capabilities = []
        
        logger.info(f"Worker {worker_id} requesting task with capabilities: {worker_capabilities}")
        
        # Use distributed lock for task assignment
        task_assigned = False
        assigned_task = None
        
        if self._redis_client:
            # Get global task assignment lock
            lock_key = "task_assignment_lock"
            got_lock = await self._redis_client.set(
                lock_key, 
                "1", 
                nx=True,
                ex=2  # Short expiry to prevent delays
            )
            
            try:
                if not got_lock:
                    logger.debug("Another coordinator is assigning tasks, waiting briefly...")
                    # Wait briefly before returning None - another coordinator has the lock
                    await asyncio.sleep(0.1)
                    return None
                
                # Get highest priority pending tasks
                pending_tasks = await self._redis_client.zrevrange("tasks:pending", 0, 20, withscores=True)

                #logger.debug(f"Found {len(pending_tasks)} pending tasks")
                
                for task_id_bytes, score in pending_tasks:
                    task_id = task_id_bytes.decode('utf-8') if isinstance(task_id_bytes, bytes) else task_id_bytes

                    #logger.info(f"Checking task {task_id}")

                    # Get task-specific lock to prevent race conditions
                    task_lock_key = f"task_lock:{task_id}"
                    got_task_lock = await self._redis_client.set(
                        task_lock_key, 
                        "1", 
                        nx=True,
                        ex=5
                    )
                    
                    if not got_task_lock:
                        # Another coordinator is working with this task, skip
                        continue
                    
                    try:
                        # Get task status to verify it's still pending
                        task_status = await self._redis_client.hget(f"task:{task_id}", "status")

                        #logger.debug(f"Task {task_id} status: {task_status}, type: {type(task_status)}")

                        if not task_status:
                            continue

                        task_status = task_status.decode('utf-8') if isinstance(task_status, bytes) else task_status
                        if task_status != "pending":
                            # Task is not actually pending, skip
                            continue

                        # Get task data
                        task_data_dict = await self._redis_client.hgetall(f"task:{task_id}")
                        if not task_data_dict:
                            continue

                        #logger.info(f"Task {task_id} task_data_dict: {task_data_dict}")

                        # Convert bytes to string and parse JSON values
                        task_data = {}
                        for key_bytes, value_bytes in task_data_dict.items():
                            key = key_bytes.decode('utf-8') if isinstance(key_bytes, bytes) else key_bytes
                            value = value_bytes.decode('utf-8') if isinstance(value_bytes, bytes) else value_bytes
                            
                            # Try to parse JSON values
                            try:
                                task_data[key] = json.loads(value)
                            except json.JSONDecodeError:
                                task_data[key] = value
                        
                        #logger.info(f"Task {task_id} data: {task_data}")
                        
                        # Check if worker can process this task type
                        task_type = task_data.get("task_type")
                        if task_type in worker_capabilities:
                            # Assign task to worker
                            assignment_time = time.time()
                            
                            pipe = self._redis_client.pipeline()
                            pipe.hset(f"task:{task_id}", "status", "assigned")
                            pipe.hset(f"task:{task_id}", "assigned_to", worker_id)
                            pipe.hset(f"task:{task_id}", "assigned_at", str(assignment_time))
                            pipe.hset(f"task:{task_id}", "last_updated", str(assignment_time))
                            pipe.set(f"task:{task_id}:needs_sync", "1", ex=600)
                            
                            # Update worker status
                            pipe.hset(f"worker:{worker_id}", "status", "busy")
                            pipe.hset(f"worker:{worker_id}", "current_task", task_id)
                            
                            await pipe.execute()
                            
                            # Update in database if available
                            if self._db_adapter:
                                try:
                                    # Update task assignment in database
                                    if hasattr(self._db_adapter, 'update_task_status'):
                                        await self._db_adapter.update_task_status(
                                            task_id=task_id, 
                                            status="assigned",
                                            assigned_to=worker_id,
                                            assigned_at=assignment_time
                                        )
                                    
                                    # Update worker status in database
                                    if hasattr(self._db_adapter, 'update_worker_status'):
                                        await self._db_adapter.update_worker_status(
                                            worker_id=worker_id,
                                            status="busy",
                                            current_task_id=task_id
                                        )
                                    
                                    # Task was updated in DB, so mark as synced
                                    await self._redis_client.delete(f"task:{task_id}:needs_sync")
                                except Exception as e:
                                    logger.error(f"Error updating task assignment in database: {e}")
                            
                            logger.info(f"Task {task_id} assigned to worker {worker_id}")
                            task_assigned = True
                            assigned_task = task_data
                            break
                    finally:
                        # Release task-specific lock
                        await self._redis_client.delete(task_lock_key)
            finally:
                # Release global lock
                await self._redis_client.delete(lock_key)
        
        if task_assigned:
            return assigned_task
        
        # If we get here, no suitable task was found
        return None
    
    def on_task_complete(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Register a callback to be called when a task is completed.
        
        Args:
            callback: Callback function that takes task_id and result as arguments
        """
        self._on_task_complete_hooks.append(callback)
    
    def on_task_failed(self, callback: Callable[[str, str], None]) -> None:
        """
        Register a callback to be called when a task fails.
        
        Args:
            callback: Callback function that takes task_id and error as arguments
        """
        self._on_task_failed_hooks.append(callback)
    
    def on_worker_join(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Register a callback to be called when a worker joins.
        
        Args:
            callback: Callback function that takes worker_id and worker_info as arguments
        """
        self._on_worker_join_hooks.append(callback)
    
    def on_worker_leave(self, callback: Callable[[str], None]) -> None:
        """
        Register a callback to be called when a worker leaves.
        
        Args:
            callback: Callback function that takes worker_id as argument
        """
        self._on_worker_leave_hooks.append(callback)

    async def get_overview_info(self) -> Dict[str, Any]:
        output = {
            # current time
            "timestamp": time.time(),
            "datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),

            "coordinator": {
                # 僅一台 coordinator server 資訊
                "start_time": self._start_time,
                "supported_task_types": [],
                "throughput": 0,
                "resource_usage": {

                }
            },
            "workers": {
                "active": 0,
                "idle": 0,
                "busy": 0,
                "total_tasks_processed": 0,
                "avg_cpu_usage": 0,
                "avg_memory_usage": 0,
                "workers_by_capability": {},
                "details": []
            }, 
            "tasks": {
                "pending": 0,
                "assigned": 0,
                "completed": 0,
                "failed": 0,
                "total": 0,
                "avg_completion_time": 0,
                "avg_waiting_time": 0,
                "throughput": 0,
            },
            "error": None,
        }

        try:
            output["coordinator"]["resource_usage"] = get_system_metrics()
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            output["error"] = str(e)

        try:
            if self._in_memory_task_manager:
                sub_output = await self._in_memory_task_manager.get_service_metrics_per_minute(minutes=2)
                if sub_output and "status" in sub_output and sub_output["status"]:
                    output["coordinator"]["throughput"] = sub_output["tasks_per_minute"] if "tasks_per_minute" in sub_output else -1
                    output["coordinator"]["supported_task_types"] = sub_output["supported_task_types"] if "supported_task_types" in sub_output else []
                    output["workers"]["active"] = sub_output["active_workers"] if "active_workers" in sub_output else -1
                    output["tasks"]["throughput"] = sub_output["tasks_per_minute"] if "tasks_per_minute" in sub_output else -1

                    output["tasks"]["pending"] = sub_output["tasks_pending"] if "tasks_pending" in sub_output else -1
                    output["tasks"]["assigned"] = sub_output["tasks_running"] if "tasks_running" in sub_output else -1

                    if "workers" in sub_output:
                        #logger.info(f"Worker details: {sub_output['workers']}")
                        output["workers"]["details"] = sub_output["workers"]
                else:
                    output["error"] = "Failed to get service metrics from in-memory task manager"
                    logger.error(f"Failed to get service metrics from in-memory task manager: {sub_output}")

            if self._db_adapter:
                try:
                    if hasattr(self._db_adapter, 'get_tasks_state_count'):
                        check_tasks_status = await self._db_adapter.get_tasks_state_count(minutes=2)
                        if check_tasks_status:
                            for key, value in check_tasks_status.items():
                                if key in output["tasks"] and key in ["completed", "failed"]:
                                    output["tasks"][key] = value
                        logger.info(f"Tasks state count via db query: {check_tasks_status}")
                except Exception as e:
                    logger.error(f"Error updating task status in database: {e}")

            output["tasks"]["total"] = output["tasks"]["pending"] + output["tasks"]["assigned"] + output["tasks"]["completed"] + output["tasks"]["failed"]

        except Exception as e:
            logger.error(f"Error getting service metrics: {e}")
            output["error"] = str(e)
        return output
    
    async def get_active_workers(self) -> List[Dict[str, Any]]:
        """
        Get information about all active workers.
        
        Returns:
            List[Dict[str, Any]]: List of worker information dictionaries
        """
        # Use heartbeat monitor if available
        if self._heartbeat_monitor:
            return await self._heartbeat_monitor.get_active_workers()
        
        # Try to get workers from database if available
        if self._db_adapter and hasattr(self._db_adapter, 'get_active_workers'):
            try:
                workers = await self._db_adapter.get_active_workers(timeout_seconds=self.worker_timeout)
                if workers:
                    return workers
            except Exception as e:
                logger.error(f"Error getting active workers from database: {e}")
        
        return []

    async def get_task_metrics(self) -> Dict[str, Any]:
        """
        Get metrics about tasks in the system.
        
        Returns:
            Dict[str, Any]: Task metrics
        """
        metrics = {
            "datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "pending": 0,
            "assigned": 0,
            "completed": 0,
            "failed": 0,
            "waiting": 0,
            "total": 0,
            "avg_completion_time": 0,
            "avg_waiting_time": 0,
            "throughput": 0,  # Tasks per minute
        }
            
        return metrics
    
    async def get_worker_metrics(self) -> Dict[str, Any]:
        """
        Get metrics about workers in the system.
        
        Returns:
            Dict[str, Any]: Worker metrics
        """
        metrics = {
            "datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "active": 0,
            "idle": 0,
            "busy": 0,
            "total_tasks_processed": 0,
            "avg_cpu_usage": 0,
            "avg_memory_usage": 0,
            "workers_by_capability": {},
        }

        return metrics
    
    def _handle_worker_active(self, worker_id: str, heartbeat_data: Dict[str, Any]) -> None:
        """
        Handle worker active event from heartbeat manager.
        
        Args:
            worker_id: ID of the worker
            heartbeat_data: Heartbeat data from worker
        """
        # Only execute hooks for newly active workers
        is_new_worker = False
        
        # Check in Redis if this is a new worker registration
        asyncio.create_task(self._check_new_worker_and_run_hooks(worker_id, heartbeat_data))
    
    async def _check_new_worker_and_run_hooks(self, worker_id: str, heartbeat_data: Dict[str, Any]) -> None:
        """
        Check if a worker is newly registered and run appropriate hooks.
        
        Args:
            worker_id: ID of the worker
            heartbeat_data: Heartbeat data from worker
        """
        if self._redis_client:
            # Get previous registration time
            registration_time = await self._redis_client.hget(f"worker:{worker_id}", "registered_at")
            current_time = time.time()
            
            # If recently registered (within 5 seconds), run join hooks
            if registration_time:
                try:
                    reg_time = float(registration_time.decode('utf-8') if isinstance(registration_time, bytes) else registration_time)
                    if current_time - reg_time < 5:  # Consider it new if registered within last 5 seconds
                        logger.info(f"New worker {worker_id} joined")
                        
                        # Get worker capabilities for logging
                        capabilities = heartbeat_data.get("capabilities", [])
                        if capabilities:
                            cap_str = ", ".join(capabilities) if isinstance(capabilities, list) else "unknown"
                            logger.info(f"Worker {worker_id} capabilities: {cap_str}")
                        
                        # Run worker join hooks
                        self._run_worker_join_hooks(worker_id, heartbeat_data)
                except (ValueError, TypeError):
                    pass
    
    def _run_worker_join_hooks(self, worker_id: str, worker_info: Dict[str, Any]) -> None:
        """
        Run all registered worker join hooks.
        
        Args:
            worker_id: ID of the worker
            worker_info: Worker information
        """
        for hook in self._on_worker_join_hooks:
            try:
                hook(worker_id, worker_info)
            except Exception as e:
                logger.error(f"Error in worker join hook for {worker_id}: {e}")
    
    def _handle_worker_inactive(self, worker_id: str, current_task_id: Optional[str]) -> None:
        """
        Handle worker inactive event from heartbeat manager.
        
        Args:
            worker_id: ID of the worker
            current_task_id: ID of the task the worker was processing (if any)
        """
        logger.warning(f"Worker {worker_id} became inactive")
        
        # Log worker stats from Redis before removal
        asyncio.create_task(self._log_worker_stats_from_redis(worker_id))
        
        # Run worker leave hooks
        self._run_worker_leave_hooks(worker_id)
    
    async def _log_worker_stats_from_redis(self, worker_id: str) -> None:
        """
        Log worker statistics from Redis before the worker record is removed.
        
        Args:
            worker_id: ID of the worker
        """
        if self._redis_client:
            try:
                # Get worker data
                worker_data = await self._redis_client.hgetall(f"worker:{worker_id}")
                if worker_data:
                    # Extract key metrics
                    tasks_processed = 0
                    registered_at = time.time()
                    
                    if b'tasks_processed' in worker_data:
                        try:
                            tasks_processed = int(worker_data[b'tasks_processed'].decode('utf-8'))
                        except (ValueError, TypeError):
                            pass
                    
                    if b'registered_at' in worker_data:
                        try:
                            registered_at = float(worker_data[b'registered_at'].decode('utf-8'))
                        except (ValueError, TypeError):
                            pass
                    
                    uptime = time.time() - registered_at
                    logger.info(f"Worker {worker_id} stats: processed {tasks_processed} tasks, uptime {uptime:.2f}s")
            except Exception as e:
                logger.error(f"Error logging worker stats: {e}")
    

    async def _handle_worker_heartbeat(self, heartbeat_data: Dict[str, Any]) -> None:
        """
        Extract heartbeat data and update task status.
        """
        if self._in_memory_task_manager:
            await self._in_memory_task_manager.update_task_status_from_heartbeat(heartbeat_data)


    def _run_worker_leave_hooks(self, worker_id: str) -> None:
        """
        Run all registered worker leave hooks.
        
        Args:
            worker_id: ID of the worker
        """
        for hook in self._on_worker_leave_hooks:
            try:
                hook(worker_id)
            except Exception as e:
                logger.error(f"Error in worker leave hook for {worker_id}: {e}")
    
    async def _schedule_tasks(self) -> None:
        """
        Schedule tasks for execution.
        
        This method runs periodically and schedules pending tasks for execution
        based on priorities and available workers.
        """
        logger.info("Task scheduling service started")
        
        while self._running:
            try:
                # load tasks from database
                await self._load_tasks_from_database()

                #await self._check_timed_out_tasks()
                
                await asyncio.sleep(600)
            except asyncio.CancelledError:
                logger.info("Task scheduling service stopped")
                break
            except Exception as e:
                logger.error(f"Error in task scheduling: {e}")
                await asyncio.sleep(10)
        logger.info("Task scheduling service finished")
    
    async def _check_timed_out_tasks(self) -> None:
        """
        Check for timed out tasks and handle them.
        """
        pass
    
    async def _collect_metrics(self) -> None:
        """
        Collect and store system metrics.
        
        This method runs periodically and collects metrics from Redis and stores
        them in the database for historical analysis.
        """
        if not self.metrics_enabled:
            return
        
        logger.info("Metrics collection service started")
        
        try:
            while self._running:
                # Check once per second if metrics need to be collected
                current_time = int(time.time())
                
                # Collect system metrics every minute
                if current_time % 60 == 0:
                    await self._collect_and_store_metrics(current_time)
                
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Metrics collection service stopped")
        except Exception as e:
            logger.error(f"Unexpected error in metrics collection: {e}")
        
        logger.info("Metrics collection service finished")
    
    async def _collect_and_store_metrics(self, timestamp: int) -> None:
        """
        Collect and store metrics for a specific timestamp.
        
        Args:
            timestamp: The timestamp to collect metrics for
        """
        try:
            # Skip if Redis client is not available
            if not self._redis_client:
                logger.warning("Redis client not available, skipping metrics collection")
                return
                
            # Collect task and worker metrics
            task_metrics = await self.get_task_metrics()
            worker_metrics = await self.get_worker_metrics()
            
            system_metrics = {
                "timestamp": str(timestamp),
                "datetime": datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat(),
                "coordinator_uptime": str(timestamp - self._start_time),
                "redis_connected": "true" if self._redis_client else "false",
                "db_connected": "true" if self._db_adapter else "false",
                "instance_id": self._instance_id,
                "active_coordinators_count": str(await self._redis_client.hlen("active_coordinators")),
            }

            await self._in_memory_task_manager.update_metrics_info(
                coordinator_id=self._instance_id,
                task_metrics=task_metrics,
                worker_metrics=worker_metrics,
                system_metrics=system_metrics,
            )
            
            logger.debug(f"Metrics collected and stored for timestamp {timestamp}")
            
            # If database adapter is configured, also store in database
            if self._db_adapter and hasattr(self._db_adapter, 'save_metrics'):
                try:
                    await self._db_adapter.save_metrics(timestamp, {
                        "tasks": task_metrics,
                        "workers": worker_metrics,
                        "system": system_metrics
                    })
                except Exception as e:
                    logger.error(f"Error saving metrics to database: {e}")
                    
        except Exception as e:
            logger.error(f"Error collecting and storing metrics: {e}")