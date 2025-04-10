"""
提供時間處理相關功能的工具模組。
"""
import datetime
import logging

logger = logging.getLogger(__name__)

def convert_to_datetime(value, fallback=None) -> datetime.datetime:
    """
    將各種格式的時間數據轉換為 datetime 對象，如果無法轉換則返回 None 或指定的 fallback 值。
    
    支持以下格式:
    - datetime 對象
    - 整數/浮點數 (秒或毫秒級時間戳)
    - ISO 格式字符串
    
    Args:
        value: 待轉換的時間值
        fallback: 轉換失敗時的返回值，默認為 None
        
    Returns:
        datetime.datetime: 帶 UTC 時區的 datetime 對象，或 fallback 值
    """
    try:
        if value is None:
            return fallback
        
        if isinstance(value, datetime.datetime):
            return value if value.tzinfo else value.replace(tzinfo=datetime.timezone.utc)
        
        if isinstance(value, (int, float)):
            return datetime.datetime.fromtimestamp(
                value if value < 1e10 else value / 1000.0, 
                tz=datetime.timezone.utc
            )
        
        if isinstance(value, str):
            if value.lower() == 'null':
                return fallback
            try:
                if 'T' in value or '-' in value:
                    return datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError as e:
                logger.warning(f"Cannot parse ISO format time string: {value}, error: {e}")

            try:
                timestamp = float(value)
                return datetime.datetime.fromtimestamp(
                    timestamp if timestamp < 1e10 else timestamp / 1000.0, 
                    tz=datetime.timezone.utc
                )
            except ValueError as e:
                logger.warning(f"Cannot convert string to timestamp: {value}, error: {e}")

        
        logger.warning(f"not supported type: {type(value)}")

        return fallback
    except Exception as e:
        logger.error(f"時間轉換發生非預期錯誤: {e}")
        return fallback

def convert_to_timestamp(data: str) -> float:
    """
    將各種格式的時間數據轉換為時間戳。
    
    Args:
        data: 待轉換的時間值
        
    Returns:
        float: 秒級時間戳
    """
    dt = convert_to_datetime(data)
    if dt is None:
        return 0.0
    
    return dt.timestamp()

def convert_timestamp(timestamp_value, use_current_time_on_error=True):
    """
    將各種格式的時間戳轉換為 datetime 對象，如果出錯則返回當前時間。
    
    Args:
        timestamp_value: 待轉換的時間戳
        use_current_time_on_error: 轉換出錯時是否使用當前時間作為返回值
        
    Returns:
        datetime.datetime: 帶 UTC 時區的 datetime 對象
    """
    fallback = datetime.datetime.now(datetime.timezone.utc) if use_current_time_on_error else None
    result = convert_to_datetime(timestamp_value, fallback)
    
    if result is None and use_current_time_on_error:
        logger.warning(f"轉換時間戳失敗，使用當前時間: {timestamp_value}")
        return datetime.datetime.now(datetime.timezone.utc)
    
    return result

def datetime_to_iso(dt):
    """
    將 datetime 對象轉換為 ISO 8601 格式的字符串。
    
    Args:
        dt: datetime 對象
        
    Returns:
        str: ISO 格式的時間字符串
    """
    if dt is None:
        return None
    
    if not isinstance(dt, datetime.datetime):
        logger.warning(f"嘗試將非 datetime 對象轉換為 ISO 格式: {dt}")
        return None
    
    # 確保時區信息
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    
    return dt.isoformat()

def format_uptime(seconds: float) -> str:
    """Format uptime in seconds to a human-readable string."""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{int(days)}d")
    if hours > 0 or days > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{int(minutes)}m")
    parts.append(f"{int(seconds)}s")
    
    return " ".join(parts)