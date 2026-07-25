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
    """登录成功返回的 Token 响应模型（包含用户信息）"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class OAuth2TokenResponse(BaseModel):
    """OAuth2 标准 Token 响应（Swagger Authorize 按钮需要的最外层格式）"""
    access_token: str
    token_type: str = "bearer"
