"""
Heartbeat sender module - provides functionality for Workers to send heartbeats.
"""
import os
import time
import datetime
import json
import asyncio
import logging
import aiohttp
from typing import Optional, Dict, Any, Union, Callable

import redis.asyncio as aioredis
from ...utils.health import get_system_metrics

from .constants import (
    HeartbeatStrategy, HeartbeatEventType,
)
from .models import HeartbeatData
from .operations import store_heartbeat, publish_worker_event

# Define a type for the stats provider function
StatsProvider = Callable[[], Dict[str, Any]]

logger = logging.getLogger(__name__)

class HeartbeatSender:
    """
    Heartbeat sender - used for workers to send heartbeat signals.
    
    Depending on the configured strategy, can send heartbeats via different methods:
    - NONE: Don't send any heartbeats
    - STDOUT: Only output to standard output
    - REDIS: Send to Redis publish/subscribe system
    - COORDINATOR_API: Send via API call to coordinator
    """
    
    def __init__(self,
                 worker_id: str,
                 heartbeat_interval: int = 10,
                 redis_url: Optional[str] = None,
                 coordinator_url: Optional[str] = None,
                 strategy: Union[str, HeartbeatStrategy] = HeartbeatStrategy.STDOUT):
        """
        Initialize a heartbeat sender.
        
        Args:
            worker_id: Worker unique identifier
            heartbeat_interval: Heartbeat interval (in seconds)
            redis_url: Redis connection URL, if using Redis strategy
            coordinator_url: Coordinator API URL, if using API strategy
            strategy: Heartbeat sending strategy
        """
        self.worker_id = worker_id
        self.heartbeat_interval = heartbeat_interval
        self.redis_url = redis_url
        self.coordinator_url = coordinator_url
        
        # Ensure strategy is a HeartbeatStrategy enum
        if isinstance(strategy, str):
            self.strategy = HeartbeatStrategy.from_string(strategy)
        else:
            self.strategy = strategy
        
        self._task = None
        self._running = False
        self._redis_client = None
        self._stats_provider = None
        self._start_time = time.time()
        
    async def start(self, stats_provider: Optional[StatsProvider] = None) -> None:
        """
        Start sending heartbeats.
        
        Args:
            stats_provider: Function that provides worker status, called for each heartbeat
        """
        if self._running:
            logger.warning(f"Heartbeat sender is already running, strategy: {self.strategy}")
            return
        
        self._stats_provider = stats_provider
        self._running = True

        logger.info(f"Starting worker {self.worker_id} heartbeat sender, strategy: {self.strategy}")
        
        # Initialize connection based on strategy
        if self.strategy == HeartbeatStrategy.REDIS:
            if not self.redis_url:
                logger.error("Using Redis strategy but no Redis URL provided, falling back to STDOUT strategy")
                self.strategy = HeartbeatStrategy.STDOUT
            else:
                try:
                    redis_url = self.redis_url
                    if redis_url and 'localhost' in redis_url:
                        redis_url = redis_url.replace('localhost', 'redis')
                        logger.info(f"In Docker environment, changing Redis URL from {self.redis_url} to {redis_url}")
                    self._redis_client = await aioredis.from_url(redis_url)
                    logger.info(f"Successfully connected to Redis: {self.redis_url}")
                except Exception as e:
                    logger.error(f"Error connecting to Redis: {e}, falling back to STDOUT strategy")
                    self.strategy = HeartbeatStrategy.STDOUT
        
        # 
        # worker registration with coordinator api will be done in the coordinator
        # 
        # Send initial heartbeat with "idle" status
        #initial_heartbeat = self._prepare_data()
        #initial_heartbeat["stats"]["status"] = "idle"
        #await self._send_heartbeat_data(HeartbeatData.from_dict(initial_heartbeat))
        #logger.info(f"Sent initial heartbeat for worker: {self.worker_id}")
        
        # Send online event
        await self._send_event(HeartbeatEventType.WORKER_ONLINE)
        logger.info(f"Worker {self.worker_id} is online, starting to send heartbeats")
        
        # Start heartbeat task
        self._task = asyncio.create_task(self._heartbeat_loop())

    async def stop(self) -> None:
        """Stop sending heartbeats."""
        if not self._running:
            return
        
        self._running = False
        
        # Send offline event
        try:
            await self._send_event(HeartbeatEventType.WORKER_OFFLINE)
        except Exception as e:
            logger.error(f"Error sending offline event: {e}")
        
        # Cancel heartbeat task
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        # Close Redis connection
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None
        
        logger.info(f"Worker {self.worker_id} stopped sending heartbeats")
        
    async def _heartbeat_loop(self) -> None:
        """Heartbeat sending loop."""
        try:
            while self._running:
                try:
                    # Send heartbeat
                    await self._send_heartbeat()
                    
                    # Wait until next heartbeat time
                    await asyncio.sleep(self.heartbeat_interval)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error sending heartbeat: {e}")
                    # Pause briefly to avoid rapid failure
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            # Task was cancelled
            pass

    async def _send_heartbeat_data(self, data: HeartbeatData) -> None:
        """Send heartbeat data"""

        logger.debug(f"Sending heartbeat, strategy: {self.strategy}, object: {data.to_dict()}")
        
        # Send heartbeat based on strategy
        if self.strategy == HeartbeatStrategy.NONE:
            # Don't send heartbeat
            return
        
        elif self.strategy == HeartbeatStrategy.STDOUT:
            # Only output to standard output
            logger.info(f"Heartbeat:\n{json.dumps(data.to_dict(), indent=2)}")
        
        elif self.strategy == HeartbeatStrategy.REDIS:
            # Send to Redis using operations module
            if not self._redis_client:
                logger.error("Redis client is not initialized, cannot send heartbeat")
                return
            
            try:
                # Use operations module to store heartbeat
                await store_heartbeat(self._redis_client, data)
            except Exception as e:
                logger.error(f"Error sending heartbeat to Redis: {e}")
        
        elif self.strategy == HeartbeatStrategy.COORDINATOR_API:
            # Send via API to coordinator
            if not self.coordinator_url:
                logger.error("No coordinator URL provided, cannot send heartbeat")
                return
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.coordinator_url.rstrip('/')}/api/workers/heartbeat"
                    async with session.post(url, json=data.to_dict()) as resp:
                        if resp.status != 200:
                            text = await resp.text()
                            logger.error(f"Error sending heartbeat to coordinator: {resp.status} - {text}")
            except Exception as e:
                logger.error(f"Error sending heartbeat to coordinator: {e}")
        
    async def _send_heartbeat(self) -> None:
        """Send one heartbeat."""

        await self._send_heartbeat_data(HeartbeatData.from_dict(self._prepare_data(event_type=HeartbeatEventType.HEARTBEAT)))
    
    async def _send_event(self, event_type: HeartbeatEventType) -> None:
        """
        Send a worker event.
        
        Args:
            event_type: Event type
        """
        # Prepare event data
        event_data = self._prepare_data(event_type=event_type)
        
        # Send event based on strategy
        if self.strategy == HeartbeatStrategy.NONE:
            # Don't send event
            return
        
        elif self.strategy == HeartbeatStrategy.STDOUT:
            # Only output to standard output
            logger.info(f"Event: {json.dumps(event_data)}")
        
        elif self.strategy == HeartbeatStrategy.REDIS:
            # Send to Redis using operations module
            if not self._redis_client:
                logger.error("Redis client is not initialized, cannot send event")
                return
            
            try:
                # Use operations module to publish event
                await publish_worker_event(
                    redis_client=self._redis_client,
                    worker_id=self.worker_id,
                    event_type=event_type,
                    event_data=event_data
                )
            except Exception as e:
                logger.error(f"Error sending event to Redis: {e}")
        
        elif self.strategy == HeartbeatStrategy.COORDINATOR_API:
            # Send via API to coordinator
            if not self.coordinator_url:
                logger.error("No coordinator URL provided, cannot send event")
                return
            
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.coordinator_url.rstrip('/')}/api/workers/event"
                    async with session.post(url, json=event_data) as resp:
                        if resp.status != 200:
                            text = await resp.text()
                            logger.error(f"Error sending event to coordinator: {resp.status} - {text}")
            except Exception as e:
                logger.error(f"Error sending event to coordinator: {e}")
    
    def _prepare_data(self, event_type: HeartbeatEventType = HeartbeatEventType.HEARTBEAT) -> Dict[str, Any]:
        """Prepare heartbeat data."""
        current_time = time.time()
        uptime = current_time - self._start_time
        
        # Basic heartbeat data
        data = {
            "event": event_type,
            "worker_id": self.worker_id,
            "timestamp": current_time,
            "stats": {},
            "resource_usage": {},
        }

        # Include stats if stats provider is available
        if self._stats_provider:
            try:
                info = self._stats_provider()
                if info:
                    if "stats" in info:
                        data["stats"] = info["stats"]
                    if "resource_usage" in info:
                        data["resource_usage"] = info["resource_usage"]
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                data["stats"]["error"] = "call stats_provider exception: "+str(e)

            if 'uptime' not in data["stats"]:
                data["stats"]["uptime"] = uptime
        else:
            data["stats"] = {
                #"status": "unknown",
                "uptime": uptime,
            }
            data["resource_usage"] = get_system_metrics()

        return data
