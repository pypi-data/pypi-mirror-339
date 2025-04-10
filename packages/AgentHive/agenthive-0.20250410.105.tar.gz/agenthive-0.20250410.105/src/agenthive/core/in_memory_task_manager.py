import redis.asyncio as redis   
import time
import logging
import json
import asyncio
import datetime

from agenthive.utils.redis_utils import (
    serialize_for_redis
)

logger = logging.getLogger(__name__)

from .heartbeat.constants import (
    REDIS_KEY_PREFIX,
    TASK_INFO_KEY_FORMAT, TASKS_STATE_PENDING_SET_KEY, TASKS_STATE_RUNNING_SET_KEY, 
    TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT, TASKS_TYPE_SUPPORTED_SET_KEY,
    WORKER_REGISTERED_LOCK_KEY_FORMAT, WORKER_HASH_KEY_FORMAT, WORKERS_SET_KEY,
    METRICS_INFO_SYSTEM_KEY_FORMAT, METRICS_INFO_TASK_KEY_FORMAT, METRICS_INFO_WORKER_KEY_FORMAT,
    METRICS_INFO_SYSTEM_TASK_COMPLETED_TOTAL_KEY, METRICS_INFO_SYSTEM_TASK_WITH_TASK_TYPE_COMPLETED_TOTAL_KEY_FORMAT,
    QUERY_ALL_TASK_IDS,
)

