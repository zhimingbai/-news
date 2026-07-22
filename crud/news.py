# 新闻相关数据库操作


from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News


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


async def get_news_list(
    db: AsyncSession,
    category_id: int,
    page: int = 1,
    page_size: int = 10,
):
    """获取新闻列表。

    Args:
        db: 数据库会话对象。
        category_id: 新闻分类ID。
        page: 页码。
        page_size: 每页数量。

    Returns:
        list[News]: 新闻对象列表。
    """
    skip = (page - 1) * page_size
    stmt = (
        select(News)
        .where(News.category_id == category_id)
        .offset(skip)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    """获取新闻分类下的新闻数量。

    Args:
        db: 数据库会话对象。
        category_id: 新闻分类ID。

    Returns:
        int: 新闻数量。
    """
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_news_detail(new_id: int, db: AsyncSession):
    """获取新闻详情。

    Args:
        new_id: 新闻ID。
        db: 数据库会话对象。

    Returns:
        News: 新闻对象，如果不存在则返回 None。
    """
    stmt = select(News).where(News.id == new_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def increase_view_count(new_id: int, db: AsyncSession):
    """增加新闻点击量。

    Args:
        new_id: 新闻ID。
        db: 数据库会话对象。

    Returns:
        bool: 是否成功增加点击量。
    """
    stmt = update(News).where(News.id == new_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_related_news(
    new_id: int, category_id: int, db: AsyncSession, limit: int = 5
):
    stmt = (
        select(News)
        .where(News.id != new_id, News.category_id == category_id)
        .order_by(News.views.desc(), News.publish_time.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    return [
        {
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "image": item.image,
            "author": item.author,
            "publishTime": item.publish_time,
            "categoryId": item.category_id,
            "views": item.views,
        }
        for item in related_news
    ]
