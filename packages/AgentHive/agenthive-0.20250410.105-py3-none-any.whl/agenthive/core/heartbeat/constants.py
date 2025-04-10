"""
Heartbeat related constants and enums.
"""
from enum import Enum

# Redis key name constants
REDIS_KEY_PREFIX = "agenthive"

WORKER_REGISTERED_LOCK_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:worker:{{worker_id}}:lock"  # LOCK
WORKER_HASH_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:worker:{{worker_id}}"
WORKERS_SET_KEY = f"{REDIS_KEY_PREFIX}:workers"

HEARTBEAT_CHANNEL = f"{REDIS_KEY_PREFIX}:heartbeats"
WORKER_EVENTS_CHANNEL = f"{REDIS_KEY_PREFIX}:worker_events"

TASK_INFO_LOCK_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:task:info:{{task_id}}:lock"  # LOCK
TASK_INFO_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:task:info:{{task_id}}"  # HASH
TASKS_STATE_PENDING_SET_KEY = f"{REDIS_KEY_PREFIX}:tasks:pending"   # SET
TASKS_STATE_RUNNING_SET_KEY = f"{REDIS_KEY_PREFIX}:tasks:running"   # SET
TASKS_PENDING_WITH_TASK_TYPE_SET_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:tasks:pending:{{task_type}}" # SET
TASKS_TYPE_SUPPORTED_SET_KEY = f"{REDIS_KEY_PREFIX}:supported_task_types"  # SET

METRICS_INFO_TASK_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:metrics:{{coordinator_id}}:task"
METRICS_INFO_WORKER_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:metrics:{{coordinator_id}}:worker"
METRICS_INFO_SYSTEM_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:metrics:{{coordinator_id}}:system"

METRICS_INFO_SYSTEM_TASK_COMPLETED_TOTAL_KEY = f"{REDIS_KEY_PREFIX}:metrics:tasks_completed:{{minute_ts}}"
METRICS_INFO_SYSTEM_TASK_WITH_TASK_TYPE_COMPLETED_TOTAL_KEY_FORMAT = f"{REDIS_KEY_PREFIX}:metrics:task_type_completed:{{task_type}}:{{minute_ts}}"

QUERY_ALL_TASK_IDS = f"{REDIS_KEY_PREFIX}:tasks:info:*"

# Heartbeat event types
class HeartbeatEventType(str, Enum):
    """Heartbeat event type enum"""
    HEARTBEAT = "heartbeat"
    WORKER_ONLINE = "worker_online"
    WORKER_OFFLINE = "worker_offline"
    WORKER_STATUS_CHANGE = "worker_status_change"
    ERROR = "error"

# Heartbeat strategy enum
class HeartbeatStrategy(Enum):
    """Heartbeat strategy enum"""
    NONE = "none"            # Don't send any heartbeats
    STDOUT = "stdout"        # Only output to standard output (default)
    REDIS = "redis"          # Send to Redis publish/subscribe system
    COORDINATOR_API = "coordinator_api"  # Send via API call to coordinator
    
    @classmethod
    def from_string(cls, value: str) -> "HeartbeatStrategy":
        """Convert string to enum value, with backward compatibility"""
        if not value:
            return cls.STDOUT
            
        value = value.lower()
        for strategy in cls:
            if strategy.value == value:
                return strategy
        
        # If no matching strategy is found, use default strategy
        return cls.STDOUT
    
    def __str__(self) -> str:
        return self.value
