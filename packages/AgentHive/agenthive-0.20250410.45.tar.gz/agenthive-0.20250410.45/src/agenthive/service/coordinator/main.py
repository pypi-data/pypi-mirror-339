"""
API module for the py-AgentHive coordinator.
"""
import os
import time
import logging
import asyncio
import json
import datetime
from typing import Dict, Any, List, Optional, Set
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Query, Header, Body, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError, field_validator, Field 

from agenthive.core.coordinator import Coordinator
from agenthive.core.enhanced_coordinator import EnhancedCoordinator
from agenthive.utils.health import get_system_metrics
from agenthive.db.connection import init_db
from agenthive.version import __version__

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

# Application state
class AppState:
    coordinator: Optional[Coordinator] = None
    enhanced_coordinator: Optional[EnhancedCoordinator] = None
    background_tasks: List[asyncio.Task] = []
    supported_task_types: Set[str] = set()  # Set of supported task types from active workers

app_state = AppState()

# Ping-pong task for health checks
async def ping_pong_task(redis_client):
    while True:
        try:
            ping = await redis_client.get("coordinator:ping")
            if ping:
                await redis_client.set("coordinator:pong", time.time())
                await redis_client.delete("coordinator:ping")
        except Exception as e:
            logger.error(f"Ping-pong error: {e}")
        
        await asyncio.sleep(1)

# Task to periodically update supported task types from worker registrations
async def update_supported_task_types(coordinator: Coordinator):
    """Periodically update the set of supported task types based on active workers"""
    while True:
        try:
            # Get all active workers
            active_workers = await coordinator.get_active_workers()
            
            # Clear current set
            app_state.supported_task_types = set()
            
            # Add task types from each worker
            for worker in active_workers:
                # Get task types from either task_types field or capabilities
                worker_task_types = worker.get("task_types", worker.get("capabilities", []))
                app_state.supported_task_types.update(worker_task_types)
            
            # Also update in Redis for persistence and sharing
            if coordinator._redis_client:
                await coordinator._redis_client.delete("supported_task_types")
                if app_state.supported_task_types:
                    await coordinator._redis_client.sadd("supported_task_types", *app_state.supported_task_types)
                
            logger.debug(f"Updated supported task types: {app_state.supported_task_types}")
        except Exception as e:
            logger.error(f"Error updating supported task types: {e}")
        
        # Update every minute
        await asyncio.sleep(60)

