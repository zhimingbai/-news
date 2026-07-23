# 用户数据验证模型（Pydantic模型）


from pydantic import BaseModel


class UserRequest(BaseModel):
    """用户请求数据模型"""
    username: str
    password: str


class UserResponse(BaseModel):
    """用户响应数据模型"""
    username: str

    model_config = {"from_attributes": True}
