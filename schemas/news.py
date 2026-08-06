# 新闻数据验证模型（Pydantic模型）
from datetime import datetime

from pydantic import BaseModel, Field


class NewsRespItem(BaseModel):
    """新闻列表响应项模型（历史、收藏列表复用）"""

    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    description: str | None = Field(None, description="新闻简介")
    image: str | None = Field(None, description="封面图片URL")
    author: str | None = Field(None, description="作者")
    views: int = Field(0, description="浏览量")
    publish_time: datetime = Field(..., description="发布时间")

    model_config = {"from_attributes": True}