def dump_environment_variables():
    """
    Dump all environment variables to logs for debugging
    """
    output_logs = ["\n", "==== ENVIRONMENT VARIABLES == Begin =="]
    for key, value in sorted(os.environ.items()):
        # Mask sensitive information in logs
        if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token']):
            masked_value = '****'
            output_logs.append(f"{key} = {masked_value}")
        else:
            output_logs.append(f"{key} = {value}")
    output_logs.append("==== ENVIRONMENT VARIABLES == End ==")
    logger.info("\n".join(output_logs))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI app.
    Handles initialization and cleanup of resources.
    """
   
    dump_environment_variables()

    # Startup logic
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    db_url = os.environ.get("DATABASE_URL")

    logger.info(f"Starting coordinator API service, Redis URL: {redis_url}, db URL: {db_url}")

    # Initialize database
    if db_url:
        await init_db(db_url)
        logger.debug("Database initialized with tables")
    
    # Create coordinator instance
    app_state.coordinator = Coordinator(
        redis_url=redis_url,
        db_url=db_url,
        worker_timeout=int(os.environ.get("WORKER_TIMEOUT", "60")),
        storage_backend=os.environ.get("STORAGE_BACKEND", "redis"),
        metrics_enabled=os.environ.get("ENABLE_METRICS", "true").lower() == "true",
        metrics_retention=int(os.environ.get("METRICS_RETENTION", "86400"))
    )
    
    # Create enhanced coordinator
    app_state.enhanced_coordinator = EnhancedCoordinator(app_state.coordinator)
    
    # Initialize and start coordinator
    await app_state.coordinator.initialize()
    await app_state.coordinator.start()
    
    # Set coordinator status in Redis
    try:
        redis_client = app_state.coordinator._redis_client
        if redis_client:
            await redis_client.set("coordinator:status", "active")
            
            # Start ping-pong task for health checks
            app_state.background_tasks.append(asyncio.create_task(ping_pong_task(redis_client)))
            
            # Start task type update task
            app_state.background_tasks.append(asyncio.create_task(
                update_supported_task_types(app_state.coordinator)
            ))
    except Exception as e:
        logger.error(f"Failed to set coordinator status: {e}")
    
    logger.info("Coordinator API Service started")

    redis_client = app_state.coordinator._redis_client
    if not redis_client or not await redis_client.ping():
        logger.error("Failed to connect to Redis")
        raise RuntimeError("Redis connection failed")
    if db_url and not app_state.coordinator._db_adapter:
        logger.error("Failed to connect to database")
        raise RuntimeError("Database connection failed")    
    yield  # This is where the application runs
    
    # Shutdown logic
    if app_state.coordinator:
        # Update status in Redis
        try:
            redis_client = app_state.coordinator._redis_client
            if redis_client:
                await redis_client.set("coordinator:status", "stopping")
        except Exception as e:
            logger.error(f"Failed to update coordinator status: {e}")
        
        # Stop coordinator
        await app_state.coordinator.stop()
    
    # Cancel background tasks
    for task in app_state.background_tasks:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    
    logger.info("Coordinator API Service stopped")

# Create FastAPI app with lifespan
app = FastAPI(
    title="AgentHive Coordinator",
    description="API for the AgentHive distributed system coordinator",
    version=__version__,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class WorkerRegistration(BaseModel):
    worker_id: str
    hostname: str
    ip_address: str
    capabilities: List[str]
    configured_capabilities: List[str]
    available_capabilities: List[str]
    tags: List[str]

class WorkerHeartbeat(BaseModel):
    worker_id: str
    status: str
    current_task: Optional[str] = None
    resource_usage: Optional[Dict[str, Any]] = None
    stats: Optional[Dict[str, Any]] = None

class TaskSubmission(BaseModel):
    task_type: str
    priority: int = 0
    data: Dict[str, Any]
    timeout: Optional[int] = None
    dependencies: List[str] = []
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    
    #@field_validator('task_type')
    #@classmethod
    #def validate_task_type(cls, v):
    #    # TaskRegistry validation is removed here - we now validate against registered workers
    #    return v.task_type 

class TaskResult(BaseModel):
    task_id: str
    worker_id: str
    result: Dict[str, Any]
    extra_data: Dict[str, Any]

class TaskFailure(BaseModel):
    task_id: str
    worker_id: str
    error: str
    extra_data: Dict[str, Any]

# Dependency to get coordinator
async def get_coordinator():
    if app_state.coordinator is None:
        raise HTTPException(status_code=503, detail="Coordinator not initialized")
    return app_state.coordinator

# Dependency to get enhanced coordinator
async def get_enhanced_coordinator():
    if app_state.enhanced_coordinator is None:
        raise HTTPException(status_code=503, detail="Enhanced coordinator not initialized")
    return app_state.enhanced_coordinator

# API key verification (if enabled)
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if os.environ.get("API_KEY_ENABLED", "false").lower() == "true":
        api_key = os.environ.get("API_KEY", "")
        if not api_key:
            return  # No API key configured, so don't check
        
        if x_api_key != api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )

# Task type validation
async def validate_task_type(task_type: str) -> bool:
    """
    Validate if a task type is supported by any active worker.
    
    Args:
        task_type: The task type to validate
        
    Returns:
        bool: True if the task type is supported, False otherwise
    """
    # Check in-memory registry first
    if task_type in app_state.supported_task_types:
        return True
        
    # If not found in memory, check Redis for persistence
    if app_state.coordinator and app_state.coordinator._redis_client:
        try:
            result = await app_state.coordinator._redis_client.sismember("supported_task_types", task_type)
            return bool(result)
        except Exception as e:
            logger.error(f"Error checking task type in Redis: {e}")
    
    # Default to false if we can't verify
    return False

# API routes
@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Check if the coordinator API is healthy.
    """
    if app_state.coordinator is None or not app_state.coordinator._running:
            raise HTTPException(status_code=503, detail="Coordinator not running")
    redis_ok = await app_state.coordinator._redis_client.ping() if app_state.coordinator._redis_client else False
    db_ok = await app_state.coordinator._db_adapter.check_connection() if app_state.coordinator._db_adapter and hasattr(app_state.coordinator._db_adapter, 'check_connection') else True
    return {"status": "ok" if redis_ok and db_ok else "fail", "redis": "ok" if redis_ok else "fail", "db": "ok" if db_ok else "fail"}

