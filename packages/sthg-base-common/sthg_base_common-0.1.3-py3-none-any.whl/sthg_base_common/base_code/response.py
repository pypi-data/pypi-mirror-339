import json
from typing import Any, Generic, Optional, TypeVar
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel
from pydantic import Field
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware

from sthg_base_common.base_code.httpCodeEnmu import ResponseEnum

T = TypeVar('T')


# 统一响应模型
class BaseResponse(BaseModel, Generic[T]):
    code: Optional[int] = Field(200, description="HTTP 状态码")
    busiCode: Optional[str] = Field("SUCCESS", description="业务状态码")
    busiMsg: Optional[str] = Field("success", description="业务消息")
    data: Optional[T] = Field(None, description="返回数据")
    count: Optional[T] = Field(None, description="返回数据")

    def __init__(self, resEnmu: ResponseEnum, data: Any, msg: str = None, *args, **kwargs):
        super().__init__(
            code=resEnmu.HttpCode,
            busiCode=resEnmu.code,
            busiMsg=f"{resEnmu.msg},{msg}" if msg else resEnmu.msg,
            data=data,
            *args,
            **kwargs
        )

    def __call__(self, *args, **kwargs) -> JSONResponse:
        return JSONResponse(status_code=self.code,
                            content={
                                "code": self.code,
                                "busiCode": self.busiCode,
                                "busiMsg": self.busiMsg,
                                "data": self.data if self.data else None,
                            })

    def is_success(self):
        is_success = False
        if self.code < 400:
            is_success = True
        return is_success

    def build_reset(self, resEnmu: ResponseEnum, msg=None):
        self.code = resEnmu.HttpCode
        self.busiCode = resEnmu.code
        self.busiMsg = f"{resEnmu.msg},{msg}" if msg else resEnmu.msg


# 自定义路由类
class BaseResponseRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        # 自动包装响应模型
        if "response_model" in kwargs and kwargs["response_model"] is not None:
            kwargs["response_model"] = BaseResponse[kwargs["response_model"]]
        else:
            kwargs["response_model"] = BaseResponse
        super().__init__(*args, **kwargs)

    def serialize_response(self, data: Any) -> Any:
        # 自动包装返回数据
        if not isinstance(data, BaseResponse):
            data = BaseResponse(data=data)
        return super().serialize_response(data)


# 自定义中间件处理响应头
class ResponseHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            print("erroe", e)
            # 直接返回标准错误响应
            return JSONResponse(
                status_code=500,
                content={
                    "code": 500,
                    "message": "Internal Server Error",
                    "data": None
                }
            )

        if isinstance(response, StreamingResponse):
            print("adfsadfasd")
            print(response)
            return response

        # 扩展支持的内容类型
        if "application/json" in response.headers.get("content-type", ""):
            try:
                body_bytes = b""
                async for chunk in response.body_iterator:
                    body_bytes += chunk
                content = json.loads(body_bytes.decode())

                # 关键修改：检查是否为有效BaseResponse结构
                if not all(key in content for key in ["code", "message", "data"]):
                    raise ValueError("Invalid response format")

                # 处理headers逻辑
                headers = content.pop("headers", {})
                mutable_headers = MutableHeaders(response.headers)
                for k, v in headers.items():
                    mutable_headers[k] = str(v)

                # 重建标准JSON响应
                return JSONResponse(
                    content=content,
                    status_code=response.status_code,
                    headers=dict(mutable_headers)
                )
            except Exception:
                # 返回原始错误响应（不修改格式）
                return JSONResponse(
                    content={
                        "code": 500,
                        "message": "Response processing failed",
                        "data": None
                    },
                    status_code=500
                )
        return response
