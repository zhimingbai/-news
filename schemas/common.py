# 通用数据验证模型

from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Res(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None

    @classmethod
    def success(cls, data: Any = None, message: str = "success"):
        return cls(code=200, message=message, data=jsonable_encoder(data))

    @classmethod
    def error(cls, code: int = 400, message: str = "error", data: Any = None):
        raise HTTPException(
            status_code=code,
            detail=cls(
                code=code, message=message, data=jsonable_encoder(data)
            ).model_dump(),
        )
