# 新闻相关API路由

from fastapi import APIRouter

from schemas.common import Res

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get(
    "/category", response_model=Res, summary="获取新闻分类", description="获取新闻分类"
)
async def get_news_category_api():
    
    return Res()
