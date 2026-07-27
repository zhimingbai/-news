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
    nickname: str | None = None
    avatar: str | None = None
    gender: str | None = None
    bio: str | None = None

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """用户登录请求数据模型"""

    username: str
    password: str


class UserUpdateRequest(BaseModel):
    """用户更新请求数据模型"""

    nickname: str | None = None
    avatar: str | None = None
    gender: str | None = None
    bio: str | None = None
    phone: str | None = None
