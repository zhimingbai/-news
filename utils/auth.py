# JWT 认证工具
# FastAPI 官方推荐的 OAuth2 + JWT 方案

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

# ---------- 配置 ----------
# 生产环境请通过环境变量或配置文件注入，不要硬编码
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# Bearer token 认证（Authorize 时手动粘贴 token）
bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """创建 JWT access token

    Args:
        data: 要编码到 token 中的数据（如 {"user_id": 1}）
        expires_delta: 可选的自定义过期时间

    Returns:
        str: 编码后的 JWT 字符串
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    """获取当前登录用户的 ID

    Args:
        credentials: HTTPAuthorizationCredentials 对象，包含 token 信息

    Raises:
        HTTPException: 如果 token 无效或缺失，则抛出 401 异常

    Returns:
        int: 当前登录用户的 ID
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user_id