class InMemoryTaskManager:
    """Utility class for Redis operations related to tasks and workers."""

    def __init__(self, redis_url: str):
        self._redis_client = None
        try:
            self._redis_client = redis.from_url(redis_url)
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._redis_client = None
            raise

        # atomic pop
        # Redis Lua script to pop tasks from pending set
        self.customize_lua_script = """
local key = KEYS[1]
local count = tonumber(ARGV[1])
local tasks = redis.call('ZRANGE', key, 0, count - 1)
if #tasks > 0 then
    redis.call('ZREM', key, unpack(tasks))
end
return tasks
"""
        self.redis_pop_pending_tasks_script = self._redis_client.register_script(self.customize_lua_script)
        if not self.redis_pop_pending_tasks_script:
            logger.error("Failed to register Lua script for Redis.")
            raise Exception("Failed to register Lua script for Redis.")

    async def close(self):
        """
        關閉 Redis 連線。
        """
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None

    async def __del__(self):
        """
        當物件被刪除時，關閉 Redis 連線。
        """
        await self.close()

    async def pop_pending_tasks(self, task_type: str, max_count: int = 1) -> list[str]:
        """
        從 TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT 定義的資料中 pop 出 max_count 個資料。

        Args:
            task_type (str): 任務類型。
            max_count (int): 要 pop 出的資料數量。

        Returns:
            list[str]: 被 pop 出的 task_id 列表。
        """
        output = []
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return output
        

        key = TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT.format(task_type=task_type)
        # 使用 ZRANGE 取出最多 max_count 個元素
        #task_ids = await self._redis_client.zrange(key, 0, max_count - 1)
        #if task_ids:
        #    # 使用 ZREM 刪除取出的元素
        #    await self._redis_client.zrem(key, *task_ids)
        #    # 解碼 task_ids
        #    output = [task_id.decode('utf-8') for task_id in task_ids]
        
        task_ids = await self.redis_pop_pending_tasks_script(keys=[key], args=[max_count])
        if task_ids:
            # 解碼 task_ids
            output = [task_id.decode('utf-8') for task_id in task_ids]

        #logger.info(f"Pop pending tasks from Redis key: {key}, data:\n {output}")

        return output
    
    async def get_all_task_ids(self) -> list[str]:
        """
        從 TASK_INFO_KEY_FORMAT 撈出所有被定義的 task_id
        """
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return []

        keys = await self._redis_client.keys(QUERY_ALL_TASK_IDS)
        if not keys:
            return []
        return [key.decode('utf-8').split(":")[-1] for key in keys]

    async def add_and_check_multiple_tasks_exists(self, tasks: list[dict], ttl=3600) -> int:
        """
        檢查指定的 task_id 是否存在於 Redis 中，如果不存在則新增一筆並存儲 task info
        task info 存儲在 Hash 結構中，並設置過期時間
        """
        count = 0
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return count
        
        try:
            pipe = self._redis_client.pipeline()

            for task in tasks:
                task_id = task.get("task_id")
                task_type = task.get("task_type")

                if not task_id or not task_type:
                    logger.debug(f"Task {task} has missing task_id or task_type, skipping")
                    continue

                if not await self._redis_client.zadd(TASKS_STATE_PENDING_SET_KEY, {task_id: time.time()}):
                    logger.info(f"Task {task_id} already exists in pending tasks, skipping")
                    continue

                try:
                    store_key = TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT.format(task_type=task_type)
                    pipe.zadd(store_key, {task_id: time.time()})

                    task_info_key = TASK_INFO_KEY_FORMAT.format(task_id=task_id)
                    serialized_task_info = serialize_for_redis(task)
                    pipe.hmset(task_info_key, serialized_task_info)
                    pipe.expire(task_info_key, ttl)

                    pending_task_key = TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT.format(task_type=task_type)
                    pipe.zadd(pending_task_key, {task_id: time.time()})

                    count += 1
                except Exception as e:
                    logger.error(f"Error adding task info for task_id {task_id}, {task}:\n {e}")

                if count % 100 == 0:
                    await pipe.execute()

            if count % 100 != 0:
                await pipe.execute()
        except Exception as e:
            logger.error(f"Error adding tasks: {e}")

        return count


    async def add_and_check_task_exists(self, task_id: str, task_info: dict, ttl=3600) -> bool:
        """
        檢查指定的 task_id 是否存在於 Redis 中，如果不存在則新增一筆並存儲 task info
        task info 存儲在 Hash 結構中，並設置過期時間
        """
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return False

        # Step 1 - 試著先添加到 pending tasks 集合中
        added_to_pending = await self._redis_client.zadd(TASKS_STATE_PENDING_SET_KEY, {task_id: time.time()})
        if not added_to_pending:
            return False
        
        pipe = self._redis_client.pipeline()

        # Step 2 - 添加 task info 到 Redis
        task_info_key = TASK_INFO_KEY_FORMAT.format(task_id=task_id)
        serialized_task_info = serialize_for_redis(task_info)
        pipe.hmset(task_info_key, serialized_task_info)
        pipe.expire(task_info_key, ttl)

        # Step 3 - 添加 task_id 到 TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT 定義的集合中
        task_type = task_info.get("task_type", "")
        if task_type:
            pending_task_key = TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT.format(task_type=task_type)
            pipe.zadd(pending_task_key, {task_id: time.time()})
            await pipe.execute()
        else:
            await pipe.execute()
            logger.warning(f"Task type not found for task_id: {task_id}") 
        return True

    async def set_task_status_to_running(self, task_id: str, worker_id: str):
        """
        將指定的 task_id 設置為正在運行狀態: 添加到 running tasks 集合中
        """
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return

        pipe = self._redis_client.pipeline()

        # Step 1 - 將 task_id 從 pending tasks 集合中刪除
        pipe.zrem(TASKS_STATE_PENDING_SET_KEY, task_id)

        # Step 2 - 將 task_id 添加到 running tasks 集合中
        pipe.zadd(TASKS_STATE_RUNNING_SET_KEY, {task_id: time.time()})

        # Step 3 - 更新 task info 中的 worker_id
        task_info_key = TASK_INFO_KEY_FORMAT.format(task_id=task_id)
        pipe.hset(task_info_key, "worker_id", worker_id)

        result = await pipe.execute()
        logger.info(f"set_task_status_to_running: end: task_id: {task_id}, worker_id: {worker_id}, result: {result}")

    async def set_task_status_to_done(self, task_id: str, task_type: str = None, ttl: int = 180) -> None:
        """
        將指定的 task_id 設置為已完成狀態: 從 running tasks 集合中刪除
        """
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return
        
        logger.info(f"set_task_status_to_done begin: task_id: {task_id}")
        
        pipe = self._redis_client.pipeline()

        # Step 1 - 將 task_id 從 running tasks 集合中刪除
        pipe.zrem(TASKS_STATE_RUNNING_SET_KEY, task_id)

        # Step 2 - 刪除 task info
        task_info_key = TASK_INFO_KEY_FORMAT.format(task_id=task_id)
        pipe.delete(task_info_key)

        # Step 3 - update_service_metrics_task_done
        timestamp = int(time.time())
        minute_timestamp = timestamp - (timestamp % 60)  # 取得當前分鐘的起始時間戳
        
        # 更新總任務完成計數
        total_counter_key = METRICS_INFO_SYSTEM_TASK_COMPLETED_TOTAL_KEY.format(minute_ts=minute_timestamp)
        pipe.incr(total_counter_key)
        pipe.expire(total_counter_key, ttl)
        
        # 如果提供了任務類型，更新特定類型的計數
        if task_type:
            type_counter_key = METRICS_INFO_SYSTEM_TASK_WITH_TASK_TYPE_COMPLETED_TOTAL_KEY_FORMAT.format(
                task_type=task_type, minute_ts=minute_timestamp
            )
            pipe.incr(type_counter_key)
            pipe.expire(type_counter_key, ttl)

        result = await pipe.execute()
        logger.info(f"set_task_status_to_done end: task_id: {task_id}, result: {result}")

    async def get_task_info(self, task_id: str) -> dict:
        """
        從 Redis 中取出指定 task_id 的 task info
        """
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return {}
        task_info_key = TASK_INFO_KEY_FORMAT.format(task_id=task_id)
        task_info = await self._redis_client.hgetall(task_info_key)
        if task_info:
            # 將 Redis 中的 byte 轉為字串
            return {k.decode('utf-8'): v.decode('utf-8') for k, v in task_info.items()}
        return {}
    
    async def update_metrics_info(self, coordinator_id: str, task_metrics: dict, worker_metrics: dict, system_metrics: dict, ttl: int = 600) -> None:
        """
        更新 task/worker/system metrics 資訊到 Redis 中
        """

        logger.info(f"update_metrics_info: coordinator_id: {coordinator_id}\n\ntask_metrics: {task_metrics}\n\nworker_metrics: {worker_metrics}\n\nsystem_metrics: {system_metrics}\n\n")

        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return
        
        pipe = self._redis_client.pipeline()
        
        # Step 1 - 更新 task metrics
        if task_metrics:
            task_metrics_key = METRICS_INFO_TASK_KEY_FORMAT.format(coordinator_id=coordinator_id)
            serialized_task_metrics = serialize_for_redis(task_metrics)
            pipe.hmset(task_metrics_key, serialized_task_metrics)
            pipe.expire(task_metrics_key, ttl)

        # Step 2 - 更新 worker metrics
        if worker_metrics:
            worker_metrics_key = METRICS_INFO_WORKER_KEY_FORMAT.format(coordinator_id=coordinator_id)
            serialized_worker_metrics = serialize_for_redis(worker_metrics)
            pipe.hmset(worker_metrics_key, serialized_worker_metrics)
            pipe.expire(worker_metrics_key, ttl)

        # Step 3 - 更新 system metrics
        if system_metrics:
            system_metrics_key = METRICS_INFO_SYSTEM_KEY_FORMAT.format(coordinator_id=coordinator_id)
            serialized_system_metrics = serialize_for_redis(system_metrics)
            pipe.hmset(system_metrics_key, serialized_system_metrics)
            pipe.expire(system_metrics_key, ttl)

        await pipe.execute()

    async def register_worker(self, worker_id: str, worker_info: dict, capabilities: list) -> None:
        """
        註冊 worker 到 Redis 中
        """
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return
        
        await self.update_worker_info(worker_id, worker_info)

        lock_key = WORKER_REGISTERED_LOCK_KEY_FORMAT.format(worker_id=worker_id)
        got_lock = await self._redis_client.set(
            lock_key, 
            "1", 
            nx=True,
            ex=10
        )
        if not got_lock:
            logger.warning(f"Another instance is currently registering worker {worker_id}")
            # Wait briefly then continue (we'll update the record)
            await asyncio.sleep(0.5)
        try:
            pipe = self._redis_client.pipeline()

            # Update global supported task types
            store_key = TASKS_TYPE_SUPPORTED_SET_KEY
            pipe.sadd(store_key, *capabilities)
            pipe.expire(store_key, 86400)

            pipe.delete(lock_key)
            await pipe.execute()

        except Exception as e:
            logger.error(f"Failed to register worker {worker_id}: {e}")
            await self._redis_client.delete(lock_key)

        logger.info(f"Worker {worker_id} registered successfully.")

    async def update_worker_info(self, worker_id: str, worker_info: dict, ttl: int = 3600) -> None:
        try:

            serialized_worker_info = serialize_for_redis(worker_info)

            pipe = self._redis_client.pipeline()
            store_key = WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)
            pipe.hset(store_key, mapping=serialized_worker_info)
            pipe.expire(store_key, ttl)

            await pipe.execute()

        except Exception as e:
            logger.error(f"Failed to update worker info {worker_id}: {e}")

        #logger.info(f"Worker {worker_id} update successfully.")        

    async def update_task_status_from_heartbeat(self, heartbeat_info: dict) -> bool:
        """
        從 worker 的 heartbeat 更新 task 狀態
        """
        if not heartbeat_info:
            logger.error("Heartbeat info is empty.")
            return False
        
        worker_id = heartbeat_info.get("worker_id")
        if not worker_id:
            logger.error("Worker ID is missing in heartbeat info.")
            return False

        #
        #current_task_id = heartbeat_info.get("current_task_id")
        #if not current_task_id:
        #    logger.error("Current task ID is missing in heartbeat info.")
        #    return False
        
        return True

    """ => set_task_status_to_done
    async def update_service_metrics_task_done(self, task_type: str = None, ttl: int = 180) -> bool:
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return False
        
        try:
            pipe = self._redis_client.pipeline()
            timestamp = int(time.time())
            minute_timestamp = timestamp - (timestamp % 60)  # 取得當前分鐘的起始時間戳
            
            # 更新總任務完成計數
            total_counter_key = METRICS_INFO_SYSTEM_TASK_COMPLETED_TOTAL_KEY.format(minute_ts=minute_timestamp)
            pipe.incr(total_counter_key)
            pipe.expire(total_counter_key, ttl)
            
            # 如果提供了任務類型，更新特定類型的計數
            if task_type:
                type_counter_key = METRICS_INFO_SYSTEM_TASK_WITH_TASK_TYPE_COMPLETED_TOTAL_KEY_FORMAT.format(
                    task_type=task_type, minute_ts=minute_timestamp
                )
                pipe.incr(type_counter_key)
                pipe.expire(type_counter_key, ttl)
            
            await pipe.execute()
            return True
            
        except Exception as e:
            logger.error(f"Error updating service metrics for task completion: {e}")
            return False
    """

    async def get_service_metrics_per_minute(self, task_type: str = None, minutes: int = 5) -> dict:
        """
        獲取每分鐘完成的任務數量統計。
        
        Args:
            task_type (str, optional): 任務類型，用於獲取特定類型的任務計數。如果為None，則獲取總計數。
            minutes (int, optional): 要獲取的歷史分鐘數，默認為5分鐘。
        
        Returns:
            dict: 包含時間戳和對應的任務完成數量的字典
        """
        output = {
            "status": False, 
            "tasks_per_minute": 0, 
            "tasks_completed": {"total": [], "timestamp": []}, 
            "tasks_pending": 0,
            "tasks_running": 0,
            "active_workers": 0,
            "supported_task_types": [],
            "workers": [],
        }
        if not self._redis_client:
            logger.error("Redis client is not initialized.")
            return output
        
        try:
            current_timestamp = int(time.time())
            current_minute = current_timestamp - (current_timestamp % 60)

            #logger.info(f"Check timeslots: {[current_minute - (i * 60) for i in range(minutes)]}")

            for minute_ts in [current_minute - (i * 60) for i in range(minutes)]:
                # Get Task Info
                key = METRICS_INFO_SYSTEM_TASK_COMPLETED_TOTAL_KEY.format(
                    minute_ts=minute_ts
                ) if task_type is None else METRICS_INFO_SYSTEM_TASK_WITH_TASK_TYPE_COMPLETED_TOTAL_KEY_FORMAT.format(
                    task_type=task_type, minute_ts=minute_ts
                )
                #logger.info(f"Check key: {key}")
                count = await self._redis_client.get(key)
                output["tasks_completed"]["total"].append(int(count) if count else 0)
                output["tasks_completed"]["timestamp"].append({
                    "timestamp": datetime.datetime.fromtimestamp(minute_ts, tz=datetime.timezone.utc).isoformat(),
                    "count": int(count) if count else 0
                })

            output["tasks_per_minute"] = output["tasks_completed"]["total"][0] if output["tasks_completed"]["total"] else 0


            # 普通集合（Set）：sadd, srem, scard, smembers 等。
            # 有序集合（ZSet）：zadd, zrem, zcard, zrange 等。

            # Get Active Workers
            #_check_key_type = await self._redis_client.type(WORKERS_SET_KEY)
            #logger.info(f"check key ({WORKERS_SET_KEY}) type: {_check_key_type}")
            count = await self._redis_client.zcard(WORKERS_SET_KEY)
            output["active_workers"] = int(count) if count else 0

            #_check_key_type = await self._redis_client.type(TASKS_STATE_PENDING_SET_KEY)
            #logger.info(f"check key ({TASKS_STATE_PENDING_SET_KEY}) type: {_check_key_type}")
            count = await self._redis_client.zcard(TASKS_STATE_PENDING_SET_KEY)
            output["tasks_pending"] = int(count) if count else 0

            #_check_key_type = await self._redis_client.type(TASKS_STATE_RUNNING_SET_KEY)
            #logger.info(f"check key ({TASKS_STATE_RUNNING_SET_KEY}) type: {_check_key_type}")
            count = await self._redis_client.zcard(TASKS_STATE_RUNNING_SET_KEY)
            output["tasks_running"] = int(count) if count else 0

            # Get Supported Task Types
            #_check_key_type = await self._redis_client.type(TASKS_TYPE_SUPPORTED_SET_KEY)
            #logger.info(f"check key ({TASKS_TYPE_SUPPORTED_SET_KEY}) type: {_check_key_type}")

            _task_types = await self._redis_client.smembers(TASKS_TYPE_SUPPORTED_SET_KEY)
            if _task_types:
                output["supported_task_types"] = [task_type.decode('utf-8') for task_type in _task_types]

            # Get Workers
            worker_list_check = await self._redis_client.zrange(WORKERS_SET_KEY, 0, -1)
            #logger.info(f"check key ({WORKERS_SET_KEY}) worker_list_check: {worker_list_check}")
            if worker_list_check:
                worker_list = [worker.decode('utf-8') for worker in worker_list_check]
                #logger.info(f"check key ({WORKERS_SET_KEY}) worker_list: {worker_list}")
                for worker_id in worker_list:
                    worker_info_raw = await self._redis_client.hgetall(WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id))
                    #logger.info(f"check key ({WORKER_HASH_KEY_FORMAT.format(worker_id=worker_id)}) worker_info_raw: {worker_info_raw}")
                    if worker_info_raw:
                        worker_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in worker_info_raw.items()}

                        for fields in ['stats', 'resource_usage', 'configured_capabilities', 'available_capabilities', 'capabilities']:
                            if fields in worker_info:
                                try:
                                    _value = json.loads(worker_info[fields])
                                    worker_info[fields] = _value
                                except Exception as e:
                                    logger.error(f"Error parsing worker '{fields}' for {worker_id}: {e}")

                        output["workers"].append(worker_info)

            output["status"] = True
        except Exception as e:
            logger.error(f"Error getting tasks per minute metrics: {e}")

        return output
    
    async def debug_key(self, key):
        output = {
            "key" : key,
            "type": None,
            "count": 0,
        }
        key_type = await self._redis_client.type(key)
        output["type"] = key_type
        
        if key_type == b'zset':
            count = await self._redis_client.zcard(key)
            output["count"] = count
        elif key_type == b'set':
            count = await self._redis_client.scard(key)
            output["count"] = count
        return output