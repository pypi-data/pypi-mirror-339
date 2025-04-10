"""
Health check utilities for py-AgentHive.
"""
import os
import sys
import logging
import socket
import time
from typing import Dict, Any, Optional

import psutil
import redis

logger = logging.getLogger(__name__)

def check_worker_health() -> bool:
    """
    Check if the worker is healthy.
    
    This function is used by the Docker health check to determine if the worker
    is functioning properly.
    
    Returns:
        bool: True if healthy, False otherwise
    """
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        # Check if CPU or memory usage is too high
        if cpu_percent > 95 or memory_percent > 95:
            logger.warning(f"Resource usage too high: CPU={cpu_percent}%, Memory={memory_percent}%")
            return False
        
        # Check Redis connection
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        try:
            r = redis.from_url(redis_url)
            r.ping()
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return False
        
        # All checks passed
        return True
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False

def check_coordinator_connection() -> bool:
    """
    Check if the worker can connect to the coordinator.
    
    Returns:
        bool: True if can connect, False otherwise
    """
    coordinator_url = os.environ.get("COORDINATOR_URL", "http://localhost:8000")
    
    # Extract host and port from URL
    if coordinator_url.startswith("http://"):
        host_port = coordinator_url[7:]
    elif coordinator_url.startswith("https://"):
        host_port = coordinator_url[8:]
    else:
        host_port = coordinator_url
    
    # Split host and port
    if ":" in host_port:
        host, port_str = host_port.split(":")
        if "/" in port_str:
            port_str = port_str.split("/")[0]
        port = int(port_str)
    else:
        host = host_port
        port = 80
    
    # Try to connect
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        s.close()
        return True
    except Exception as e:
        logger.error(f"Coordinator connection failed: {e}")
        return False

def get_system_metrics() -> Dict[str, Any]:
    """
    Get system metrics.
    
    Returns:
        Dict[str, Any]: System metrics
    """
    # CPU metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    
    # Memory metrics
    memory = psutil.virtual_memory()
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    
    # Network metrics
    net_io = psutil.net_io_counters()
    
    # Process metrics
    process = psutil.Process()
    process_memory = process.memory_info()
    
    return {
        "cpu": {
            "percent": cpu_percent,
            "count": cpu_count
        },
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        },
        "network": {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        },
        "process": {
            "memory_rss": process_memory.rss,
            "memory_vms": process_memory.vms,
            "cpu_percent": process.cpu_percent(interval=0.1),
            "threads": process.num_threads()
        }
    }

if __name__ == "__main__":
    # Run health check when called directly
    if check_worker_health():
        print("Worker is healthy")
        sys.exit(0)
    else:
        print("Worker is unhealthy")
        sys.exit(1)
