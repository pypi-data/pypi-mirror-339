"""
Worker implementations for AgentHive.

This module dynamically loads all worker implementations from the files
in this directory and registers them with the TaskRegistry.
"""
import os
import sys
import importlib
import inspect
import logging
from typing import Dict, Type, List, Optional

from agenthive.core.worker import Worker

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

# 存储所有worker类
worker_classes: Dict[str, Type[Worker]] = {}
worker_classes_with_task_type: Dict[str, Type[Worker]] = {}

# 动态导入当前目录下的所有Python文件
for filename in os.listdir(current_dir):
    # 跳过非Python文件、特殊文件和目录
    if not filename.endswith('.py') or filename.startswith('__') or os.path.isdir(os.path.join(current_dir, filename)):
        continue
        
    module_name = filename[:-3]  # 去除.py后缀
    
    try:
        # 导入模块
        module = importlib.import_module(f"agenthive.workers.{module_name}")
        
        # 查找模块中所有Worker子类
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, Worker) and 
                obj != Worker and
                obj.__module__ == module.__name__):

                worker_classes[name] = obj
                if len(obj.TASK_TYPES) > 0:
                    worker_classes_with_task_type[name] = obj
                    logger.info(f"Found worker class: agenthive.workers.{name} with TASK_TYPES: {obj.TASK_TYPES}")
                else:
                    logger.info(f"Worker agenthive.workers.{name} has no TASK_TYPES defined, skipping")
                
    except Exception as e:
        logger.warning(f"Error importing worker module {module_name}: {e}")

logger.info(f"Found {len(worker_classes)} worker classes in total, {len(worker_classes_with_task_type)} with TASK_TYPES defined") 

def get_worker_class_name() -> Dict[str, Type[Worker]]:
    global worker_classes
    return list(worker_classes.keys())

def get_worker_class_name_with_task_type() -> List[Type[Worker]]:
    global worker_classes_with_task_type
    return list(worker_classes_with_task_type.keys())

__all__ = ['get_worker_class_name', 'get_worker_class_name_with_task_type'] + list(worker_classes.keys()) 

globals().update(worker_classes)
globals().update(worker_classes_with_task_type)