# 全局异常处理器
# 所有异常统一返回 { code, message, data } 格式
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from schemas.common import Res

# 开发模式：返回详细错误信息；生产模式：返回简化错误信息
DEBUG_MODE = True  # 教学项目保持开启


def register_exception_handlers(app: FastAPI):
    """向 FastAPI 应用注册全局异常处理器"""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """处理所有 HTTPException（包括 Res.error 主动抛出的）"""
        # 如果 detail 已是 {code, message, data} 格式，直接返回
        if isinstance(exc.detail, dict) and "code" in exc.detail and "message" in exc.detail:
            content = exc.detail
        else:
            content = Res(
                code=exc.status_code, message=str(exc.detail)
            ).model_dump()
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """处理 Pydantic 请求参数校验失败"""
        return JSONResponse(
            status_code=422,
            content=Res(
                code=422,
                message="请求参数校验失败",
                data=exc.errors(),
            ).model_dump(),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """处理数据库完整性约束错误（如用户名重复、外键不存在）"""
        error_msg = str(exc.orig)

        # 判断具体的约束错误类型
        if "Duplicate entry" in error_msg or "username_UNIQUE" in error_msg:
            detail = "用户名已存在"
        elif "FOREIGN KEY" in error_msg:
            detail = "关联数据不存在"
        else:
            detail = "数据约束冲突，请检查输入"

        # 开发模式下返回详细错误信息
        error_data = None
        if DEBUG_MODE:
            error_data = {
                "error_type": "IntegrityError",
                "error_detail": error_msg,
                "path": str(request.url),
            }

        return JSONResponse(
            status_code=400,
            content=Res(code=400, message=detail, data=error_data).model_dump(),
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        """处理 SQLAlchemy 数据库错误"""
        error_data = None
        if DEBUG_MODE:
            error_data = {
                "error_type": type(exc).__name__,
                "error_detail": str(exc),
                # 格式化异常信息为字符串，方便日志记录和调试
                "traceback": traceback.format_exc(),
                "path": str(request.url),
            }

        return JSONResponse(
            status_code=500,
            content=Res(
                code=500, message="数据库操作失败，请稍后重试", data=error_data
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理所有未捕获的异常"""
        error_data = None
        if DEBUG_MODE:
            error_data = {
                "error_type": type(exc).__name__,
                "error_detail": str(exc),
                # 格式化异常信息为字符串，方便日志记录和调试
                "traceback": traceback.format_exc(),
                "path": str(request.url),
            }

        return JSONResponse(
            status_code=500,
            content=Res(
                code=500, message="服务器内部错误", data=error_data
            ).model_dump(),
        )
