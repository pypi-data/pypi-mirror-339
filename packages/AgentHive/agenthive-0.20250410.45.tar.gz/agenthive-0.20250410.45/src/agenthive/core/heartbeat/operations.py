"""
Heartbeat operations module - contains functions for heartbeat data operations.
"""
import json
import time
import datetime
import logging
from typing import Dict, Any, Optional, List, Set, Union, Dict

import redis.asyncio as redis

from agenthive.core.heartbeat.constants import (
    REDIS_KEY_PREFIX, WORKER_HASH_KEY_FORMAT, WORKERS_SET_KEY,
    HEARTBEAT_CHANNEL, WORKER_EVENTS_CHANNEL, HeartbeatEventType
)
from agenthive.core.heartbeat.models import HeartbeatData, WorkerEvent

logger = logging.getLogger(__name__)

async def store_heartbeat(redis_client: redis.Redis, heartbeat: HeartbeatData, ttl: int = 180) -> bool:
    """
    Store heartbeat data in Redis.
    
    Args:
        redis_client: Redis client
        heartbeat: Heartbeat data to store
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        worker_id = heartbeat.worker_id
        timestamp = heartbeat.timestamp
        heartbeat_data = heartbeat.to_dict()
        
        #logger.info(f"Storing heartbeat data for worker {worker_id}: {heartbeat_data}")

        # Create a pipeline to batch Redis operations
        pipeline = redis_client.pipeline()
        
        # Update worker hash
        worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
        
        pipeline.hset(
            worker_hash_key, 
            "timestamp", 
            timestamp,
        )

        pipeline.hset(
            worker_hash_key, 
            "last_heartbeat", 
            datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
        )

        # Add ["resource_usage", "stats", "data"] as JSON
        if heartbeat.resource_usage:
            pipeline.hset(
                worker_hash_key, 
                "resource_usage", 
                json.dumps(heartbeat.resource_usage, default=str)
            )
        else:
            pipeline.hset(worker_hash_key, "resource_usage", "{}")

        if heartbeat.stats:
            pipeline.hset(
                worker_hash_key, 
                "stats", 
                json.dumps(heartbeat.stats, default=str)
            )
        else:
            pipeline.hset(worker_hash_key, "stats", "{}")
        
        pipeline.expire(worker_hash_key, ttl)
        
        # Update the active workers sorted set (score is timestamp)
        pipeline.zadd(WORKERS_SET_KEY, {worker_id: timestamp})
        
        # Publish heartbeat for metrics collection
        pipeline.publish(
            HEARTBEAT_CHANNEL, 
            json.dumps(heartbeat_data, default=str)  # Use default=str to handle non-serializable objects
        )
        
        # Execute all Redis operations
        await pipeline.execute()
        return True
        
    except Exception as e:
        logger.error(f"Error storing heartbeat data, {heartbeat}\n, exception: {e}")
        return False

async def update_worker_status(
    redis_client: redis.Redis,
    worker_id: str,
    status: str,
    inactive_since: Optional[float] = None
) -> bool:
    """
    Update worker status in Redis.
    
    Args:
        redis_client: Redis client
        worker_id: ID of the worker
        status: New status
        inactive_since: Timestamp when worker became inactive (only for inactive status)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
        
        if status == "inactive":
            # Create a pipeline to batch Redis operations
            pipeline = redis_client.pipeline()
            
            # Remove from active workers set
            pipeline.zrem(WORKERS_SET_KEY, worker_id)
            
            # Store worker data in inactive hash for history
            inactive_key = f"{REDIS_KEY_PREFIX}:inactive_worker:{worker_id}"
            
            # Get worker data
            worker_data = await redis_client.hgetall(worker_hash_key)
            if worker_data:
                # Copy data to inactive hash
                for key, value in worker_data.items():
                    pipeline.hset(inactive_key, key, value)
                
                # Add inactive timestamp
                pipeline.hset(inactive_key, "inactive_since", inactive_since or time.time())
                
                # Set expiration on inactive worker data (1 day by default)
                pipeline.expire(inactive_key, 86400)  # 24 hours
            
            # Delete active worker hash
            pipeline.delete(worker_hash_key)
            
            # Execute all Redis operations
            await pipeline.execute()
        else:
            # Simple status update for active workers
            await redis_client.hset(worker_hash_key, "status", status)
            await redis_client.hset(worker_hash_key, "last_updated", time.time())
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating worker status: {e}")
        return False

async def publish_worker_event(
    redis_client: redis.Redis,
    worker_id: str,
    event_type: str,
    event_data: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Publish a worker event to Redis.
    
    Args:
        redis_client: Redis client
        worker_id: ID of the worker
        event_type: Type of the event
        event_data: Additional event data
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create event object
        event = WorkerEvent(
            worker_id=worker_id,
            event_type=event_type,
            data=event_data,
            timestamp=event_data.get("timestamp") if event_data else None
        )
        
        # Convert to dictionary for JSON serialization
        event_dict = event.to_dict()
        
        # Publish to Redis
        await redis_client.publish(
            WORKER_EVENTS_CHANNEL,
            json.dumps(event_dict, default=str)
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Error publishing worker event: {e}")
        return False

async def get_worker_current_task(redis_client: redis.Redis, worker_id: str) -> Optional[str]:
    """
    Get the current task ID of a worker.
    
    Args:
        redis_client: Redis client
        worker_id: ID of the worker
        
    Returns:
        Optional[str]: Current task ID, or None if not found or not assigned
    """
    try:
        worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
        current_task = await redis_client.hget(worker_hash_key, "current_task")
        
        if current_task and current_task != b'':
            return current_task.decode('utf-8') if isinstance(current_task, bytes) else current_task
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting worker current task: {e}")
        return None
