# 新闻相关数据库操作


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category


async def get_categories(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
):
    """获取新闻分类列表。

    Args:
        db: 数据库会话对象。
        skip: 跳过的记录数，用于分页。
        limit: 返回的最大记录数，用于分页。

    Returns:
        list[Category]: 新闻分类对象列表。
    """
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
