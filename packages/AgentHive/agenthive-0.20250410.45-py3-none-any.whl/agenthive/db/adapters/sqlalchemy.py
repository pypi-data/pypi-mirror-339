"""
Unified SQLAlchemy database adapter implementation.
"""
import logging
import datetime
import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from sqlalchemy import Column, Integer, String, DateTime, JSON, select, func, desc, insert, update, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from ...core.heartbeat.models import HeartbeatData
from ...utils.datetime_utils import convert_to_datetime, convert_timestamp
from ..models import WorkerModel, TaskModel, WorkerHeartbeatModel, WorkerEventModel 
from .base import BaseDBAdapter

logger = logging.getLogger(__name__)

class SQLAlchemyAdapter(BaseDBAdapter):
    """
    Unified SQLAlchemy database adapter implementation for heartbeat system.
    This adapter handles both PostgreSQL and SQLite databases using SQLAlchemy's
    async functionality with appropriate drivers.
    """
    
    def __init__(self, connection_string: str, **options: Any) -> None:
        """
        Initialize the SQLAlchemy adapter.
        
        Args:
            connection_string: Database connection string (SQLAlchemy URL format)
            options: Additional database connection options
        """
        super().__init__(connection_string, **options)
        
        self.db_url = connection_string
        self.engine = None
        self.async_session = None
        self.workers_timestamp_field = 'last_seen'
        
        # 常用配置選項
        self.application_name = options.get('application_name', 'agenthive')
        self.pool_options = {
            'pool_size': options.get('max_size', 10),
            'max_overflow': options.get('max_overflow', 20),
            'pool_timeout': options.get('timeout', 60.0),
            'pool_recycle': options.get('pool_recycle', 1800),
            'pool_pre_ping': options.get('pool_pre_ping', True),
        }
        
        # 檢測數據庫類型
        self.db_type = self._detect_database_type(connection_string)
        logger.debug(f"Detected database type: {self.db_type}")
    
    def _detect_database_type(self, connection_string: str) -> str:
        """Detect database type from connection string."""
        conn_str = connection_string.lower()
        if 'postgresql' in conn_str or 'postgres' in conn_str:
            return 'postgresql'
        elif 'sqlite' in conn_str:
            return 'sqlite'
        else:
            logger.warning(f"Unable to detect database type from connection string: {connection_string}")
            return 'unknown'
    
    async def connect(self):
        try:
            # Append client_name to the URL if needed, or omit connect_args
            self.engine = create_async_engine(
                self.db_url,
                echo=False
                # Remove connect_args entirely, or use only supported args
            )

            self.async_session = sessionmaker(
                self.engine, 
                class_=AsyncSession, 
                expire_on_commit=False
            )

            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                logger.info("Database connection established")
                self._connected = True
        except Exception as e:
            logger.error(f"Failed to connect to database via SQLAlchemy: {e}")
            raise
   
    def _prepare_connection_string(self, conn_string: str) -> str:
        """Prepare connection string for the appropriate database driver."""
        if self.db_type == 'postgresql':
            if '+' not in conn_string and 'postgresql://' in conn_string:
                scheme_parts = conn_string.split('://', 1)
                if len(scheme_parts) == 2:
                    conn_string = f"postgresql+asyncpg://{scheme_parts[1]}"
            if 'application_name=' not in conn_string:
                conn_string += f"{'&' if '?' in conn_string else '?'}application_name={self.application_name}"
        
        elif self.db_type == 'sqlite':
            if '+' not in conn_string and 'sqlite://' in conn_string:
                conn_string = conn_string.replace('sqlite://', 'sqlite+aiosqlite://')
            if '/' in conn_string and not conn_string.endswith(':memory:'):
                parts = conn_string.split('://', 1)
                if len(parts) > 1:
                    path_part = parts[1]
                    if path_part.startswith('/'):
                        path_part = path_part[1:]
                    db_dir = os.path.dirname(path_part)
                    if db_dir and not os.path.exists(db_dir):
                        os.makedirs(db_dir, exist_ok=True)
        
        return conn_string
    
    def _get_engine_options(self) -> Dict[str, Any]:
        """Get database-specific engine options."""
        options = {'echo': False}
        if self.db_type == 'postgresql':
            options.update(self.pool_options)
        elif self.db_type == 'sqlite':
            options['connect_args'] = {"check_same_thread": False}
        return options
    
    async def _ensure_tables_exist(self) -> None:
        """Create database tables if they don't exist."""
        from ..models import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.debug("Ensured database tables exist")
    
    async def close(self) -> None:
        """Close the database connection."""
        if self.engine and self.is_connected():
            try:
                await self.engine.dispose()
                self._connected = False
                logger.debug("Disconnected from database")
            except Exception as e:
                logger.error(f"Error disconnecting from database: {e}")
    
    async def save_heartbeat(self, heartbeat_data: Dict[str, Any]) -> None:
        """Save heartbeat data to the database."""
        if not self.is_connected():
            await self.connect()
        
        if 'worker_id' not in heartbeat_data:
            raise ValueError("Heartbeat data must include a worker_id")
        
        logger.debug(f"Received heartbeat data: {heartbeat_data}")

        heartbeat_data['timestamp'] = heartbeat_data.get('timestamp', datetime.datetime.now(datetime.timezone.utc))
        heartbeat_data['timestamp'] = self._convert_to_datetime(heartbeat_data['timestamp'])

        heartbeat_obj = HeartbeatData.from_dict(heartbeat_data)
        
        logger.debug(f"Saving heartbeat data: {heartbeat_obj.to_dict()} via HeartbeatData.from_dict(heartbeat_data) ")

        async with self.async_session() as session:
            async with session.begin():
                # 第一步：检查并确保 worker 记录存在
                worker_id = heartbeat_data['worker_id']
                stmt = select(WorkerModel).where(WorkerModel.worker_id == worker_id)
                result = await session.execute(stmt)
                worker = result.scalar_one_or_none()

                if not worker:
                    worker = WorkerModel(
                        worker_id=worker_id, 
                        last_seen=heartbeat_obj.timestamp,
                        status=heartbeat_obj.status,
                    )
                    session.add(worker)
                    await session.flush()
 
                #stmt = insert(WorkerHeartbeatModel).values(**heartbeat_data)
                stmt = insert(WorkerHeartbeatModel).values(**(WorkerHeartbeatModel.from_heartbeat_data_object_to_dict(heartbeat_obj)))
                #db_record = WorkerHeartbeatModel.from_heartbeat_data_object_to_dict(heartbeat_obj)
                #stmt = insert(WorkerHeartbeatModel).values(**db_record)
                await session.execute(stmt)
                await self._update_worker_from_heartbeat(
                    session, 
                    heartbeat_obj
                )

    async def save_worker(self, data: Dict[str, Any]) -> None:
        """Save worker data to the database."""
        if not self.is_connected():
            await self.connect()

        if 'worker_id' not in data:
            raise ValueError("Event data must include worker_id")
        
        async with self.async_session() as session:
            async with session.begin():

                stmt = select(WorkerModel).where(WorkerModel.worker_id == data['worker_id'])
                result = await session.execute(stmt)
                worker = result.scalar_one_or_none()

                if not worker:
                    worker = WorkerModel(
                        worker_id=data['worker_id'], 
                        last_seen=data.get('last_heartbeat', datetime.datetime.now(datetime.timezone.utc)),
                        registered_at=data.get('registered_at', datetime.datetime.now(datetime.timezone.utc)),
                        hostname=data.get('hostname', None),
                        ip_address=data.get('ip_address', None),
                        version=data.get('version', None),
                        capabilities=data.get('capabilities', []),
                        configured_capabilities=data.get('configured_capabilities', []),
                        available_capabilities=data.get('available_capabilities', []),
                        tags=data.get('tags', {}),
                        status=data.get('status', 'unknown'),
                    )
                    session.add(worker)
                else:
                    update_data = {
                        'last_seen': data.get('last_heartbeat', datetime.datetime.now(datetime.timezone.utc)),
                        'hostname': data.get('hostname', None),
                        'ip_address': data.get('ip_address', None),
                        'version': data.get('version', None),
                        'capabilities': data.get('capabilities', []),
                        'configured_capabilities': data.get('configured_capabilities', []),
                        'available_capabilities': data.get('available_capabilities', []),
                        'tags': data.get('tags', {}),
                        'status': data.get('status', 'unknown'),
                    }
                    # update worker record
                    stmt = update(WorkerModel).where(WorkerModel.worker_id == data['worker_id']).values(**update_data)
                    await session.execute(stmt)

                await session.flush()
    
    async def save_worker_event(self, event_data: Dict[str, Any]) -> None:
        """Save worker event data to the database."""
        if not self.is_connected():
            await self.connect()
        
        if 'worker_id' not in event_data or 'event' not in event_data:
            raise ValueError("Event data must include worker_id and event")
        
        event_data['timestamp'] = event_data.get('timestamp', datetime.datetime.now(datetime.timezone.utc))
        event_data['timestamp'] = self._convert_to_datetime(event_data['timestamp'])
        
        event_obj = {
            'worker_id': event_data['worker_id'],
            'timestamp': event_data.get('timestamp', datetime.datetime.now(datetime.timezone.utc)),
            'event': event_data['event'],
            'data': event_data.get('data', {}),
            'extra_data': event_data.get('extra_data', {})
        }
        
        async with self.async_session() as session:
            async with session.begin():
                stmt = insert(WorkerEventModel).values(**event_obj)
                await session.execute(stmt)

    async def save_task(self, task_data: Dict[str, Any]) -> None:
        """Save task to database."""
        if not self.is_connected():
            await self.connect()
        
        if 'task_id' not in task_data or 'task_type' not in task_data:
            raise ValueError("Task task_data must include task_id and task_type")
    
        #data = task_data.get('data', '{}')
        #if isinstance(data, dict) or isinstance(data, list):
        #    data = json.dumps(data)
        #    logger.error(f"Converted task data to JSON: {data}")
        #try:
        #    data = json.loads(data)
        #except Exception as e:
        #    logger.error(f"Error parsing task data: {e}")
        #    data = {}

        task_obj = {
            'task_id': task_data['task_id'], 
            'task_type': task_data['task_type'],            
            'priority': task_data.get('priority', 0),
            'status': task_data.get('status', 'pending'),
            'assigned_to': task_data.get('assigned_to', None),
            'attempts': task_data.get('attempts', 0),
            'created_at': task_data.get('created_at', datetime.datetime.now(datetime.timezone.utc)),
        }

        #for time_field in ['started_at', 'completed_at']:
        #    if time_field in task_data:
        #        task_obj[time_field] = self._convert_timestamp(task_data[time_field])

        for time_field in ['created_at', 'started_at', 'completed_at']:
            if time_field in task_obj:
                task_obj[time_field] = self._convert_to_datetime(task_obj[time_field])

        # SELECT * FROM mytable WHERE field::text = 'null';
        for json_field in ['data', 'result', 'error']:
            data = task_data.get(json_field, None)
            if isinstance(data, str):
                if data == 'null':
                    data = None
                elif (data.startswith('{') and data.endswith('}')) or (data.startswith('[') and data.endswith(']')):
                    try:
                        data = json.loads(data)
                    except Exception as e:
                        logger.error(f"Error parsing task data: {e}")
                        data = {"error": "Error parsing task data", "raw": task_data.get(json_field, None)}
                else:
                    data = {"error": "Invalid JSON data", "raw": task_data.get(json_field, None)}
            task_obj[json_field] = data

        async with self.async_session() as session:
            async with session.begin():

                stmt = select(TaskModel).where(TaskModel.task_id == task_data['task_id'])
                result = await session.execute(stmt)
                if not result.scalar_one_or_none():
                    # Keep null values for data, result, error fields if they are None
                    for json_field in ['data', 'result', 'error']:
                        if json_field in task_obj and task_obj[json_field] is None:
                            del task_obj[json_field]
                    stmt = insert(TaskModel).values(**task_obj)
                    await session.execute(stmt)
                else:
                    if 'created_at' in task_obj:
                        del task_obj['created_at']
                    stmt = update(TaskModel).where(TaskModel.task_id == task_data['task_id']).values(**task_obj)
                    await session.execute(stmt)

    async def update_task(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """Update task in database."""
        if not self.is_connected():
            await self.connect()

        updated_result = False
        async with self.async_session() as session:
            async with session.begin():

                stmt = update(TaskModel).where(TaskModel.task_id == task_id).values(**update_data)
                result = await session.execute(stmt)
                if result.rowcount == 0:
                    logger.error(f"Task with ID {task_id} not found")
                else:
                    updated_result = True
                await session.commit()

        logger.debug(f"Updated task {task_id} with data: {update_data}, result: {updated_result}")
        return updated_result


    async def get_active_workers(self, timeout_seconds: int = 30) -> List[Dict[str, Any]]:
        """Get active workers from the database."""
        if not self.is_connected():
            await self.connect()
        
        cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=timeout_seconds)
        
        async with self.async_session() as session:
            stmt = (
                select(WorkerModel)
                .where(WorkerModel.last_seen > cutoff_time)
                .order_by(desc(WorkerModel.last_seen))
            )
            result = await session.execute(stmt)
            workers = result.scalars().all()
            #output = []
            #for worker in workers:
            #    worker_dict = self._orm_to_dict(worker)
            #    if not 'stats' in worker_dict:
            #        worker_dict['stats'] = worker_dict['extra_data']
            #    output.append(worker_dict)
            #return output
            return [self._orm_to_dict(worker) for worker in workers] if workers else []
    
    async def get_worker_history(self, worker_id: str, limit: int = 100, 
                                since: Optional[datetime.datetime] = None) -> List[Dict[str, Any]]:
        """Get a worker's heartbeat history."""
        if not self.is_connected():
            await self.connect()
        
        if since and not isinstance(since, datetime.datetime):
            since = self._convert_timestamp(since)
        
        async with self.async_session() as session:
            # 修改：使用 WorkerHeartbeat 替代 HeartbeatModel
            stmt = select(WorkerHeartbeatModel).where(WorkerHeartbeatModel.worker_id == worker_id)
            if since:
                stmt = stmt.where(WorkerHeartbeatModel.timestamp > since)
            stmt = stmt.order_by(desc(WorkerHeartbeatModel.timestamp)).limit(limit)
            
            result = await session.execute(stmt)
            heartbeats = result.scalars().all()
            return [self._orm_to_dict(heartbeat) for heartbeat in heartbeats]
    
    async def _update_worker_from_heartbeat(self, session, heartbeat_data_obj: HeartbeatData) -> None:
        """Update workers table from heartbeat data."""
        try:
            stmt = select(WorkerModel).where(WorkerModel.worker_id == heartbeat_data_obj.worker_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            worker_obj = {
                'worker_id': heartbeat_data_obj.worker_id,
                'last_seen': heartbeat_data_obj.timestamp,
                #'capabilities': json.dumps(heartbeat_data_obj.stats.get('capabilities', [])) if heartbeat_data_obj.stats else '[]',
                'status': heartbeat_data_obj.status,
                'version': heartbeat_data_obj.stats.get('version', None) if heartbeat_data_obj.stats else None,
                'extra_data': heartbeat_data_obj.stats,
            }
            logger.debug(f"Updating worker record: {worker_obj}")
            
            if existing:
                stmt = update(WorkerModel).where(WorkerModel.worker_id == heartbeat_data_obj.worker_id).values(**worker_obj)
            else:
                stmt = insert(WorkerModel).values(**worker_obj)
            
            await session.execute(stmt)
        except Exception as e:
            logger.error(f"Error updating worker record: {e}")
    
    def _convert_to_datetime(self, value):
        """Convert various timestamp formats to datetime object."""
        return convert_to_datetime(value)

    def _convert_timestamp(self, timestamp_value):
        """Convert various timestamp formats to datetime object."""
        return convert_timestamp(timestamp_value)
    
    def _orm_to_dict(self, orm_object):
        """Convert ORM object to dictionary."""
        result = {}
        for column in orm_object.__table__.columns:
            value = getattr(orm_object, column.name)
            
            if isinstance(value, datetime.datetime):
                result[column.name] = value.isoformat()
            elif isinstance(column.type, JSON):
                if value is None:
                    result[column.name] = None
                else:
                    try:
                        json_str = json.dumps(value)
                        result[column.name] = json.loads(json_str)
                    except Exception as e:
                        logger.error(f"Error processing JSON field {column.name}: {e}")
                        result[column.name] = {}
            else:
                result[column.name] = value
                
        return result
    
    async def get_pending_tasks(self, max_initial_tasks:int = 100, timeout_seconds: int = 30) -> List[Dict[str, Any]]:
        if not self.is_connected():
            await self.connect()
        if max_initial_tasks <= 0:
            max_initial_tasks = 100
        try:
            async with self.async_session() as session:
                stmt = select(TaskModel).where(TaskModel.status == "pending", TaskModel.task_type is not None).limit(max_initial_tasks)
                result = await session.execute(stmt)
                tasks = result.scalars().all()
                return [ json.loads(json.dumps(self._orm_to_dict(task))) for task in tasks] if tasks else []
        except Exception as e:
            logger.error(f"Error getting pending tasks: {e}")
        return []
    
    async def get_tasks_state_count(self, minutes: int = 2 ) -> Dict[str, int]:
        if not self.is_connected():
            await self.connect()
        try:
            async with self.async_session() as session:
                stmt = select(TaskModel.status, func.count(TaskModel.status)).group_by(TaskModel.status)
                if minutes > 0:
                    last_timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp() - (minutes * 60)
                    stmt = stmt.where(TaskModel.updated_at >= datetime.datetime.fromtimestamp(last_timestamp, tz=datetime.timezone.utc))
                result = await session.execute(stmt)
                task_counts = {status: count for status, count in result}
                return task_counts
        except Exception as e:
            logger.error(f"Error getting tasks state count: {e}")
        return {}

__all__ = ['SQLAlchemyAdapter']
