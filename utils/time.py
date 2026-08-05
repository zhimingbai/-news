# 通用时间工具
from datetime import datetime, timezone


def utcnow() -> datetime:
    """返回不带时区信息的 UTC 时间（兼容 MySQL DATETIME 列）。"""
    return datetime.now(timezone.utc).replace(tzinfo=None)
