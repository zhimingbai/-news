# 收藏相关API路由
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import favorite
from schemas.common import Res
from utils.auth import get_current_user_id

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# 检查收藏状态
@router.get(
    "/check",
    response_model=Res,
    summary="检查收藏状态",
    description="检查用户是否收藏了这一条新闻",
)
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    is_favorited = await favorite.is_news_favorite(db, user_id, news_id)
    return Res.success(data={"isFavorite": is_favorited})
