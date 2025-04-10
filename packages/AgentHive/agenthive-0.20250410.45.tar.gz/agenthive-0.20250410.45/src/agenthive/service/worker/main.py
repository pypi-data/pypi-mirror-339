"""
Main entry point for the py-AgentHive worker.

This module provides worker implementations and the main entry point 
for starting workers in the AgentHive system.
"""
import os
import sys
import asyncio
import logging
import argparse
import socket
import uuid
import signal
from typing import Optional, List, Dict, Any, Set, Tuple, Type
from pathlib import Path

import aiohttp
import importlib
import inspect

try:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
except ValueError:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.warning(f"Invalid log level '{os.environ.get('LOG_LEVEL', 'INFO').upper()}', defaulting to INFO")
else:
    logger = logging.getLogger(__name__)

logger.info(f"Starting py-AgentHive worker");

from agenthive.core.worker import Worker
from agenthive.core.heartbeat.constants import HeartbeatStrategy
from agenthive.utils.health import get_system_metrics
from agenthive.utils.module_loader import load_module_from_file, discover_worker_dirs
from agenthive.workers import *

logger.info(f"loading internal worker classes: {get_worker_class_name()}")  

# Global flag for shutdown
shutting_down = False

def signal_handler(signum, frame):
    global shutting_down
    shutting_down = True
    logger.info("Received shutdown signal, initiating graceful shutdown")

# Worker class registry and task type registry
worker_classes = {} # from agenthive.workers.__init__.py
worker_classes_with_task_type = {} # from agenthive.workers.__init__.py
task_type_registry = {}  # Maps task_type -> list of worker classes that can handle it

def load_workers():
    """
    Load all worker classes and register their task types.
    
    1. First try to import from agenthive.workers module
    2. Then try to import from packages specified in environment variables
    3. Finally try to import from custom directories
    
    Returns:
        bool: True if at least one Worker class was successfully loaded, False otherwise
    """
    global worker_classes, task_type_registry
    imported_classes = 0
    
    # 1. Try to import from main workers module
    try:
        for name in get_worker_class_name():
            if name != "Worker":
                worker_classes[name] = globals()[name]
                imported_classes += 1
        for name in get_worker_class_name_with_task_type():
            if name != "Worker":
                worker_classes_with_task_type[name] = globals()[name]
                register_task_types(worker_classes_with_task_type[name], name, 'agenthive.workers')
                imported_classes += 1
    except ImportError as e:
        logger.warning(f"Could not import workers from agenthive.workers: {e}")
    
    # 2. Try to import from custom directories
    worker_dirs = discover_worker_dirs()
    
    for directory in worker_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            logger.info(f"Looking for workers in: {directory}")
            
            # Add custom directory to sys.path
            if directory not in sys.path:
                sys.path.insert(0, directory)
            
            # Scan all Python files in directory
            python_files = glob.glob(os.path.join(directory, "*.py"))
            
            for file_path in python_files:
                # Skip __init__.py and .* files
                filename = os.path.basename(file_path)
                if filename.startswith('__') or filename.startswith('.'):
                    continue
                    
                # Load module
                module = load_module_from_file(file_path)
                if module:
                    # Find Worker classes in module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, Worker) and 
                            obj != Worker):
                            
                            worker_classes[name] = obj
                            task_types = register_task_types(obj, name, file_path)
                            if len(task_types) > 0:
                                worker_classes_with_task_type[name] = obj
                                imported_classes += 1
                                logger.info(f"01-Imported worker class: {name} from {file_path} with task types: {task_types}")
    
    # Look for Worker classes in subdirectories
    for directory in worker_dirs:
        # Walk all subdirectories
        for root, dirs, files in os.walk(directory):
            # Skip top level directory (already processed)
            if root == directory:
                continue
                
            # Check if subdirectory has __init__.py, might be a package
            if "__init__.py" in files:
                # Add package path to sys.path
                if root not in sys.path:
                    sys.path.insert(0, root)
                    
                # Try to import as package
                package_name = os.path.basename(root)
                try:
                    package = importlib.import_module(package_name)
                    
                    # Find Worker classes in package
                    for name, obj in inspect.getmembers(package):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, Worker) and 
                            obj != Worker):

                            worker_classes[name] = obj
                            task_types = register_task_types(obj, name, package_name)
                            if len(task_types) > 0:
                                worker_classes_with_task_type[name] = obj
                                imported_classes += 1
                                logger.info(f"02-Imported worker class: {name} from package {package_name} with task types: {task_types}")
                except ImportError as e:
                    logger.warning(f"Could not import package {package_name}: {e}")
            
            # Process Python files in directory
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(root, file)
                    module = load_module_from_file(file_path)
                    if module:
                        # Find Worker classes in module
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and 
                                issubclass(obj, Worker) and 
                                obj != Worker):
                                
                                worker_classes[name] = obj
                                task_types = register_task_types(obj, name, file_path)
                                if len(task_types) > 0:
                                    worker_classes_with_task_type[name] = obj
                                    imported_classes += 1
                                    logger.info(f"03-Imported worker class: {name} from {file_path} with task types: {task_types}")
    
    # Log summary of discovered task types
    logger.info(f"Discovered {len(task_type_registry)} task types across {imported_classes} worker classes")
    for task_type, workers in task_type_registry.items():
        worker_names = [w.__name__ for w in workers]
        logger.info(f"  Task type '{task_type}' can be handled by: {', '.join(worker_names)}")
    
    # All import attempts failed
    if imported_classes == 0:
        logger.error("No worker classes could be imported")
        return False
    
    logger.info(f"Successfully imported {imported_classes} worker classes")
    return True

