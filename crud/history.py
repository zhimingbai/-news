# 历史记录相关数据库操作
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
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
