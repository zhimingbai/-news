# Redis缓存配置
import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


redis_client = redis.Redis(
    host=REDIS_HOST,  # Redis服务器地址
    port=REDIS_PORT,  # Redis服务器端口
    db=REDIS_DB,  # Redis数据库编号
    decode_responses=True,  # 解码响应为字符串
)


async def get_cache(key: str):
    """获取字符串缓存。

    从 Redis 中读取指定 key 对应的原始字符串值，
    通常用于读取通过 set_cache 存入的字符串或已被序列化的 JSON 字符串。

    Args:
        key: 缓存的键名。

    Returns:
        str | None: 缓存的值；若 key 不存在或读取失败则返回 None。
    """
    try:
        value = await redis_client.get(key)
        return value
    except redis.RedisError as e:
        print(f"获取缓存失败: {e}")
        return None


async def get_json_cache(key: str):
    """获取 JSON 缓存。

    从 Redis 中读取指定 key 对应的值，并将其反序列化为 Python 对象。
    适用于存入时以 JSON 字符串保存的 dict/list 类型数据。

    Args:
        key: 缓存的键名。

    Returns:
        dict | list | None: 反序列化后的 Python 对象；
            若 key 不存在、内容为空或解析失败则返回 None。
    """
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except (redis.RedisError, json.JSONDecodeError) as e:
        print(f"获取 JSON 缓存失败: {e}")
        return None


async def set_cache(key: str, value: Any, expire: int = 3600):
    """设置缓存。

    将 value 写入 Redis 并设置过期时间；若 value 为 dict/list，
    会自动序列化为 JSON 字符串后再存入，方便后续用 get_json_cache 读取。

    Args:
        key: 缓存的键名。
        value: 要缓存的值，可为字符串或 dict/list 等可序列化对象。
        expire: 过期时间（秒），默认 3600 秒（1 小时）。

    Returns:
        bool: 是否设置成功；写入失败返回 False。
    """
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.set(key, value, ex=expire)
        return True
    except (redis.RedisError, TypeError, ValueError) as e:
        print(f"设置缓存失败: {e}")
        return False
