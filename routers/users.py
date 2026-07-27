# 用户相关API路由

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import (
    authenticate_user,
    create_user,
    get_user_by_id,
    get_user_by_username,
    update_user,
)
from schemas.common import Res
from schemas.users import LoginRequest, UserRequest, UserResponse, UserUpdateRequest
from utils.auth import create_access_token, get_current_user_id

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


@router.post(
    "/login",
    response_model=Res,
    summary="用户登录接口",
    description="用户登录接口，接收用户名和密码，返回 JWT Token",
)
async def login_api(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """用户登录接口"""
    user = await authenticate_user(login_data.username, login_data.password, db)
    if not user:
        return Res.error(message="用户名或密码错误")
    access_token = create_access_token(data={"user_id": user.id})
    return Res.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user),
        }
    )


@router.get(
    "/me",
    response_model=Res,
    summary="获取当前用户信息",
    description="获取当前登录用户的信息（需要登录）",
)
async def get_user_api(
    user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    """获取当前登录用户信息"""
    user = await get_user_by_id(user_id, db)
    if not user:
        return Res.error(message="用户不存在")
    return Res.success(data={"user": UserResponse.model_validate(user)})


@router.post(
    "/update",
    response_model=Res,
    summary="更新当前用户信息",
    description="更新当前登录用户的信息（需要登录）",
)
async def update_user_api(
    user_update: UserUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    user = await update_user(user_id, user_update, db)
    if user is None:
        user = await get_user_by_id(user_id, db)
    return Res.success(data={"user": UserResponse.model_validate(user)})
