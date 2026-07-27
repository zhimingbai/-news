# 用户数据验证模型（Pydantic模型）

from pydantic import BaseModel


class UserRequest(BaseModel):
    """用户注册请求数据模型"""

    username: str
    password: str


class UserResponse(BaseModel):
    """用户基本响应数据模型（注册时返回）"""

    id: int
    username: str

    model_config = {"from_attributes": True}


class UserInfoResponse(UserResponse):
    """用户详细信息响应模型（登录/个人信息时返回）"""

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


class UserPasswordUpdateRequest(BaseModel):
    """用户密码更新请求数据模型"""

    old_password: str
    new_password: str
