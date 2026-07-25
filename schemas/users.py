# 用户数据验证模型（Pydantic模型）

from pydantic import BaseModel


class UserRequest(BaseModel):
    """用户注册请求数据模型"""
    username: str
    password: str


class UserResponse(BaseModel):
    """用户响应数据模型"""
    id: int
    username: str

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """用户登录请求数据模型"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """登录成功返回的 Token 响应模型"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
