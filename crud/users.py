# 用户相关数据库操作

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserPasswordUpdateRequest, UserRequest, UserUpdateRequest
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


async def get_user_by_id(user_id: int, db: AsyncSession):
    """根据用户ID获取用户信息。

    Args:
        user_id: 用户ID。
        db: 数据库会话对象。

    Returns:
        User: 用户对象，如果不存在则返回 None。
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def authenticate_user(username: str, password: str, db: AsyncSession):
    """验证用户凭据。

    Args:
        username: 用户名。
        password: 明文密码。
        db: 数据库会话对象。

    Returns:
        User: 验证通过返回用户对象，否则返回 None。
    """
    user = await get_user_by_username(username, db)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
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


async def update_user(user_id: int, updated_data: UserUpdateRequest, db: AsyncSession):
    """更新用户信息（按需更新，仅修改客户端传了的字段）。

    Args:
        user_id: 用户ID（来自 JWT，无需再校验存在性）。
        updated_data: 用户更新请求对象，包含可选的昵称、头像、性别、简介和手机号。
        db: 数据库会话对象。

    Returns:
        User: 更新后的用户对象。
    """
    # 仅提取客户端显式传了的字段，避免将未传字段覆盖为 None
    update_fields = updated_data.model_dump(exclude_unset=True)
    if not update_fields:
        return None

    user = await db.get(User, user_id)
    for field, value in update_fields.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def update_user_password(
    user_id: int, data: UserPasswordUpdateRequest, db: AsyncSession
):
    """更新用户密码。

    Args:
        user_id: 用户ID（来自 JWT，无需再校验存在性）。
        data: 用户密码更新请求对象，包含新密码。
        db: 数据库会话对象。

    Returns:
        User: 更新后的用户对象。
    """
    user = await db.get(User, user_id)
    if not user:
        return None
    if not security.verify_password(data.old_password,user.password):
        return False
    user.password = security.get_hash_password(data.new_password)
    await db.commit()
    await db.refresh(user)
    return user