async def register_with_coordinator(
    worker_id: str,
    coordinator_url: str,
    capabilities: List[str],
    configured_capabilities: List[str],
    available_capabilities: List[str],
    max_retries: int = 5,  
    retry_delay: int = 2 
    ) -> bool:
    """
    Register the worker with the coordinator.
    
    Args:
        worker_id: ID of the worker
        coordinator_url: URL of the coordinator
        capabilities: List of capabilities
        tags: List of tags
        max_retries: Maximum number of retries
        retry_delay: Delay between retries (in seconds)
        
    Returns:
        bool: True if registration was successful, False otherwise
    """
    # Get hostname and IP address
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "127.0.0.1"  # Fallback to localhost


    # Create registration data
    registration_data = {
        "worker_id": worker_id,
        "hostname": hostname,
        "ip_address": ip_address,
        "capabilities": capabilities,
        "configured_capabilities": configured_capabilities,
        "available_capabilities": available_capabilities,
        "tags": [],
    }
    
    logger.info(f"Registering worker with coordinator at {coordinator_url} with data: {registration_data}")

    # Try multiple times to register with coordinator
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{coordinator_url}/api/workers/register"
                logger.info(f"Attempting to register with coordinator at {url} (attempt {attempt+1}/{max_retries})")
                async with session.post(url, json=registration_data, timeout=5) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        logger.info(f"Worker registered: {response_data}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.warning(f"Registration attempt {attempt+1}/{max_retries} failed: {response.status} - {error_text}")
        
        except aiohttp.ClientConnectionError as e:
            logger.warning(f"Connection error on attempt {attempt+1}/{max_retries}: {e}")
        except asyncio.TimeoutError:
            logger.warning(f"Timeout on attempt {attempt+1}/{max_retries}")
        except Exception as e:
            logger.error(f"Registration error on attempt {attempt+1}/{max_retries}: {e}")
        
        # If this wasn't the last attempt, wait before retrying
        if attempt < max_retries - 1:
            logger.info(f"Waiting {retry_delay} seconds before next registration attempt...")
            await asyncio.sleep(retry_delay)
    
    # If we get here, all attempts failed
    logger.error(f"Registration failed after {max_retries} attempts")
    return False

def get_worker_class_by_type(task_type: str) -> Optional[type]:
    """
    Get worker class by type name.
    
    Args:
        worker_type: Type name of the worker
        
    Returns:
        Optional[type]: Worker class if found, None otherwise
    """
    global worker_classes
    return worker_classes.get(task_type, None)

def register_task_types(worker_class: Type[Worker], class_name: str, source: str) -> List[str]:
    """
    Register task types supported by a worker class.
    
    Args:
        worker_class: Worker class to register
        class_name: Name of the worker class
        source: Source of the worker class (file path or package name)
        
    Returns:
        List[str]: List of task types registered for this worker
    """
    global task_type_registry
    registered_types = []
    
    # Get task types from class attribute
    if hasattr(worker_class, 'TASK_TYPES'):
        task_types = worker_class.TASK_TYPES
    else:
        task_types = []
        
    # If no explicit task types defined, try to detect from process_* methods
    #if not task_types:
    #    for attr_name in dir(worker_class):
    #        if (attr_name.startswith('process_') and 
    #            callable(getattr(worker_class, attr_name))):
    #            task_type = attr_name[8:]  # Remove 'process_' prefix
    #            if task_type:
    #                task_types.append(task_type)
    
    # Register each task type
    for task_type in task_types:
        if task_type not in task_type_registry:
            task_type_registry[task_type] = []
            
        # Check for duplicates with exact same worker class
        if worker_class not in task_type_registry[task_type]:
            task_type_registry[task_type].append(worker_class)
            registered_types.append(task_type)
            
            # Log duplicate task types (handled by different workers)
            if len(task_type_registry[task_type]) > 1:
                other_workers = [w.__name__ for w in task_type_registry[task_type] if w != worker_class]
                logger.warning(
                    f"Task type '{task_type}' is handled by multiple workers: {class_name} and {', '.join(other_workers)}"
                )
    
    return registered_types

if not load_workers():
    logger.error("Failed to load any worker classes, exiting")
    sys.exit(1)

required_workers = ["MainServiceWorker"]
missing_workers = [w for w in required_workers if w not in worker_classes]
if missing_workers:
    logger.warning(f"Missing required worker classes: {missing_workers}")
    logger.warning("System may not function correctly without these workers")

MainServiceWorker = worker_classes.get("MainServiceWorker")

async def main():
    """
    Main entry point for the worker.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="py-AgentHive Worker")
    parser.add_argument("--worker-id", help="Worker ID (default: auto-generated)")
    parser.add_argument("--coordinator", help="URL of the coordinator (default: from environment)")
    parser.add_argument("--capabilities", help="Comma-separated list of capabilities")
    parser.add_argument("--redis-url", help="Redis URL (default: from environment)")
    parser.add_argument("--heartbeat-interval", type=int, help="Heartbeat interval in seconds (default: from environment)")
    parser.add_argument("--resource-check-interval", type=int, help="Resource check interval in seconds (default: from environment)")
    parser.add_argument("--scan-dir", help="Additional directory to scan for worker modules")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Set log level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get worker ID
    worker_id = args.worker_id
    if not worker_id:
        os.environ.get("WORKER_ID", None)
    if not worker_id:
        # Generate worker ID if not provided
        hostname = socket.gethostname()
        unique_id = str(uuid.uuid4())[:8]
        worker_id = f"{hostname}-{unique_id}"    
    
    # Get coordinator URL
    coordinator_url = args.coordinator or os.environ.get("COORDINATOR_URL", "http://localhost:8000")
    
    # Get Redis URL
    redis_url = args.redis_url or os.environ.get("REDIS_URL")
    
    # Get heartbeat interval
    heartbeat_interval = args.heartbeat_interval or int(os.environ.get("HEARTBEAT_INTERVAL", "60"))
    
    # Get resource check interval
    resource_check_interval = args.resource_check_interval or int(os.environ.get("RESOURCE_CHECK_INTERVAL", "30"))
    
    # Scan additional directory if provided
    if args.scan_dir:
        if os.path.exists(args.scan_dir) and os.path.isdir(args.scan_dir):
            if args.scan_dir not in sys.path:
                sys.path.insert(0, args.scan_dir)
                
            discover_worker_dirs()
            # Reload workers from this directory
            imported_classes = 0
            for filename in os.listdir(args.scan_dir):
                if filename.endswith('.py') and not filename.startswith('__'):
                    file_path = os.path.join(args.scan_dir, filename)
                    module = load_module_from_file(file_path)
                    if module:
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and 
                                issubclass(obj, Worker) and 
                                obj != Worker):
                                
                                worker_classes[name] = obj
                                task_types = register_task_types(obj, name, file_path)
                                if len(task_types) > 0:
                                    worker_classes_with_task_type[name] = obj
                                    imported_classes += 1
                                    logger.info(f"04-Imported worker class: {name} from {file_path} with task types: {task_types}")
            logger.info(f"Discovered {imported_classes} worker classes in {args.scan_dir}")

    # Get capabilities
    capabilities_str = args.capabilities or os.environ.get("CAPABILITIES", "")
    capabilities = [c.strip() for c in capabilities_str.split(",")] if capabilities_str else []

    available_work_types = []
    if capabilities:
        for target_type in capabilities:
            if get_worker_class_by_type(target_type):
                available_work_types.append(target_type)
            else:
                logger.warning(f"No worker class found for type '{target_type}'")
    else:
        logger.info(f"No capabilities specified, using all available worker types")
        available_work_types = list(task_type_registry.keys())

    if len(available_work_types) == 0:
        logger.error(f"No worker classes available for the specified capabilities: {capabilities}, worker supports: {task_type_registry.keys()}")
        return

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    mainServiceWorkerObject = MainServiceWorker(
        coordinator_url=coordinator_url,
        worker_id=worker_id,
        heartbeat_interval=heartbeat_interval,
        resource_check_interval=resource_check_interval,
        redis_url=redis_url,
        heartbeat_strategy=HeartbeatStrategy.REDIS,
        worker_classes=worker_classes_with_task_type,
        task_type_registry=task_type_registry, 
        available_work_types=available_work_types,
    )

    # Register with coordinator
    logger.info(f"Registering worker {worker_id} of type {available_work_types} with coordinator at {coordinator_url}")
    
    # Delay before registering with coordinator
    startup_delay = int(os.environ.get("WORKER_STARTUP_DELAY", "5"))
    if startup_delay > 0:
        logger.info(f"Waiting {startup_delay} seconds for coordinator to start up...")
        await asyncio.sleep(startup_delay)
    
    # Register with coordinator
    registration_success = await register_with_coordinator(
        worker_id=worker_id,
        coordinator_url=coordinator_url,
        capabilities=available_work_types,
        configured_capabilities=capabilities,
        available_capabilities=list(task_type_registry.keys()),
        max_retries=int(os.environ.get("WORKER_REGISTRATION_MAX_RETRIES", "15"))
    )

    if not registration_success:
        logger.error(f"Failed to register worker {worker_id} with coordinator")
        logger.error("Exiting...")
        return

    # Start the worker
    logger.info(f"Starting worker {worker_id} with task_types: {available_work_types}")
    
    try:
        # Start the worker
        await mainServiceWorkerObject.run()
    
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping worker")
    
    except Exception as e:
        logger.error(f"Worker error: {e}")
    
    finally:
        # Close worker resources
        await mainServiceWorkerObject.close()

if __name__ == "__main__":
    asyncio.run(main())
