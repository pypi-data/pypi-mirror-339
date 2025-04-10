"""
Database operations for py-AgentHive.
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
import datetime

from sqlalchemy import select, update, delete, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .models.worker import WorkerModel
from .models.task import Task
from .models.heartbeat import WorkerHeartbeat
from .models.system import SystemMetrics

logger = logging.getLogger(__name__)

async def get_worker(session: AsyncSession, worker_id: str) -> Optional[WorkerModel]:
    """Get a worker by ID."""
    stmt = select(WorkerModel).where(WorkerModel.worker_id == worker_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_workers(session: AsyncSession, active_only: bool = True, limit: int = 100, offset: int = 0) -> List[WorkerModel]:
    """Get all workers, optionally filtered by active status."""
    stmt = select(WorkerModel)
    if active_only:
        cutoff_time = datetime.datetime.now(datetime.timezone.utc).timestamp() - 120
        stmt = stmt.where(WorkerModel.last_seen >= cutoff_time)
    stmt = stmt.order_by(desc(WorkerModel.last_seen)).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def create_worker(session: AsyncSession, worker_id: str, hostname: Optional[str] = None,
                      ip_address: Optional[str] = None, capabilities: Optional[List[str]] = None,
                      tags: Optional[List[str]] = None) -> WorkerModel:
    """Create a new worker."""
    worker = WorkerModel(
        worker_id=worker_id,
        last_seen=datetime.datetime.now(datetime.timezone.utc),
        capabilities=capabilities or [],
        status="idle",
        extra_data={"hostname": hostname, "ip_address": ip_address, "tags": tags or []}
    )
    session.add(worker)
    await session.commit()
    await session.refresh(worker)
    return worker

async def update_worker_status(session: AsyncSession, worker_id: str, status: str,
                              current_task_id: Optional[str] = None) -> bool:
    """Update a worker's status."""
    stmt = update(WorkerModel).where(WorkerModel.worker_id == worker_id).values(
        status=status,
        last_seen=datetime.datetime.now(datetime.timezone.utc)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def record_worker_heartbeat(session: AsyncSession, worker_id: str, status: str,
                                 cpu_percent: Optional[float] = None, memory_percent: Optional[float] = None,
                                 disk_percent: Optional[float] = None, current_task_id: Optional[str] = None) -> Tuple[WorkerHeartbeat, bool]:
    """Record a worker heartbeat."""
    heartbeat = WorkerHeartbeat(
        worker_id=worker_id,
        timestamp=datetime.datetime.now(datetime.timezone.utc), # Datetime
        status=status,
        cpu_percent=cpu_percent,
        memory_percent=memory_percent,
        disk_percent=disk_percent,
        current_task_id=current_task_id
    )
    session.add(heartbeat)
    
    worker = await get_worker(session, worker_id)
    worker_updated = False
    if worker:
        worker.status = status
        worker.last_seen = heartbeat.timestamp
        worker_updated = True
    
    await session.commit()
    await session.refresh(heartbeat)
    return heartbeat, worker_updated

async def increment_worker_task_count(session: AsyncSession, worker_id: str) -> bool:
    """Increment a worker's task count."""
    worker = await get_worker(session, worker_id)
    if worker:
        worker.extra_data["tasks_processed"] = worker.extra_data.get("tasks_processed", 0) + 1
        worker.last_seen = datetime.datetime.now(datetime.timezone.utc)
        await session.commit()
        return True
    return False

async def get_task(session: AsyncSession, task_id: str) -> Optional[Task]:
    """Get a task by ID."""
    stmt = select(Task).where(Task.task_id == task_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_tasks(session: AsyncSession, status: Optional[str] = None, task_type: Optional[str] = None,
                   assigned_to: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Task]:
    """Get tasks, optionally filtered by status, type, or assignment."""
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    if task_type:
        stmt = stmt.where(Task.task_type == task_type)
    if assigned_to:
        stmt = stmt.where(Task.assigned_to == assigned_to)
    stmt = stmt.order_by(desc(Task.created_at)).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def create_task(session: AsyncSession, task_id: str, task_type: str, priority: int = 0,
                    data: Optional[Dict[str, Any]] = None) -> Task:
    """Create a new task."""
    task = Task(
        task_id=task_id,
        task_type=task_type,
        priority=priority,
        data=data or {},
        status="pending"
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def update_task_status(session: AsyncSession, task_id: str, status: str,
                            assigned_to: Optional[str] = None, result: Optional[Dict[str, Any]] = None,
                            error: Optional[str] = None) -> bool:
    """Update a task's status."""
    update_values = {"status": status, "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp()}
    if assigned_to is not None:
        update_values["assigned_to"] = assigned_to
    if status == "assigned" and assigned_to:
        update_values["started_at"] = datetime.datetime.now(datetime.timezone.utc).timestamp()
    if status == "completed" and result is not None:
        update_values["result"] = result
        update_values["completed_at"] = datetime.datetime.now(datetime.timezone.utc).timestamp()
    if status == "failed" and error is not None:
        update_values["error"] = error
        update_values["attempts"] = Task.attempts + 1
    
    stmt = update(Task).where(Task.task_id == task_id).values(**update_values)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def get_task_counts(session: AsyncSession) -> Dict[str, int]:
    """Get counts of tasks by status."""
    stmt = select(Task.status, func.count(Task.id)).group_by(Task.status)
    result = await session.execute(stmt)
    
    counts = {"pending": 0, "assigned": 0, "completed": 0, "failed": 0, "waiting": 0, "total": 0}
    for status, count in result:
        counts[status] = count
        counts["total"] += count
    return counts

async def record_system_metrics(session: AsyncSession, active_workers: int, idle_workers: int,
                              busy_workers: int, pending_tasks: int, assigned_tasks: int,
                              completed_tasks: int, failed_tasks: int, waiting_tasks: int,
                              avg_cpu_usage: float, avg_memory_usage: float, avg_disk_usage: float,
                              task_throughput: float) -> SystemMetrics:
    """Record system metrics."""
    metrics = SystemMetrics(
        timestamp=datetime.datetime.now(datetime.timezone.utc).timestamp(),
        active_workers=active_workers,
        idle_workers=idle_workers,
        busy_workers=busy_workers,
        pending_tasks=pending_tasks,
        assigned_tasks=assigned_tasks,
        completed_tasks=completed_tasks,
        failed_tasks=failed_tasks,
        waiting_tasks=waiting_tasks,
        avg_cpu_usage=avg_cpu_usage,
        avg_memory_usage=avg_memory_usage,
        avg_disk_usage=avg_disk_usage,
        task_throughput=task_throughput
    )
    session.add(metrics)
    await session.commit()
    await session.refresh(metrics)
    return metrics

async def get_system_metrics(session: AsyncSession, start_time: Optional[float] = None,
                            end_time: Optional[float] = None, limit: int = 100,
                            interval: str = "minute") -> List[SystemMetrics]:
    """Get system metrics within a time range."""
    end_time = end_time or datetime.datetime.now(datetime.timezone.utc).timestamp()
    start_time = start_time or (end_time - 86400)
    
    stmt = select(SystemMetrics).where(
        and_(SystemMetrics.timestamp >= start_time, SystemMetrics.timestamp <= end_time)
    ).order_by(desc(SystemMetrics.timestamp)).limit(limit)
    
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def cleanup_old_heartbeats(session: AsyncSession, retention_days: int = 7) -> int:
    """Clean up old worker heartbeats."""
    cutoff_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=retention_days)).timestamp()
    stmt = delete(WorkerHeartbeat).where(WorkerHeartbeat.timestamp < cutoff_time)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount

async def cleanup_old_metrics(session: AsyncSession, retention_days: int = 30) -> int:
    """Clean up old system metrics."""
    cutoff_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=retention_days)).timestamp()
    stmt = delete(SystemMetrics).where(SystemMetrics.timestamp < cutoff_time)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount

__all__ = [
    'get_worker', 'get_workers', 'create_worker', 'update_worker_status', 
    'record_worker_heartbeat', 'increment_worker_task_count', 'get_task', 
    'get_tasks', 'create_task', 'update_task_status', 'get_task_counts', 
    'record_system_metrics', 'get_system_metrics', 'cleanup_old_heartbeats', 
    'cleanup_old_metrics'
]
