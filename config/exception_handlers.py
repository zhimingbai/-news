# 全局异常处理器
# 所有异常统一返回 { code, message, data } 格式

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from schemas.common import Res


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
