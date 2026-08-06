# 历史记录数据验证模型（Pydantic模型）
from pydantic import BaseModel, Field

from schemas.news import NewsRespItem


class HistoryPageReq(BaseModel):
    """历史记录分页请求参数模型"""

    page: int = Field(1, description="页码", ge=1)
    size: int = Field(10, description="每页数量", ge=1, le=100)


class HistoryRespList(BaseModel):
    """历史记录列表响应模型"""

    total: int = Field(..., description="总记录数")
    items: list[NewsRespItem] = Field(..., description="历史记录的新闻列表")

    model_config = {"from_attributes": True}
