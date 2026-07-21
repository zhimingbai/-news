# 新闻相关API路由

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import get_categories
from schemas.common import Res

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get(
    "/category", response_model=Res, summary="获取新闻分类", description="获取新闻分类"
)
async def get_news_category_api(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """获取新闻分类列表"""
    categories = await get_categories(skip=skip, limit=limit, db=db)
    return Res.success(data=categories)
