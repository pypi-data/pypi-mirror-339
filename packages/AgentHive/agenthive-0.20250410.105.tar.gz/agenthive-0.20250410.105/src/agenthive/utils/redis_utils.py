import json
import datetime
import pytz

def serialize_for_redis(data: dict) -> dict:
    """
    Serialize a dictionary for Redis storage.

    Args:
        data (dict): The dictionary to serialize.

    Returns:
        dict: A dictionary with values serialized for Redis.
    """
    serialized_data = {}
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            serialized_data[key] = json.dumps(value)
        elif value is None:
            serialized_data[key] = ""  # Redis 不支持 None，轉為空字串
        elif isinstance(value, datetime.datetime):
            serialized_data[key] = value.astimezone(pytz.UTC).isoformat()            
        else:
            serialized_data[key] = str(value)  # 確保其他類型都轉為字串
    return serialized_data

def deserialize_from_redis(data: dict, intFields: list[str] = [], floatFields: list[str] = [], datetimeFields: list[str] = [], timestampFields: list[str] = [], jsonFields: list[str] = []) -> dict:
    """
    Deserialize a dictionary from Redis storage.

    Args:
        data (dict): The dictionary to deserialize.

    Returns:
        dict: A dictionary with values deserialized from Redis.
    """
    deserialized_data = {}
    if not data:
        return deserialized_data

    check_fields = {
        "int": set(intFields),
        "float": set(floatFields),
        "datetime": set(datetimeFields),
        "timestamp": set(timestampFields),
        "json": set(jsonFields),
    }

    for key, value in data.items():
        if key in check_fields["float"]:
            try:
                deserialized_data[key] = float(value)
            except (ValueError, TypeError):
                deserialized_data[key] = value
        elif key in check_fields["datetime"]:
            try:
                deserialized_data[key] = datetime.datetime.fromisoformat(value)
            except (ValueError, TypeError):
                deserialized_data[key] = value
        elif key in check_fields["timestamp"]:
            try:
                deserialized_data[key] = datetime.datetime.fromtimestamp(float(value), tz=datetime.timezone.utc)
            except (ValueError, TypeError):
                deserialized_data[key] = value
        elif key in check_fields["int"]:
            try:
                deserialized_data[key] = int(value)
            except (ValueError, TypeError):
                deserialized_data[key] = value
        elif key in check_fields["json"]:
            try:
                deserialized_data[key] = json.loads(value)
            except json.JSONDecodeError:
                deserialized_data[key] = value
        else:
            deserialized_data[key] = value

    return deserialized_data