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
        Favorite: 创建成功的收藏对象（含自增 id 与收藏时间）。
    """
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite
