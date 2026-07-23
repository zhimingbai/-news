# 用户相关API路由

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import create_user, get_user_by_username
from schemas.common import Res
from schemas.users import UserRequest, UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/register",
    response_model=Res,
    summary="用户注册接口",
    description="用户注册接口，接收用户名和密码，返回注册结果",
)
async def register_api(user: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册接口
    """
    existing_user = await get_user_by_username(user.username, db)
    if existing_user:
        return Res.error(message="用户名已存在")
    created_user = await create_user(user, db)
    return Res.success(data={"user": UserResponse.model_validate(created_user)})
