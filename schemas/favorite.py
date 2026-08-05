# 收藏数据验证模型（Pydantic模型）
from datetime import datetime

from pydantic import BaseModel, Field


class FavoriteReqList(BaseModel):
    """收藏列表请求参数模型"""

    page: int = Field(1, description="页码", gt=0)
    size: int = Field(10, description="每页数量", gt=0, le=100)


class FavoriteRespItem(BaseModel):
    """收藏列表响应项模型（真实新闻信息）"""

    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    description: str | None = Field(None, description="新闻简介")
    author: str | None = Field(None, description="作者")
    views: int = Field(..., description="浏览量")
    publish_time: datetime = Field(..., description="发布时间")

    model_config = {"from_attributes": True}


class FavoriteRespList(BaseModel):
    """收藏列表响应模型"""

    total: int = Field(..., description="总记录数")
    items: list[FavoriteRespItem] = Field(..., description="收藏的新闻列表")

    model_config = {"from_attributes": True}