@app.post("/api/workers/register", dependencies=[Depends(verify_api_key)])
async def register_worker(
    registration: WorkerRegistration,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Register a worker with the coordinator.
    """
    logger.debug(f"Registering worker: {registration.worker_id}, capabilities: {registration.capabilities}, tags: {registration.tags}, hostname: {registration.hostname}, IP: {registration.ip_address}, configured: {registration.configured_capabilities}, available: {registration.available_capabilities}")
    # Handle task_types if provided
    task_types = registration.capabilities
    
    # Update supported task types
    app_state.supported_task_types.update(task_types)
    
    # Store task types in Redis
    if coordinator._redis_client:
        try:
            # Add to supported task types set
            if task_types:
                await coordinator._redis_client.sadd("supported_task_types", *task_types)
            
            # Also store mapping of worker to task types for future reference
            worker_task_types_key = f"worker:{registration.worker_id}:task_types"
            await coordinator._redis_client.delete(worker_task_types_key)
            if task_types:
                await coordinator._redis_client.sadd(worker_task_types_key, *task_types)
        except Exception as e:
            logger.error(f"Error storing task types in Redis: {e}")
    
    # Log supported task types
    logger.info(f"Worker {registration.worker_id} supports task types: {task_types}")
    logger.info(f"Updated system-wide supported task types: {app_state.supported_task_types}")
    
    # Register worker with coordinator
    success = await coordinator.register_worker(
        worker_id=registration.worker_id,
        capabilities=registration.capabilities,
        configured_capabilities=registration.configured_capabilities,
        available_capabilities=registration.available_capabilities,
        hostname=registration.hostname,
        ip_address=registration.ip_address,
        tags=registration.tags
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to register worker")
    
    return {"status": "registered", "worker_id": registration.worker_id}

@app.post("/api/workers/heartbeat", dependencies=[Depends(verify_api_key)])
async def worker_heartbeat(
    heartbeat: WorkerHeartbeat,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Update worker heartbeat information.
    """
    success = await coordinator.worker_heartbeat(
        worker_id=heartbeat.worker_id,
        status=heartbeat.status,
        current_task=heartbeat.current_task,
        resource_usage=heartbeat.resource_usage,
        stats=heartbeat.stats
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update heartbeat")
    
    return {"status": "updated", "timestamp": time.time()}

@app.get("/api/workers", dependencies=[Depends(verify_api_key)])
async def get_workers(
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get information about all active workers.
    """
    workers = await coordinator.get_active_workers()
    return {"workers": workers, "count": len(workers)}

@app.post("/api/tasks/submit", dependencies=[Depends(verify_api_key)])
async def submit_task(
    task_submission: TaskSubmission,
    enhanced_coordinator: EnhancedCoordinator = Depends(get_enhanced_coordinator)
):
    """
    Submit a task for processing.
    """
    # First validate if the task type is supported by any active worker
    is_supported = await validate_task_type(task_submission.task_type)
    if not is_supported:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported task type: {task_submission.task_type}. No active worker supports this task type."
        )
    
    task_id = None
    try:
        task_id = await enhanced_coordinator.create_task(
            task_type=task_submission.task_type,
            task_data=task_submission.data,
            priority=task_submission.priority
        )
    except Exception as e:
        logger.error(f"Error submitting task: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"Task {task_id} submitted with type {task_submission.task_type} and priority {task_submission.priority}")
    return {"status": "submitted", "task_id": task_id}

@app.get("/api/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
async def get_task_status(
    task_id: str,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get the status of a task.
    """
    status = await coordinator.get_task_status(task_id)
    
    if status.get("status") == "unknown":
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return status

@app.get("/api/tasks/{task_id}/result", dependencies=[Depends(verify_api_key)])
async def get_task_result(
    task_id: str,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get the result of a completed task.
    """
    status = await coordinator.get_task_status(task_id)
    
    if status.get("status") == "unknown":
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    if status.get("status") != "completed":
        raise HTTPException(status_code=400, detail=f"Task {task_id} is not completed")
    
    result = await coordinator.get_task_result(task_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Result for task {task_id} not found")
    
    return {"task_id": task_id, "result": result}

@app.post("/api/tasks/{task_id}/complete", dependencies=[Depends(verify_api_key)])
async def report_task_complete(
    task_id: str,
    task_result: TaskResult,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Report that a task has been completed.
    """
    if task_id != task_result.task_id:
        raise HTTPException(status_code=400, detail="Task ID mismatch")
    
    
    success = await coordinator.report_task_complete(
        worker_id=task_result.worker_id,
        task_id=task_id,
        result=task_result.result, 
        extra_data=task_result.extra_data,
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to report task completion")
    
    return {"status": "completed", "task_id": task_id}

@app.post("/api/tasks/{task_id}/fail", dependencies=[Depends(verify_api_key)])
async def report_task_failure(
    task_id: str,
    task_failure: TaskFailure,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Report that a task has failed.
    """
    if task_id != task_failure.task_id:
        raise HTTPException(status_code=400, detail="Task ID mismatch")
    
    success = await coordinator.report_task_failure(
        worker_id=task_failure.worker_id,
        task_id=task_id,
        error=task_failure.error,
        extra_data=task_failure.extra_data,
   )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to report task failure")
    
    return {"status": "failed", "task_id": task_id}

@app.get("/api/next/task", dependencies=[Depends(verify_api_key)])
async def get_next_task(
    worker_id: str = Query(..., description="ID of the worker requesting a task"),
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get the next task for a worker to process.
    """
    task = await coordinator.get_next_task(worker_id)
    
    if task is None:
        return {"status": "no_task", "worker_id": worker_id}
    
    return {"status": "task_available", "task": task, "worker_id": worker_id}

@app.get("/api/tasks", dependencies=[Depends(verify_api_key)])
async def get_tasks(
    status: Optional[str] = Query(None, description="Filter by task status"),
    task_type: Optional[str] = Query(None, description="Filter by task type"),
    limit: int = Query(100, description="Maximum number of tasks to return"),
    enhanced_coordinator: EnhancedCoordinator = Depends(get_enhanced_coordinator)
):
    """
    Get tasks with optional filtering.
    """
    tasks = await enhanced_coordinator.get_tasks(
        status=status,
        task_type=task_type,
        limit=limit
    )
    
    return {
        "tasks": tasks,
        "count": len(tasks),
        "status_filter": status,
        "type_filter": task_type
    }

@app.get("/api/metrics/tasks", dependencies=[Depends(verify_api_key)])
async def get_task_metrics(
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get metrics about tasks in the system.
    """
    metrics = await coordinator.get_task_metrics()
    return metrics

@app.get("/api/supported_task_types")
async def get_supported_task_types():
    """
    Get all supported task types from active workers.
    """
    # First check in-memory cache
    in_memory_types = list(app_state.supported_task_types)
    
    # If empty, try to get from Redis
    if not in_memory_types and app_state.coordinator and app_state.coordinator._redis_client:
        try:
            redis_types = await app_state.coordinator._redis_client.smembers("supported_task_types")
            in_memory_types = [t.decode('utf-8') if isinstance(t, bytes) else t for t in redis_types]
            
            # Update in-memory cache
            app_state.supported_task_types.update(in_memory_types)
        except Exception as e:
            logger.error(f"Error getting supported task types from Redis: {e}")
 
    return {"task_types": in_memory_types}

# Exception handler for validation errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Handle Pydantic validation errors.
    """
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )

@app.get("/api/metrics/workers", dependencies=[Depends(verify_api_key)])
async def get_worker_metrics(
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get metrics about workers in the system.
    """
    metrics = await coordinator.get_worker_metrics()
    return metrics

@app.get("/api/metrics/system", dependencies=[Depends(verify_api_key)])
async def get_system_metrics_api():
    """
    Get metrics about the system.
    """
    metrics = get_system_metrics()
    
    # Add coordinator-specific metrics
    if app_state.coordinator:
        metrics["coordinator"] = {
            "start_time": app_state.coordinator._start_time if hasattr(app_state.coordinator, "_start_time") else time.time(),
            "task_registry_size": len(app_state.coordinator._task_registry) if hasattr(app_state.coordinator, "_task_registry") else 0,
            "worker_registry_size": len(app_state.coordinator._worker_registry) if hasattr(app_state.coordinator, "_worker_registry") else 0,
            "task_queue_size": len(app_state.coordinator._task_queue) if hasattr(app_state.coordinator, "_task_queue") else 0,
            "task_results_size": len(app_state.coordinator._task_results) if hasattr(app_state.coordinator, "_task_results") else 0,
            "supported_task_types": list(app_state.supported_task_types)
        }
    
    return metrics

@app.get("/api/metrics/overview", dependencies=[Depends(verify_api_key)])
async def get_overview_metrics_api():
    """
    Get metrics overview about the system.
    """
    output = {
        "datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    if app_state and app_state.coordinator:
        output = await app_state.coordinator.get_overview_info()
    
    return output


@app.get("/api/load/tasks", dependencies=[Depends(verify_api_key)])
async def load_tasks():
    """
    Load tasks from the database.
    """
    if app_state.coordinator and app_state.coordinator._db_adapter:
        tasks = await app_state.coordinator._load_tasks_from_database()
        return {"load": tasks}

def hypercornMain():
    """
    Main function - use Hypercorn to run the FastAPI application
    """
    import asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    import sys
   
    # Get host and port
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    logger.info(f"Starting Coordinator API service, listening on {host}:{port}")
    
    # Configure Hypercorn
    config = Config()
    config.bind = [f"{host}:{port}"]
    config.use_reloader = os.environ.get("DEBUG", "false").lower() == "true"
    config.accesslog = "-"  # Output access logs to stdout
    config.errorlog = "-"   # Output error logs to stdout
    config.loglevel = "info"
    
    try:
        # Run server
        asyncio.run(serve(app, config))
    except KeyboardInterrupt:
        logger.info("Server stopped")

def main():
    """
    Main function - use uvicorn to run the FastAPI application
    """
    import uvicorn
    
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    logger.info(f"Starting Coordinator API service, listening on {host}:{port}")
    
    uvicorn.run(
        "agenthive.service.coordinator.main:app", 
        host=host, 
        port=port,
        reload=os.environ.get("DEBUG", "false").lower() == "true"
    )

if __name__ == "__main__":
    main()
