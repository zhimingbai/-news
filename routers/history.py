# 历史记录相关API路由

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.history import add_history, get_history, remove_all_history, remove_history
from schemas.common import Res
from schemas.history import HistoryPageReq, HistoryRespList
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


@router.delete(
    "/delete",
    response_model=Res,
    summary="删除历史记录",
    description="删除用户浏览新闻的历史记录",
)
async def delete_history_api(
    history_id: int = Query(..., alias="historyId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除单个历史记录"""
    is_delete = await remove_history(history_id, user_id, db)
    if is_delete is False:
        return Res.error(message="未找到历史记录")
    return Res.success(message="删除成功")


@router.delete(
    "/delete_all",
    response_model=Res,
    summary="删除所有历史记录",
    description="删除用户浏览新闻的所有历史记录",
)
async def delete_all_history_api(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除所有历史记录"""
    total = await remove_all_history(user_id, db)
    return Res.success(message=f"成功删除 {total} 条历史记录")


@router.post(
    "/list",
    response_model=Res,
    summary="获取历史记录列表",
    description="获取用户浏览新闻的历史记录列表",
)
async def get_history_list_api(
    page_info: HistoryPageReq,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取历史记录列表"""
    history_list = await get_history(page_info, user_id, db)
    return Res.success(data=HistoryRespList.model_validate(history_list))
