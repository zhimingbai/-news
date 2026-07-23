# 用户相关数据库操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRequest
from utils import security


async def get_user_by_username(username: str, db: AsyncSession):
    """根据用户名获取用户信息。

    Args:
        username: 用户名。
        db: 数据库会话对象。

    Returns:
        User: 用户对象，如果不存在则返回 None。
    """
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def create_user(new_user: UserRequest, db: AsyncSession):
    """创建新用户。

    Args:
        new_user: 新用户请求对象，包含用户名和密码。
        db: 数据库会话对象。

    Returns:
        User: 创建成功的用户对象。
    """
    hashed_password = security.get_hash_password(new_user.password)
    user = User(username=new_user.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
