"""
Task registry for AgentHive.

This module provides a task registry to track available task types and their handlers.
It follows a similar pattern to the database adapters by providing a centralized
registry that can be accessed throughout the application.
"""
import logging
from typing import Dict, Type, Optional, Set, List

logger = logging.getLogger(__name__)

class TaskRegistry:
    """
    Task registry for tracking available task types and their handlers.
    
    This registry maintains a mapping of task types to worker classes,
    allowing the coordinator to validate task types without requiring
    workers to be online.
    """
    
    _registry: Dict[str, List[str]] = {}  # task_type -> list of worker types
    _worker_capabilities: Dict[str, Set[str]] = {}  # worker_type -> set of capabilities
    
    @classmethod
    def register_worker_type(cls, worker_type: str, capabilities: List[str]) -> None:
        """
        Register a worker type with its capabilities.
        
        Args:
            worker_type: Type of the worker
            capabilities: List of task types this worker can handle
        """
        cls._worker_capabilities[worker_type] = set(capabilities)
        
        for capability in capabilities:
            if capability not in cls._registry:
                cls._registry[capability] = []
            if worker_type not in cls._registry[capability]:
                cls._registry[capability].append(worker_type)
        
        logger.info(f"Registered worker type {worker_type} with capabilities: {capabilities}")
    
    @classmethod
    def get_worker_types(cls, task_type: str) -> List[str]:
        """
        Get worker types that can handle a specific task type.
        
        Args:
            task_type: Type of the task
            
        Returns:
            List[str]: List of worker types that can handle this task
        """
        return cls._registry.get(task_type, [])
    
    @classmethod
    def get_capabilities(cls, worker_type: str) -> Set[str]:
        """
        Get capabilities of a worker type.
        
        Args:
            worker_type: Type of the worker
            
        Returns:
            Set[str]: Set of capabilities
        """
        return cls._worker_capabilities.get(worker_type, set())
    
    @classmethod
    def is_task_supported(cls, task_type: str) -> bool:
        """
        Check if a task type is supported.
        
        Args:
            task_type: Type of the task
            
        Returns:
            bool: True if the task type is supported, False otherwise
        """
        return task_type in cls._registry and len(cls._registry[task_type]) > 0
    
    @classmethod
    def get_all_task_types(cls) -> List[str]:
        """
        Get all registered task types.
        
        Returns:
            List[str]: List of all registered task types
        """
        return list(cls._registry.keys())
    
    @classmethod
    def get_all_worker_types(cls) -> List[str]:
        """
        Get all registered worker types.
        
        Returns:
            List[str]: List of all registered worker types
        """
        return list(cls._worker_capabilities.keys())
    
    @classmethod
    def clear(cls) -> None:
        """
        Clear the registry.
        
        This method is mainly useful for testing.
        """
        cls._registry.clear()
        cls._worker_capabilities.clear()
        logger.debug("Task registry cleared")


# Register default worker types and capabilities
TaskRegistry.register_worker_type("generic", ["echo", "transform", "time_report"])
TaskRegistry.register_worker_type("crawler", ["crawl", "scrape", "extract"])
TaskRegistry.register_worker_type("ai_agent", ["generate", "classify", "analyze"])


def supports_task(task_type: str):
    """
    Decorator to register a task type.
    
    This decorator can be used on worker classes to register
    the task types they support.
    
    Args:
        task_type: Type of the task
        
    Returns:
        Function: Decorator function
    """
    def decorator(worker_class):
        worker_type = worker_class.__name__
        capabilities = getattr(worker_class, "_capabilities", [])
        capabilities.append(task_type)
        setattr(worker_class, "_capabilities", capabilities)
        TaskRegistry.register_worker_type(worker_type, capabilities)
        return worker_class
    return decorator
