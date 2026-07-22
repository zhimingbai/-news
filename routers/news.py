# 新闻相关API路由

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import (
    get_categories,
    get_news_count,
    get_news_detail,
    get_news_list,
    get_related_news,
    increase_view_count,
)
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


@router.get(
    "/list", response_model=Res, summary="获取新闻列表", description="获取新闻列表"
)
async def get_news_list_api(
    category_id: int = Query(..., alias="categoryId", description="新闻分类ID"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, le=100, alias="pageSize", description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """获取新闻列表"""
    news_list = await get_news_list(db, category_id, page, page_size)
    total = await get_news_count(db, category_id)
    return Res.success(data={"news_list": news_list, "total": total})


@router.get(
    "/detail", response_model=Res, summary="获取新闻详情", description="获取新闻详情"
)
async def get_news_detail_api(
    new_id: int = Query(..., description="新闻ID", alias="id"),
    db: AsyncSession = Depends(get_db),
):
    """获取新闻详情，并增加浏览量，同时返回相关的新闻列表"""
    new = await get_news_detail(new_id, db)
    if not new:
        return Res.error(message="新闻不存在")
    result = await increase_view_count(new_id, db)
    if result is False:
        return Res.error(message="浏览量增加失败")
    related_news = await get_related_news(new_id, new.category_id, db)
    data = {
        "id": new.id,
        "title": new.title,
        "description": new.description,
        "content": new.content,
        "image": new.image,
        "author": new.author,
        "publishTime": new.publish_time,
        "categoryId": new.category_id,
        "views": new.views + 1,
        "related_news": related_news,
    }
    return Res.success(data=data)
