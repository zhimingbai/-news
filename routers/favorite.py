# 收藏相关API路由
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.favorite import (
    add_favorite,
    is_news_favorite,
    remove_all_favorites,
    remove_favorite,
)
from schemas.common import Res
from utils.auth import get_current_user_id

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get(
    "/check",
    response_model=Res,
    summary="检查收藏状态",
    description="检查用户是否收藏了这一条新闻",
)
async def check_favorite_api(
    news_id: int = Query(..., alias="newsId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """检查收藏状态"""
    is_favorited = await is_news_favorite(user_id, news_id, db)
    return Res.success(data={"isFavorite": is_favorited})


@router.post(
    path="/add",
    response_model=Res,
    summary="添加收藏",
    description="添加收藏记录",
)
async def add_favorite_api(
    news_id: int = Query(..., alias="newsId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """添加收藏记录"""
    favorite_record = await add_favorite(user_id, news_id, db)
    if favorite_record is None:
        return Res.error(message="已收藏过该新闻")
    return Res.success(
        data={"favoriteId": favorite_record.id},
        message="收藏成功",
    )


@router.delete(
    path="/remove",
    response_model=Res,
    summary="取消收藏",
    description="取消收藏记录",
)
async def remove_favorite_api(
    news_id: int = Query(..., alias="newsId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """取消收藏记录"""
    is_favorited = await remove_favorite(user_id, news_id, db)
    if not is_favorited:
        return Res.error(message="未找到收藏记录")
    return Res.success(message="取消收藏成功")


@router.delete(
    "",
    response_model=Res,
    summary="清空收藏列表",
    description="清空用户的所有收藏记录（集合级删除）",
)
async def remove_all_favorites_api(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """清空用户的所有收藏记录"""
    rowcount = await remove_all_favorites(user_id, db)
    return Res.success(
        message=f"已清空 {rowcount} 条收藏记录", data={"rowcount": rowcount}
    )
