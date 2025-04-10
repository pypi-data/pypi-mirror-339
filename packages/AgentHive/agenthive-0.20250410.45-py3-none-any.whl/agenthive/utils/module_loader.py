"""
Module loading utilities for dynamically importing Python modules.

This module provides functions for dynamically loading Python modules 
from file paths or packages at runtime.
"""
import os
import sys
import importlib.util
import logging
from typing import Optional, Dict, List, Any, Type

logger = logging.getLogger(__name__)

def load_module_from_file(file_path: str) -> Optional[object]:
    """
    Dynamically load a Python module from a file path.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        object: Loaded module object, or None if loading failed
    """
    try:
        module_name = os.path.basename(file_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return None
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Error loading module from {file_path}: {e}")
        return None
    
def discover_worker_dirs() -> List[str]:
    """
    Discover all directories that may contain Worker implementations.
    
    Searches environment variables for directory paths, with support for multiple
    directories separated by colons or semicolons.
    
    Returns:
        List[str]: List of directories containing Worker implementations
    """
    worker_dirs = []
    
    # 1. Check WORKER_DIRS environment variable (multiple directories, colon or semicolon separated)
    worker_dirs_env = os.environ.get("WORKER_DIRS", "")
    if worker_dirs_env:
        # Support colon or semicolon separators
        for separator in [':', ';']:
            if separator in worker_dirs_env:
                dirs = [d.strip() for d in worker_dirs_env.split(separator) if d.strip()]
                worker_dirs.extend(dirs)
                break
        else:
            # If no separator, treat as a single directory
            worker_dirs.append(worker_dirs_env.strip())
    
    # 2. Check CUSTOM_WORKERS_PATH environment variable (backward compatibility)
    custom_workers_path = os.environ.get("CUSTOM_WORKERS_PATH")
    if custom_workers_path and custom_workers_path not in worker_dirs:
        worker_dirs.append(custom_workers_path)
    
    # 3. Check WORKER_PLUGINS_DIR environment variable
    plugins_dir = os.environ.get("WORKER_PLUGINS_DIR")
    if plugins_dir and plugins_dir not in worker_dirs:
        worker_dirs.append(plugins_dir)
    
    # 4. Check for plugins or workers subdirectories in the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for subdir in ['plugins', 'workers', 'custom_workers']:
        path = os.path.join(current_dir, subdir)
        if os.path.exists(path) and os.path.isdir(path) and path not in worker_dirs:
            worker_dirs.append(path)
    
    # 5. Additionally check WORKER_PACKAGES environment variable (comma-separated package names)
    # This is just recorded here, actual import happens in load_workers function
    
    return worker_dirs

