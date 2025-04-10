"""
Heartbeat monitor module - used to monitor and manage worker heartbeats.
"""
import asyncio
import json
import logging
import time
import datetime
from typing import Dict, Any, Optional, List, Set, Callable, Type

import redis.asyncio as aioredis

from .constants import (
    REDIS_KEY_PREFIX, WORKER_HASH_KEY_FORMAT, WORKERS_SET_KEY,
    HEARTBEAT_CHANNEL, WORKER_EVENTS_CHANNEL, HeartbeatEventType
)
from .models import HeartbeatData, WorkerEvent
from agenthive.db.adapters.base import BaseDBAdapter as DBAdapter

# Define types for callbacks
HeartbeatCallback = Callable[[Dict[str, Any]], None]
WorkerEventCallback = Callable[[Dict[str, Any]], None]

logger = logging.getLogger(__name__)

class HeartbeatMonitor:
    """
    Heartbeat monitor - used to monitor and manage worker heartbeats.
    
    Features:
    1. Receive and process worker heartbeats
    2. Monitor worker status, detect timed-out workers
    3. Record worker events (online, offline, etc.)
    4. Provide interfaces to query worker status and history
    """
    
    def __init__(self,
                redis_url: Optional[str] = None,
                worker_timeout_seconds: int = 30,
                db_adapter: Optional[DBAdapter] = None):
        """
        Initialize a heartbeat monitor.
        
        Args:
            redis_url: Redis connection URL, used to listen for Redis pub/sub messages
            worker_timeout_seconds: Worker timeout in seconds
            db_adapter: Database adapter, used to store heartbeat data
        """
        self.redis_url = redis_url
        self.worker_timeout_seconds = worker_timeout_seconds
        self.db_adapter = db_adapter
        self._running = False
        self._redis_client = None
        self._pubsub = None
        self._monitor_task = None
        self._cleanup_task = None
        
        # Active worker heartbeat records (local cache)
        self.active_workers: Dict[str, HeartbeatData] = {}
        
        # Callbacks, called when heartbeats are received
        self._heartbeat_callbacks: List[HeartbeatCallback] = []
        self._worker_event_callbacks: List[WorkerEventCallback] = []
    
    async def start(self) -> None:
        """
        Start the heartbeat monitor.
        
        Initialize Redis connection (if Redis URL is configured) and start the monitoring task.
        """
        if self._running:
            logger.warning("Heartbeat monitor is already running")
            return
        
        self._running = True

        # Initialize Redis connection (if Redis URL is configured)
        if self.redis_url:
            retry_count = 0
            max_retries = 3
            # Try to initialize connection multiple times
            while retry_count < max_retries:
                await self._init_redis()
                if self._pubsub:
                    break
                retry_count += 1
                logger.warning(f"Redis connection attempt {retry_count}/{max_retries} failed, retrying...")
                await asyncio.sleep(1)
            
            if self._pubsub:
                # Start Redis heartbeat monitoring task
                self._monitor_task = asyncio.create_task(self._monitor_redis_heartbeats())
            else:
                logger.error(f"Could not connect to Redis ({self.redis_url}), giving up after {max_retries} retries")
        
        # Start timed-out worker cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_stale_workers())
        
        logger.info("Heartbeat monitor started")
    
    async def stop(self) -> None:
        """
        Stop the heartbeat monitor.
        
        Cancel all running tasks and close Redis connection.
        """
        if not self._running:
            logger.warning("Heartbeat monitor is not running")
            return
        
        self._running = False
        
        # Cancel monitoring task
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None
        
        # Cancel cleanup task
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
        
        # Close Redis connection
        if self._pubsub:
            await self._pubsub.unsubscribe(HEARTBEAT_CHANNEL)
            await self._pubsub.unsubscribe(WORKER_EVENTS_CHANNEL)
            await self._pubsub.close()
            self._pubsub = None
        
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None
        
        logger.info("Heartbeat monitor stopped")
    
    def register_heartbeat_callback(self, callback: HeartbeatCallback) -> None:
        """
        Register a heartbeat callback function.
        
        This callback will be called when a worker heartbeat is received.
        
        Args:
            callback: Callback function that takes heartbeat data as parameter
        """
        self._heartbeat_callbacks.append(callback)
    
    def register_worker_event_callback(self, callback: WorkerEventCallback) -> None:
        """
        Register a worker event callback function.
        
        This callback will be called when a worker event (online, offline, etc.) occurs.
        
        Args:
            callback: Callback function that takes event data as parameter
        """
        self._worker_event_callbacks.append(callback)
    
    async def process_api_heartbeat(self, heartbeat_data: Dict[str, Any]) -> None:
        """
        Process a heartbeat received via API.
        
        This method is used for heartbeats received via Coordinator API, not through Redis pub/sub.
        
        Args:
            heartbeat_data: Heartbeat data
        """
        # Make sure heartbeat data includes timestamp
        if "timestamp" not in heartbeat_data:
            heartbeat_data["timestamp"] = time.time()

        if "status" not in heartbeat_data:
            heartbeat_data["status"] = heartbeat_data.get("stats", {}).get("status", "unknown")
        
        # 确保有 resource_usage 字段
        if "resource_usage" not in heartbeat_data and "stats" in heartbeat_data:
            if "resource_usage" in heartbeat_data["stats"]:
                heartbeat_data["resource_usage"] = heartbeat_data["stats"]["resource_usage"]
        
        # Process heartbeat data
        await self._process_heartbeat(heartbeat_data)
    
    async def get_active_workers(self) -> List[Dict[str, Any]]:
        """
        Get a list of currently active workers.
        
        Returns:
            List of active workers, each containing its last heartbeat data
        """
        logger.info("Getting active workers")
        # If database adapter is configured, get from database first
        if self.db_adapter:
            try:
                return await self.db_adapter.get_active_workers(self.worker_timeout_seconds)
            except Exception as e:
                logger.error(f"Error getting active workers from database: {e}")
        
        # Get from Redis
        if self._redis_client:
            try:
                current_time = time.time()
                cutoff_time = current_time - self.worker_timeout_seconds
                
                # Get all non-timed-out workers
                worker_ids = await self._redis_client.zrangebyscore(
                    WORKERS_SET_KEY, cutoff_time, float('inf')
                )
                
                results = []
                for worker_id in worker_ids:
                    if isinstance(worker_id, bytes):
                        worker_id = worker_id.decode('utf-8')
                    
                    # Get worker data from Redis
                    worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
                    worker_data = await self._redis_client.hgetall(worker_hash_key)
                    
                    if worker_data:
                        # Convert binary data to string
                        worker_data_str = {
                            k.decode('utf-8') if isinstance(k, bytes) else k: 
                            v.decode('utf-8') if isinstance(v, bytes) else v
                            for k, v in worker_data.items()
                        }
                        
                        # Try to parse data JSON string
                        data_json = worker_data_str.get("data")
                        if data_json:
                            try:
                                heartbeat_data = json.loads(data_json)
                                results.append(heartbeat_data)
                                continue
                            except json.JSONDecodeError:
                                pass
                        
                        # Try to parse stats JSON string
                        try:
                            stats = json.loads(worker_data_str.get("stats", "{}"))
                        except json.JSONDecodeError:
                            stats = {}
                        
                        # Construct heartbeat data
                        heartbeat_data = {
                            "worker_id": worker_id,
                            "timestamp": float(worker_data_str.get("timestamp", 0)),
                            "stats": stats
                        }
                        results.append(heartbeat_data)
                
                # Update local cache
                for data in results:
                    worker_id = data.get("worker_id")
                    if worker_id:
                        self.active_workers[worker_id] = data
                
                return results
                
            except Exception as e:
                logger.error(f"Error getting active workers from Redis: {e}")
        
        # If no Redis or database, or if an error occurred, return local cache
        return list(self.active_workers.values())
    
    async def get_worker_by_id(self, worker_id: str) -> Optional[Dict[str, Any]]:
        """
        Get data for a specific worker by ID.
        
        Args:
            worker_id: Worker ID
            
        Returns:
            Worker heartbeat data, or None if worker not found
        """
        # Try to get from database
        if self.db_adapter:
            try:
                workers = await self.db_adapter.get_active_workers(self.worker_timeout_seconds)
                for worker in workers:
                    if worker.get("worker_id") == worker_id:
                        return worker
            except Exception as e:
                logger.error(f"Error getting worker data from database: {e}")
        
        # Try to get from Redis
        if self._redis_client:
            try:
                # Check if worker exists
                score = await self._redis_client.zscore(WORKERS_SET_KEY, worker_id)
                if score:
                    current_time = time.time()
                    # Check if not timed out
                    if current_time - score <= self.worker_timeout_seconds:
                        # Get worker data
                        worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
                        worker_data = await self._redis_client.hgetall(worker_hash_key)
                        
                        if worker_data:
                            # Convert binary data to string
                            worker_data_str = {
                                k.decode('utf-8') if isinstance(k, bytes) else k: 
                                v.decode('utf-8') if isinstance(v, bytes) else v
                                for k, v in worker_data.items()
                            }
                            
                            # Try to parse JSON strings
                            try:
                                stats = json.loads(worker_data_str.get("stats", "{}"))
                            except json.JSONDecodeError:
                                stats = {}
                            
                            # Construct heartbeat data
                            heartbeat_data = {
                                "worker_id": worker_id,
                                "timestamp": float(worker_data_str.get("timestamp", 0)),
                                "stats": stats
                            }
                            return heartbeat_data
            except Exception as e:
                logger.error(f"Error getting worker data from Redis: {e}")
        
        # If not found in Redis or database, use local cache
        return self.active_workers.get(worker_id)
    
    async def get_worker_history(self, worker_id: str, limit: int = 100, 
                              since: Optional[datetime.datetime] = None) -> List[Dict[str, Any]]:
        """
        Get a worker's heartbeat history.
        
        Args:
            worker_id: Worker ID
            limit: Maximum number of records to return
            since: Only return records after this time
            
        Returns:
            List[Dict[str, Any]]: Worker's heartbeat history
        """
        # Get history from database if adapter is configured
        if self.db_adapter:
            try:
                return await self.db_adapter.get_worker_history(worker_id, limit, since)
            except Exception as e:
                logger.error(f"Error getting worker history from database: {e}")
        
        # Return empty list if no database adapter
        return []
    
    async def _init_redis(self) -> None:
        """
        Initialize Redis connection and subscription.
        """
        try:
            # In Docker environment, replace localhost with redis service name
            redis_url = self.redis_url
            if redis_url and 'localhost' in redis_url:
                redis_url = redis_url.replace('localhost', 'redis')
                logger.info(f"In Docker environment, changing Redis URL from {self.redis_url} to {redis_url}")
            
            self._redis_client = await aioredis.from_url(redis_url)
            self._pubsub = self._redis_client.pubsub()
            
            # Subscribe to heartbeat and worker event channels
            await self._pubsub.subscribe(HEARTBEAT_CHANNEL)
            await self._pubsub.subscribe(WORKER_EVENTS_CHANNEL)
            
            logger.info(f"Connected to Redis ({redis_url}) and subscribed to heartbeat channels")
        except Exception as e:
            logger.error(f"Error connecting to Redis or subscribing to channels: {e}")
            if self._redis_client:
                await self._redis_client.close()
                self._redis_client = None
            # Make sure _pubsub is also None on error
            self._pubsub = None
    
    async def _monitor_redis_heartbeats(self) -> None:
        """
        Monitor Redis heartbeat channel.
        """
        if not self._pubsub:
            logger.error("Redis pubsub is not initialized, cannot monitor heartbeats")
            # Try to reinitialize connection if Redis URL is provided
            if self.redis_url:
                await self._init_redis()
                if not self._pubsub:
                    logger.critical("Could not initialize Redis pubsub, stopping heartbeat monitoring")
                    return
            else:
                return
        
        logger.info("Starting to monitor Redis heartbeat channel")
        
        try:
            while self._running:
                try:
                    message = await self._pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if message:
                        channel = message.get('channel')
                        if isinstance(channel, bytes):
                            channel = channel.decode('utf-8')
                        
                        data = message.get('data')
                        if isinstance(data, bytes):
                            data = data.decode('utf-8')
                        
                        # Parse JSON data
                        try:
                            payload = json.loads(data)
                        except json.JSONDecodeError:
                            logger.warning(f"Could not parse JSON data: {data}")
                            continue
                        
                        # Process different channel messages
                        if channel == HEARTBEAT_CHANNEL:
                            # Process heartbeat data
                            await self._process_heartbeat(payload)
                        elif channel == WORKER_EVENTS_CHANNEL:
                            # Process worker event
                            await self._process_worker_event(payload)
                
                except Exception as e:
                    # If connection is broken, try to reconnect
                    logger.error(f"Error getting Redis message: {e}")
                    await asyncio.sleep(1)
                    # Try to reinitialize connection
                    await self._init_redis()
                    if not self._pubsub:
                        logger.critical("Could not reconnect to Redis, stopping heartbeat monitoring")
                        break
                
                # Short sleep to avoid high CPU usage
                await asyncio.sleep(0.01)
        
        finally:
            logger.info("Stopped monitoring Redis heartbeat channel")
    
    async def _process_heartbeat(self, heartbeat_data: Dict[str, Any]) -> None:
        """
        Process heartbeat data.
        
        Args:
            heartbeat_data: Heartbeat data
        """
        worker_id = heartbeat_data.get("worker_id")
        if not worker_id:
            logger.warning(f"Received heartbeat without worker_id: {heartbeat_data}")
            return
        
        # Update active workers list
        was_active = worker_id in self.active_workers
        self.active_workers[worker_id] = heartbeat_data
        
        # If this is a new worker, log it
        if not was_active:
            logger.info(f"New worker joined: {worker_id}")
        
        # If database adapter is configured, store heartbeat data
        if self.db_adapter:
            try:
                await self.db_adapter.save_heartbeat(heartbeat_data)
            except Exception as e:
                logger.error(f"Error saving heartbeat data to database: {e}, data: {heartbeat_data}")
        
        # Call all heartbeat callbacks
        for callback in self._heartbeat_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(heartbeat_data)  # Await async callback
                else:
                    callback(heartbeat_data)  # Call sync callback
            except Exception as e:
                logger.error(f"Error in heartbeat callback: {e}")
    
    async def _process_worker_event(self, event_data: Dict[str, Any]) -> None:
        """
        Process worker event.
        
        Args:
            event_data: Event data
        """
        event_type = event_data.get("event")
        worker_id = event_data.get("worker_id")
        
        if not worker_id:
            logger.warning(f"Received event without worker_id: {event_data}")
            return
        
        # Process by event type
        if event_type == HeartbeatEventType.WORKER_OFFLINE:
            # Worker offline
            if worker_id in self.active_workers:
                del self.active_workers[worker_id]
                logger.info(f"Worker offline: {worker_id}")
        
        # If database adapter is configured, store event data
        if self.db_adapter:
            try:
                await self.db_adapter.save_worker_event(event_data)
            except Exception as e:
                logger.error(f"Error saving worker event to database: {e}")
        
        # Call all worker event callbacks
        for callback in self._worker_event_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event_data)  # Await async callback
                else:
                    callback(event_data)  # Call sync callback
            except Exception as e:
                logger.error(f"Error in worker event callback: {e}")
    
    async def _cleanup_stale_workers(self) -> None:
        """
        Periodically clean up timed-out workers.
        Remove workers that haven't sent heartbeats for a while from the active workers list.
        """
        logger.info("Starting to monitor worker timeouts")
        
        while self._running:
            try:
                current_time = time.time()
                current_datetime = datetime.datetime.fromtimestamp(current_time, tz=datetime.timezone.utc)
                
                stale_workers = []
                
                # Check workers in local cache
                for worker_id, heartbeat_data in list(self.active_workers.items()):
                    timestamp = heartbeat_data.get("timestamp", 0)

                    # Ensure timestamp is a datetime object
                    if isinstance(timestamp, (int, float)):  # If it's a Unix timestamp
                        timestamp_datetime = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
                    elif isinstance(timestamp, datetime.datetime):  # Already a datetime
                        timestamp_datetime = timestamp
                    else:  # Fallback for invalid types
                        timestamp_datetime = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)

                    # Convert both to seconds for comparison
                    time_diff = (current_datetime - timestamp_datetime).total_seconds()

                    if time_diff > self.worker_timeout_seconds:
                        # Worker timed out
                        stale_workers.append(worker_id)
                        # Remove from local cache
                        self.active_workers.pop(worker_id, None)
                        
                        # Create offline event
                        offline_event = {
                            "event": HeartbeatEventType.WORKER_OFFLINE,
                            "worker_id": worker_id,
                            "timestamp": current_time,
                            "reason": "timeout"
                        }
                        
                        # Call worker event callbacks
                        for callback in self._worker_event_callbacks:
                            try:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(offline_event)  # Await async callback
                                else:
                                    callback(offline_event)  # Call sync callback
                            except Exception as e:
                                logger.error(f"Error in worker event callback: {e}")
                        
                        # Store worker offline event to database
                        if self.db_adapter:
                            try:
                                await self.db_adapter.save_worker_event(offline_event)
                                # Optionally update worker status in database
                                if hasattr(self.db_adapter, 'update_worker_status'):
                                    await self.db_adapter.update_worker_status(worker_id, "offline", current_time)
                            except Exception as e:
                                logger.error(f"Error updating worker status in database: {e}")
                
                # If using Redis, also clean up timed-out workers in Redis
                if self._redis_client:
                    try:
                        # Get all workers and their heartbeat times
                        worker_scores = await self._redis_client.zrange(
                            WORKERS_SET_KEY, 0, -1, withscores=True
                        )
                        
                        # Check timed-out workers
                        for worker_item in worker_scores:
                            worker_id = worker_item[0]
                            if isinstance(worker_id, bytes):
                                worker_id = worker_id.decode('utf-8')
                            timestamp = worker_item[1]

                            # Ensure timestamp is a datetime object
                            if isinstance(timestamp, (int, float)):  # If it's a Unix timestamp
                                timestamp_datetime = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
                            elif isinstance(timestamp, datetime.datetime):  # Already a datetime
                                timestamp_datetime = timestamp
                            else:  # Fallback for invalid types
                                timestamp_datetime = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)

                            # Convert both to seconds for comparison
                            time_diff = (current_datetime - timestamp_datetime).total_seconds()

                            if time_diff > self.worker_timeout_seconds:
                                # Delete worker related data
                                worker_hash_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
                                await self._redis_client.delete(worker_hash_key)
                                await self._redis_client.zrem(WORKERS_SET_KEY, worker_id)
                                
                                # Publish offline event
                                offline_event = {
                                    "event": HeartbeatEventType.WORKER_OFFLINE,
                                    "worker_id": worker_id,
                                    "timestamp": current_time,
                                    "reason": "timeout"
                                }
                                await self._redis_client.publish(
                                    WORKER_EVENTS_CHANNEL, 
                                    json.dumps(offline_event)
                                )
                                
                                # Store worker offline event to database for Redis-detected timeouts
                                if self.db_adapter and worker_id not in stale_workers:
                                    try:
                                        await self.db_adapter.save_worker_event(offline_event)
                                        # Optionally update worker status in database
                                        if hasattr(self.db_adapter, 'update_worker_status') and callable(self.db_adapter.update_worker_status):
                                            await self.db_adapter.update_worker_status(worker_id, "offline", current_time)
                                    except Exception as e:
                                        logger.error(f"Error updating Redis-detected worker status in database: {e}")
                                
                                if worker_id not in stale_workers:
                                    stale_workers.append(worker_id)
                                    logger.info(f"Detected timed-out worker in Redis: {worker_id}")
                    
                    except Exception as e:
                        logger.error(f"Error cleaning up timed-out workers in Redis: {e}")
                
                # Log timed-out workers
                if stale_workers:
                    logger.warning(f"Detected {len(stale_workers)} timed-out workers: {', '.join(stale_workers)}")
                
                # Check every 5 seconds
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error cleaning up timed-out workers: {e}")
                await asyncio.sleep(5)
        
        logger.info("Stopped monitoring worker timeouts")
