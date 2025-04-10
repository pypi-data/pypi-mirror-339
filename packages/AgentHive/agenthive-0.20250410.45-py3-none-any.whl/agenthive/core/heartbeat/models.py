"""
Data models for the heartbeat system.
"""
import time
import json
import logging
from typing import Dict, Any, Optional, Union, List

logger = logging.getLogger(__name__)

class HeartbeatData:
    """
    Container for worker heartbeat data.
    """
    
    def __init__(self, 
                 worker_id: str,
                 status: str,
                 current_task: Optional[str] = None,
                 resource_usage: Optional[Dict[str, Any]] = None,
                 stats: Optional[Dict[str, Any]] = None,
                 timestamp: Optional[float] = None):
        """
        Initialize a new HeartbeatData object.
        
        Args:
            worker_id: ID of the worker
            status: Current status of the worker
            current_task: ID of the task currently being processed (if any)
            resource_usage: System resource usage metrics
            stats: Worker statistics
            timestamp: Timestamp of the heartbeat (if None, current time is used)
        """
        self.worker_id = worker_id
        self.status = status
        self.current_task = current_task
        self.resource_usage = resource_usage or {}
        self.stats = stats or {}
        self.timestamp = timestamp or time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the heartbeat data to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the heartbeat data
        """
        return {
            "worker_id": self.worker_id,
            "status": self.status,
            "current_task": self.current_task,
            "resource_usage": self.resource_usage,
            "stats": self.stats,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HeartbeatData':
        """
        Create a HeartbeatData object from a dictionary.
        
        Args:
            data: Dictionary containing heartbeat data
            
        Returns:
            HeartbeatData: New HeartbeatData object
        """

        #logger.info(f"HeartbeatData.from_dict: {data}")

        input_stats = {}
        input_resource_data = {}
        input_current_task = None
        input_status = 'unknown'

        if 'stats' in data:
            input_stats = data['stats']
            if isinstance(input_stats, str):
                try:
                    input_stats = json.loads(input_stats)
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode stats JSON: {input_stats}")
                    input_stats = {}

        if 'resource_usage' in data:
            input_resource_data = data['resource_usage']
            if isinstance(input_resource_data, str):
                try:
                    input_resource_data = json.loads(input_resource_data)
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode resource_usage JSON: {input_resource_data}")
                    input_resource_data = {}
        elif 'resource_usage' in input_stats:
            input_resource_data = input_stats['resource_usage']
            if isinstance(input_resource_data, str):
                try:
                    input_resource_data = json.loads(input_resource_data)
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode resource_usage JSON: {input_resource_data}")
                    input_resource_data = {}

        if 'current_task' in data:
            input_current_task = data['current_task']
        elif 'current_task' in input_stats:
            input_current_task = input_stats['current_task']

        if 'status' in data:
            input_status = data['status']
        elif 'status' in input_stats:
            input_status = input_stats['status']

        #logger.info(f"HeartbeatData.from_dict: worker_id={data.get('worker_id', None)}, status={input_status}, current_task={input_current_task}, resource_usage={input_resource_data}, stats={input_stats}")

        return cls(
            worker_id=data.get("worker_id", None),
            status=input_status,
            current_task=input_current_task,
            resource_usage=input_resource_data,
            stats=input_stats,
            timestamp=data.get("timestamp", None)
        )

class WorkerEvent:
    """
    Container for worker event data.
    """
    
    def __init__(self,
                 worker_id: str,
                 event_type: str,
                 timestamp: Optional[float] = None,
                 data: Optional[Dict[str, Any]] = None):
        """
        Initialize a new WorkerEvent object.
        
        Args:
            worker_id: ID of the worker
            event_type: Type of the event
            timestamp: Timestamp of the event (if None, current time is used)
            data: Additional event data
        """
        self.worker_id = worker_id
        self.event_type = event_type
        self.timestamp = timestamp or time.time()
        self.data = data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the worker event to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the worker event
        """
        return {
            "worker_id": self.worker_id,
            "event": self.event_type,
            "timestamp": self.timestamp,
            **self.data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkerEvent':
        """
        Create a WorkerEvent object from a dictionary.
        
        Args:
            data: Dictionary containing worker event data
            
        Returns:
            WorkerEvent: New WorkerEvent object
        """
        # Extract the basic fields
        worker_id = data["worker_id"]
        event_type = data["event"]
        timestamp = data.get("timestamp")
        
        # Everything else is considered additional data
        event_data = {k: v for k, v in data.items() 
                     if k not in ["worker_id", "event", "timestamp"]}
        
        return cls(
            worker_id=worker_id,
            event_type=event_type,
            timestamp=timestamp,
            data=event_data
        )
