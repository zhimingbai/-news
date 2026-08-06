# 收藏数据验证模型（Pydantic模型）

from pydantic import BaseModel, Field

from schemas.news import NewsRespItem


class FavoriteReqList(BaseModel):
    """收藏列表请求参数模型"""

    page: int = Field(1, description="页码", gt=0)
    size: int = Field(10, description="每页数量", gt=0, le=100)


class FavoriteRespList(BaseModel):
    """收藏列表响应模型"""

    total: int = Field(..., description="总记录数")
    items: list[NewsRespItem] = Field(..., description="收藏的新闻列表")

    model_config = {"from_attributes": True}
