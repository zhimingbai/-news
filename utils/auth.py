# JWT 认证工具
# FastAPI 官方推荐的 OAuth2 + JWT 方案

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import get_user_by_id
from models.users import User

# ---------- 配置 ----------
# 生产环境请通过环境变量或配置文件注入，不要硬编码
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# OAuth2 密码流 scheme（tokenUrl 需与登录接口路径一致）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """创建 JWT access token

    Args:
        data: 要编码到 token 中的数据（如 {"user_id": 1}）
        expires_delta: 可选的自定义过期时间

    Returns:
        str: 编码后的 JWT 字符串
    """
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """从请求头 Authorization: Bearer <token> 中解析当前登录用户

    作为 FastAPI 依赖项使用，需要认证的路由注入此依赖即可。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 从数据库查询用户（确保用户仍存在）
    user = await get_user_by_id(user_id, db)
    if user is None:
        raise credentials_exception
    return user
