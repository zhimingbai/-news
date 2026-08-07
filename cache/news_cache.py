# 新闻相关的缓存方法：新闻分类的读取与写入


from typing import Any

from config.cache_conf import get_json_cache, set_cache

CATEGORY_CACHE_KEY = "news:categories"  # 缓存新闻分类的键


async def get_category_cache():
    """获取新闻分类缓存。

    Returns:
        list[dict[str, Any]] | None: 新闻分类列表；
            若缓存不存在或读取失败则返回 None。
    """
    return await get_json_cache(CATEGORY_CACHE_KEY)


async def set_category_cache(data: list[dict[str, Any]], expire: int = 7200):
    """设置新闻分类缓存。

    Args:
        data: 新闻分类列表。
        expire: 过期时间（秒），默认 7200 秒（2 小时）。

    Returns:
        bool: 是否设置成功；写入失败返回 False。
    """
    return await set_cache(CATEGORY_CACHE_KEY, data, expire)
