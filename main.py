# 应用入口文件
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

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


@app.get("/", response_model=Res)
async def root():
    return Res()


app.include_router(news.router)
