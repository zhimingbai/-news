# 应用入口文件
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from routers import news
from schemas.common import Res

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
        if isinstance(exc.detail, dict)
        else Res(code=exc.status_code, message=str(exc.detail)).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=Res(
            code=422,
            message="请求参数校验失败",
            data=exc.errors(),
        ).model_dump(),
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=Res(code=exc.status_code, message=str(exc.detail)).model_dump(),
    )


@app.get("/", response_model=Res)
async def root():
    return Res()


app.include_router(news.router)
