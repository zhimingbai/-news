# 历史记录相关API路由

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.history import add_history
from schemas.common import Res
from utils.auth import get_current_user_id

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post(
    "/add",
    response_model=Res,
    summary="添加历史记录",
    description="添加用户浏览新闻的历史记录",
)
async def add_history_api(
    new_id: int = Query(..., alias="newsId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """添加历史记录"""
    history = await add_history(new_id, user_id, db)
    return Res.success(data={"historyId": history.id})
