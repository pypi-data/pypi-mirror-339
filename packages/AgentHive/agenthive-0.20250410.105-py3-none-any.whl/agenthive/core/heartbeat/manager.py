"""
Heartbeat manager for py-AgentHive.

This module provides a manager for handling worker heartbeats, tracking worker status,
and detecting inactive workers. It uses the heartbeat operations module for the actual
Redis interactions.
"""
import json
import time
import asyncio
import logging
from typing import Dict, Any, Optional, List, Callable, Set, Union

import redis.asyncio as redis

from agenthive.core.heartbeat.constants import (
    REDIS_KEY_PREFIX, WORKER_HASH_KEY_FORMAT, WORKERS_SET_KEY,
    HEARTBEAT_CHANNEL, WORKER_EVENTS_CHANNEL, HeartbeatEventType
)
from agenthive.core.heartbeat.models import HeartbeatData
from agenthive.core.heartbeat.operations import (
    store_heartbeat, update_worker_status, publish_worker_event,
    get_worker_current_task
)

logger = logging.getLogger(__name__)


class HeartbeatManager:
    """
    Manager for worker heartbeats.
    
    This class is responsible for:
    - Processing worker heartbeats
    - Tracking worker status
    - Detecting inactive workers
    - Publishing heartbeat metrics
    
    It follows the adapter pattern, similar to the database adapters,
    by using the heartbeat operations module for the actual Redis interactions.
    """
    
    def __init__(self, 
                 redis_client: redis.Redis,
                 worker_timeout: int = 60,
                 metrics_enabled: bool = True):
        """
        Initialize a new HeartbeatManager.
        
        Args:
            redis_client: Redis client for heartbeat storage and pubsub
            worker_timeout: Timeout in seconds for worker heartbeats
            metrics_enabled: Whether to collect and store metrics
        """
        self.redis_client = redis_client
        self.worker_timeout = worker_timeout
        self.metrics_enabled = metrics_enabled
        
        # Local cache and state
        self._worker_registry = {}  # Local cache of worker info
        self._running = False
        self._pubsub = None
        self._monitor_task = None
        
        # Callbacks
        self._on_worker_active_callbacks: Set[Callable[[str, Dict[str, Any]], None]] = set()
        self._on_worker_inactive_callbacks: Set[Callable[[str, Optional[str]], None]] = set()
    
    async def initialize(self) -> None:
        """
        Initialize the heartbeat manager.
        
        This sets up pubsub if metrics are enabled and marks the manager as running.
        """
        logger.info("Initializing heartbeat manager")
        
        if self.metrics_enabled:
            # Set up pubsub for worker heartbeats
            self._pubsub = self.redis_client.pubsub()
            await self._pubsub.subscribe(HEARTBEAT_CHANNEL)
        
        self._running = True
        logger.info("Heartbeat manager initialized")
    
    async def process_heartbeat(self, heartbeat: HeartbeatData) -> bool:
        """
        Process a worker heartbeat.
        
        Args:
            heartbeat: Heartbeat data
            
        Returns:
            bool: True if the heartbeat was processed successfully, False otherwise
        """
        worker_id = heartbeat.worker_id
        logger.debug(f"Processing heartbeat from worker {worker_id}")
        
        try:
            # Store heartbeat data using operations module
            success = await store_heartbeat(
                redis_client=self.redis_client,
                heartbeat=heartbeat
            )
            
            if not success:
                logger.error(f"Failed to store heartbeat data for worker {worker_id}")
                return False
            
            # Update in-memory worker registry
            self._worker_registry[worker_id] = heartbeat.to_dict()
            
            # Trigger callbacks for active workers
            for callback in self._on_worker_active_callbacks:
                try:
                    callback(worker_id, heartbeat.to_dict())
                except Exception as e:
                    logger.error(f"Error in worker active callback: {e}")
            
            logger.debug(f"Heartbeat from worker {worker_id}: status={heartbeat.status}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing heartbeat: {e}")
            return False
    
    async def start_monitoring(self) -> None:
        """
        Start monitoring worker heartbeats.
        
        This initializes the manager if needed and starts a background task
        to monitor worker timeouts.
        """
        if not self._running:
            await self.initialize()
        
        # Start monitoring task
        self._monitor_task = asyncio.create_task(self._monitor_workers())
        
        logger.info("Heartbeat monitoring started")
    
    async def stop_monitoring(self) -> None:
        """
        Stop monitoring worker heartbeats.
        
        This cancels the monitoring task and closes pubsub connections if active.
        """
        self._running = False
        
        # Cancel monitoring task
        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        
        # Close pubsub if active
        if self._pubsub:
            await self._pubsub.unsubscribe(HEARTBEAT_CHANNEL)
            self._pubsub = None
        
        logger.info("Heartbeat monitoring stopped")
    
    async def _monitor_workers(self) -> None:
        """
        Monitor worker heartbeats and identify inactive workers.
        
        This is an internal method that runs as a background task to periodically
        check for timed-out workers.
        """
        logger.info("Starting worker monitoring task")
        
        while self._running:
            try:
                current_time = time.time()
                workers_to_remove = []
                
                # Check for timed out workers
                cutoff_time = current_time - self.worker_timeout
                
                # Get all workers and their last heartbeat times
                try:
                    # Get all workers with scores (heartbeat times)
                    worker_scores = await self.redis_client.zrangebyscore(
                        WORKERS_SET_KEY, 
                        0,  # Min score (from beginning of time)
                        '+inf',  # Max score (to now)
                        withscores=True
                    )
                    
                    # Check for timed out workers
                    for worker_item in worker_scores:
                        worker_id = worker_item[0]
                        timestamp = worker_item[1]
                        
                        # Decode worker_id if it's bytes
                        if isinstance(worker_id, bytes):
                            worker_id = worker_id.decode('utf-8')
                        
                        # Check if worker has timed out
                        if timestamp < cutoff_time:
                            # Add to removal list
                            workers_to_remove.append(worker_id)
                
                except Exception as e:
                    logger.error(f"Error checking worker timeouts in Redis: {e}")
                
                # Process inactive workers
                for worker_id in workers_to_remove:
                    await self._handle_worker_timeout(worker_id, current_time)
                
                # Wait before next check
                await asyncio.sleep(self.worker_timeout / 2)
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in worker monitoring: {e}")
                await asyncio.sleep(10)
    
    async def _handle_worker_timeout(self, worker_id: str, current_time: float) -> None:
        """
        Handle worker timeout - mark worker as inactive and notify callbacks.
        
        Args:
            worker_id: ID of the worker that timed out
            current_time: Current timestamp
        """
        logger.warning(f"Worker {worker_id} timed out, marking as inactive")
        
        # Get current task
        current_task_id = await get_worker_current_task(self.redis_client, worker_id)
        
        # Publish worker offline event using operations module
        await publish_worker_event(
            redis_client=self.redis_client,
            worker_id=worker_id,
            event_type=HeartbeatEventType.WORKER_OFFLINE,
            event_data={"reason": "timeout", "timestamp": current_time}
        )
        
        # Update worker status to inactive using operations module
        await update_worker_status(
            redis_client=self.redis_client,
            worker_id=worker_id,
            status="inactive", 
            inactive_since=current_time
        )
        
        # Remove from local registry
        self._worker_registry.pop(worker_id, None)
        
        # Trigger callbacks for inactive workers
        for callback in self._on_worker_inactive_callbacks:
            try:
                callback(worker_id, current_task_id)
            except Exception as e:
                logger.error(f"Error in worker inactive callback: {e}")
    
    def on_worker_active(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Register a callback for when a worker is active.
        
        Args:
            callback: Function to call when worker is active
        """
        self._on_worker_active_callbacks.add(callback)
    
    def on_worker_inactive(self, callback: Callable[[str, Optional[str]], None]) -> None:
        """
        Register a callback for when a worker becomes inactive.
        
        Args:
            callback: Function to call when worker becomes inactive
        """
        self._on_worker_inactive_callbacks.add(callback)
    
    def remove_worker_active_callback(self, callback: Callable) -> None:
        """
        Remove a worker active callback.
        
        Args:
            callback: Callback to remove
        """
        self._on_worker_active_callbacks.discard(callback)
    
    def remove_worker_inactive_callback(self, callback: Callable) -> None:
        """
        Remove a worker inactive callback.
        
        Args:
            callback: Callback to remove
        """
        self._on_worker_inactive_callbacks.discard(callback)
    
    async def get_worker_info(self, worker_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific worker.
        
        Args:
            worker_id: ID of the worker
            
        Returns:
            Optional[Dict[str, Any]]: Worker information, or None if not found
        """
        # Check local cache first
        if worker_id in self._worker_registry:
            return self._worker_registry[worker_id]
        
        # Try to get from Redis
        try:
            worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
            data = await self.redis_client.hget(worker_hash_key, "data")
            
            if data:
                try:
                    worker_data = json.loads(data.decode('utf-8') if isinstance(data, bytes) else data)
                    return worker_data
                except json.JSONDecodeError:
                    pass
            
            # If no serialized data, try to build from individual fields
            worker_data = await self.redis_client.hgetall(worker_hash_key)
            if worker_data:
                result = {}
                for key, value in worker_data.items():
                    # Decode key and value if they're bytes
                    key = key.decode('utf-8') if isinstance(key, bytes) else key
                    value = value.decode('utf-8') if isinstance(value, bytes) else value
                    
                    # Try to parse JSON values
                    try:
                        result[key] = json.loads(value)
                    except (json.JSONDecodeError, TypeError):
                        result[key] = value
                
                return result
        except Exception as e:
            logger.error(f"Error getting worker info from Redis: {e}")
        
        return None
    
    async def get_all_workers(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Get information about all workers.
        
        Args:
            include_inactive: Whether to include inactive workers
            
        Returns:
            List[Dict[str, Any]]: List of worker information
        """
        result = []
        
        try:
            # Get all active workers first
            worker_ids = await self.redis_client.zrange(WORKERS_SET_KEY, 0, -1)
            
            for worker_id_bytes in worker_ids:
                worker_id = worker_id_bytes.decode('utf-8') if isinstance(worker_id_bytes, bytes) else worker_id_bytes
                worker_info = await self.get_worker_info(worker_id)
                
                if worker_info:
                    result.append(worker_info)
            
            # Include inactive workers if requested
            if include_inactive:
                # Pattern to match inactive worker keys
                inactive_pattern = f"{REDIS_KEY_PREFIX}:inactive_worker:*"
                
                # Get all inactive worker keys
                inactive_keys = await self.redis_client.keys(inactive_pattern)
                
                for key_bytes in inactive_keys:
                    key = key_bytes.decode('utf-8') if isinstance(key_bytes, bytes) else key_bytes
                    
                    # Extract worker ID from key
                    worker_id = key.split(':')[-1]
                    
                    # Get worker data
                    worker_data = await self.redis_client.hgetall(key)
                    
                    if worker_data:
                        worker_info = {}
                        for field, value in worker_data.items():
                            # Decode field and value if they're bytes
                            field = field.decode('utf-8') if isinstance(field, bytes) else field
                            value = value.decode('utf-8') if isinstance(value, bytes) else value
                            
                            # Try to parse JSON values
                            try:
                                worker_info[field] = json.loads(value)
                            except (json.JSONDecodeError, TypeError):
                                worker_info[field] = value
                        
                        # Add flag indicating this is an inactive worker
                        worker_info["active"] = False
                        
                        result.append(worker_info)
        
        except Exception as e:
            logger.error(f"Error getting all workers: {e}")
            
            # Fall back to local registry
            result = list(self._worker_registry.values())
        
        return result
