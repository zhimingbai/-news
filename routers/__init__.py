# 路由集中注册

from fastapi import FastAPI

from routers import favorite, history, news, users


def register_routers(app: FastAPI):
    """向 FastAPI 应用注册所有子路由"""
    app.include_router(news.router)
    app.include_router(users.router)
    app.include_router(favorite.router)
    app.include_router(history.router)
