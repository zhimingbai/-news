# 历史记录相关数据库操作
from typing import cast

from sqlalchemy import delete, func, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News
from schemas.history import HistoryPageReq
from utils.time import utcnow


async def add_history(news_id: int, user_id: int, db: AsyncSession):
    """添加/更新历史记录：同一用户对同一新闻只保留一条，重复浏览时刷新浏览时间。

    Args:
        news_id: 新闻ID。
        user_id: 用户ID。
        db: 数据库会话对象。

    Returns:
        History: 历史记录对象。
    """
    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    history = (await db.execute(stmt)).scalar_one_or_none()

    if history:
        # 已浏览过：只刷新浏览时间，不新增重复记录
        history.view_time = utcnow()
        await db.commit()
        await db.refresh(history)
        return history

    # 未浏览过：插入新记录
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    try:
        await db.commit()
    except IntegrityError:
        # 并发竞态兜底：另一请求刚插入成功，这里改为刷新浏览时间
        await db.rollback()
        history = (await db.execute(stmt)).scalar_one()
        history.view_time = utcnow()
        await db.commit()
    await db.refresh(history)
    return history


async def remove_history(history_id: int, user_id: int, db: AsyncSession):
    """删除单个历史记录

    Args:
        history_id: 历史记录ID。
        user_id: 用户ID。
        db: 数据库会话对象。

    Returns:
        bool: 删除成功返回 True，未找到记录返回 False。
    """
    stmt = select(History).where(History.id == history_id, History.user_id == user_id)
    history = (await db.execute(stmt)).scalar_one_or_none()
    if not history:
        return False
    await db.delete(history)
    await db.commit()
    return True


async def remove_all_history(user_id: int, db: AsyncSession):
    """删除用户的所有历史记录

    Args:
        user_id: 用户ID。
        db: 数据库会话对象。
    Returns:
        int: 删除的历史记录数量。
    """
    stmt = delete(History).where(History.user_id == user_id)
    result = cast(CursorResult, await db.execute(stmt))
    await db.commit()
    return result.rowcount


async def get_history(page_info: HistoryPageReq, user_id: int, db: AsyncSession):
    """获取用户的历史记录列表（含真实新闻信息）。

    历史表里只有 (user_id, news_id) 记录，这里先分页查出历史记录，
    再根据 news_id 批量查询对应的真实新闻，并返回历史记录总数。

    Args:
        page_info: 分页信息。
        user_id: 用户ID。
        db: 数据库会话对象。

    Returns:
        dict: 包含 "total"（历史记录总数）和 "items"（当前页新闻列表）的字典。
    """
    offset = (page_info.page - 1) * page_info.size
    limit = page_info.size
    total_stmt = select(func.count(History.id)).where(History.user_id == user_id)
    total = (await db.execute(total_stmt)).scalar_one()

    history_stmt = (
        select(History)
        .where(History.user_id == user_id)
        .offset(offset)
        .limit(limit)
        .order_by(History.view_time.desc())
    )
    history_list = (await db.execute(history_stmt)).scalars().all()
    news_id = [history.news_id for history in history_list]
    if not news_id:
        return {"total": total, "items": []}
    news_stmt = select(News).where(News.id.in_(news_id))
    news_list = (await db.execute(news_stmt)).scalars().all()
    news_map = {new.id: new for new in news_list}
    items = [news_map[new_id] for new_id in news_id if new_id in news_map]
    return {"total": total, "items": items}
