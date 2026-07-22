# 应用入口文件

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.exception_handlers import register_exception_handlers
from routers import register_routers
from schemas.common import Res

app = FastAPI()

# 注册全局异常处理器
register_exception_handlers(app)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有子路由
register_routers(app)


@app.get("/", response_model=Res)
async def root():
    return Res()
