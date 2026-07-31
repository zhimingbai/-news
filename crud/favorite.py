# 收藏相关数据库操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite


async def is_news_favorite(user_id: int, news_id: int, db: AsyncSession):
    """检查用户是否已收藏某条新闻。

    Args:
        user_id: 用户ID。
        news_id: 新闻ID。
        db: 数据库会话对象。

    Returns:
        bool: 已收藏返回 True，未收藏返回 False。
    """
    query = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    # 是否有收藏记录
    return result.scalar_one_or_none() is not None


async def add_favorite(user_id: int, news_id: int, db: AsyncSession):
    """添加收藏记录。

    Args:
        user_id: 用户ID。
        news_id: 新闻ID。
        db: 数据库会话对象。

    Returns:
        Favorite | None: 添加成功返回收藏记录对象，已收藏过返回 None。
    """
    # 已收藏过则直接返回 None，避免重复插入触发唯一约束
    query = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    if result.scalar_one_or_none() is not None:
        return None

    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(user_id: int, news_id: int, db: AsyncSession):
    """取消收藏记录。

    Args:
        user_id: 用户ID。
        news_id: 新闻ID。
        db: 数据库会话对象。
    Returns:
        bool: 取消收藏成功返回 True，未找到收藏记录返回 False。
    """
    query = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    favorite = result.scalar_one_or_none()
    if not favorite:
        return False
    await db.delete(favorite)
    await db.commit()
    return True
