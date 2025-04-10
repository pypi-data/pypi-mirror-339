"""Base database adapter interface definition with protocol."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import datetime

class BaseDBAdapter(ABC):
    """Base interface for database adapters."""
    
    def __init__(self, connection_string: str, **options: Any) -> None:
        """Initialize with connection string and options."""
        self.connection_string = connection_string
        self._connected = False
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to database."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close database connection."""
        pass
    
    @abstractmethod
    async def save_heartbeat(self, heartbeat_data: Dict[str, Any]) -> None:
        """Save heartbeat data to database."""
        pass
    
    @abstractmethod
    async def save_worker(self, data: Dict[str, Any]) -> None:
        """Save worker to database."""
        pass

    @abstractmethod
    async def save_worker_event(self, event_data: Dict[str, Any]) -> None:
        """Save worker event to database."""
        pass

    @abstractmethod
    async def save_task(self, data: Dict[str, Any]) -> None:
        """Save task to database."""
        pass
    
    @abstractmethod
    async def get_active_workers(self, timeout_seconds: int = 30) -> List[Dict[str, Any]]:
        """Get active workers based on timeout threshold."""
        pass
    
    @abstractmethod
    async def get_worker_history(self, worker_id: str, limit: int = 100, 
                                since: Optional[datetime.datetime] = None) -> List[Dict[str, Any]]:
        """Get worker's heartbeat history."""
        pass

__all__ = ['BaseDBAdapter']