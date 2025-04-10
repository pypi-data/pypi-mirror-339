"""
Enhanced Coordinator implementation for AgentHive.
"""
import os
import time
import json
import uuid
import logging
import asyncio
from typing import Dict, Any, Optional, List, Type, Set, Tuple, Callable

import redis.asyncio as redis

from agenthive.core.task import Task
from agenthive.core.coordinator import Coordinator

# Try to import the TaskRegistry
try:
    from agenthive.core.registry import TaskRegistry
except ImportError:
    # If registry module doesn't exist yet, use a simple TaskRegistry implementation
    class TaskRegistry:
        _registry = {}
        
        @classmethod
        def is_task_supported(cls, task_type: str) -> bool:
            return task_type in ["not found"]

logger = logging.getLogger(__name__)


class EnhancedCoordinator:
    """
    Enhanced Coordinator class with improved task management.
    
    This class extends the functionality of the base Coordinator class
    with additional methods for task management and worker coordination.
    It uses the adapter pattern to delegate most operations to the underlying
    Coordinator instance.
    """
    
    def __init__(self, coordinator: Coordinator):
        """
        Initialize the EnhancedCoordinator with a base Coordinator instance.
        
        Args:
            coordinator: The base Coordinator instance
        """
        self.coordinator = coordinator
        self.task_registry = {}  # task_id -> task_info mapping
    
    async def validate_task_type(self, task_type: str) -> bool:
        """
        Validate if a task type is supported.
        
        Args:
            task_type: The task type to validate
            
        Returns:
            bool: True if the task type is supported, False otherwise
        """
        return TaskRegistry.is_task_supported(task_type)
    
    async def create_task(self, task_type: str, task_data: Dict[str, Any], priority: int = 0) -> str:
        """
        Create a new task.
        
        Args:
            task_type: The type of the task
            task_data: The task data
            priority: The priority of the task
            
        Returns:
            str: The task ID
            
        Raises:
            ValueError: If the task type is not supported
        """

        # Validate task type
        if not await self.validate_task_type(task_type):
            logger.error(f"validate_task_type: {task_type} failed")
            raise ValueError(f"Unsupported task type: {task_type}")
        
        # Create task based on type
        task_id = str(uuid.uuid4())
        
        # Create a generic task
        from agenthive.core.task import Task
        task = None

        try:
            task = Task(
                task_id=task_id,
                task_type=task_type,
                data=task_data,
                priority=priority
            )
        except Exception as e:
            logger.error(f"Error creating task: {e}")
        
        # Submit task to coordinator
        await self.coordinator.submit_task(task)

        # Store in local registry
        self.task_registry[task_id] = {
            "task_type": task_type,
            "data": task_data,
            "priority": priority,
            "created_at": time.time(),
            "status": "pending"
        }
        
        return task_id
    
    async def find_suitable_worker(self, task_type: str) -> Optional[str]:
        """
        Find a suitable worker for a task type.
        
        Args:
            task_type: The task type
            
        Returns:
            Optional[str]: Worker ID if found, None otherwise
        """
        try:
            # Get active workers
            active_workers = await self.coordinator.get_active_workers()
            
            # Find suitable workers (idle and with the right capability)
            suitable_workers = []
            for worker in active_workers:
                worker_id = worker.get("worker_id")
                capabilities = worker.get("capabilities", [])
                status = worker.get("status", worker.get("stats", {}).get("status", "unknown"))
                
                if task_type in capabilities and status == "idle":
                    suitable_workers.append(worker_id)
            
            # Return a suitable worker if found
            if suitable_workers:
                # Simple round-robin for now, could implement more sophisticated selection
                return suitable_workers[0]
            
            return None
        except Exception as e:
            logger.error(f"Error finding suitable worker: {e}")
            return None
    
    async def get_tasks(self, 
                       status: Optional[str] = None, 
                       limit: int = 100,
                       task_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get tasks by status and/or type.
        
        Args:
            status: Filter by status (pending, assigned, completed, failed)
            limit: Maximum number of tasks to return
            task_type: Filter by task type
            
        Returns:
            List[Dict[str, Any]]: List of task information
        """
        # Get tasks from Redis or database 
        try:
            tasks = []
            
            # See if coordinator has a get_tasks method
            if hasattr(self.coordinator, 'get_tasks'):
                tasks = await self.coordinator.get_tasks(status=status, limit=limit, include_details=True)
            # Otherwise try to use the Redis client directly
            elif self.coordinator._redis_client:
                redis_client = self.coordinator._redis_client
                # Get tasks based on status
                if status == "pending" or status is None:
                    pending_ids = await redis_client.zrevrange("tasks:pending", 0, limit-1)
                    for task_id_bytes in pending_ids:
                        task_id = task_id_bytes.decode('utf-8')
                        task_data = await redis_client.hgetall(f"task:{task_id}")
                        if task_data:
                            # Convert to dictionary
                            task_dict = {k.decode('utf-8'): self._try_decode_json(v) 
                                      for k, v in task_data.items()}
                            task_dict["task_id"] = task_id
                            task_dict["status"] = "pending"
                            tasks.append(task_dict)
                
                if status == "completed" or status is None:
                    completed_ids = await redis_client.zrevrange("tasks:completed", 0, limit-1)
                    for task_id_bytes in completed_ids:
                        task_id = task_id_bytes.decode('utf-8')
                        task_data = await redis_client.hgetall(f"task:{task_id}")
                        if task_data:
                            # Convert to dictionary
                            task_dict = {k.decode('utf-8'): self._try_decode_json(v) 
                                      for k, v in task_data.items()}
                            task_dict["task_id"] = task_id
                            task_dict["status"] = "completed"
                            tasks.append(task_dict)
                
                if status == "failed" or status is None:
                    failed_ids = await redis_client.zrevrange("tasks:failed", 0, limit-1)
                    for task_id_bytes in failed_ids:
                        task_id = task_id_bytes.decode('utf-8')
                        task_data = await redis_client.hgetall(f"task:{task_id}")
                        if task_data:
                            # Convert to dictionary
                            task_dict = {k.decode('utf-8'): self._try_decode_json(v) 
                                      for k, v in task_data.items()}
                            task_dict["task_id"] = task_id
                            task_dict["status"] = "failed"
                            tasks.append(task_dict)
            
            # Filter by task_type if specified
            if task_type:
                tasks = [t for t in tasks if t.get("task_type") == task_type]
            
            return tasks[:limit]
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            return []
    
    def _try_decode_json(self, value):
        """Helper method to try decoding JSON values."""
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Dict[str, Any]: Task status information
        """
        return await self.coordinator.get_task_status(task_id)
    
    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a pending task.
        
        Args:
            task_id: ID of the task to cancel
            
        Returns:
            bool: True if task was cancelled, False otherwise
        """
        # Not fully implemented yet, as it depends on the base coordinator implementation
        # This is a placeholder
        task_status = await self.get_task_status(task_id)
        
        if task_status.get("status") == "pending":
            # Mark as cancelled in local registry
            if task_id in self.task_registry:
                self.task_registry[task_id]["status"] = "cancelled"
            
            # If coordinator has cancellation support
            if hasattr(self.coordinator, 'cancel_task'):
                return await self.coordinator.cancel_task(task_id)
            
            # Fallback: try to remove from pending queue
            elif self.coordinator._redis_client:
                try:
                    # Remove from pending queue
                    await self.coordinator._redis_client.zrem("tasks:pending", task_id)
                    # Add to cancelled set
                    await self.coordinator._redis_client.zadd(
                        "tasks:cancelled", 
                        {task_id: time.time()}
                    )
                    # Update task status
                    await self.coordinator._redis_client.hset(
                        f"task:{task_id}", 
                        "status", 
                        "cancelled"
                    )
                    return True
                except Exception as e:
                    logger.error(f"Error cancelling task: {e}")
                    return False
            
            return True
        
        return False
