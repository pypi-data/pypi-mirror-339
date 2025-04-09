#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：DongQing
@File    ：exception.py
@Time    ：2025/3/31
@Desc    ：
"""
__all__ = [
    'BaseException',
]

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import JSONResponse

from sthg_base_common.base_code.httpCodeEnmu import ResponseEnum

ERROR_TYPE_MAPPING = {
    "value_error.number.not_ge": "{},值不能小于:{}",
    "value_error.list.min_items": "{},元素个数至少为:{}",
    "value_error.str，": "{},元素个数至少为:{}",
    "value_error.missing": "字段必填",
    "type_error.integer": "必须是整数类型",
    "value_error.number.not_gt": "必须大于 {limit_value}",
}

KeyErrorChineseDict = {
    "": ""

}


# 定义一个自定义异常类
class CustomException(Exception):
    def __init__(self, response_enum: ResponseEnum, message: str = None):
        self.code = response_enum.HttpCode
        self.busiCode = response_enum.code
        self.busiMsg = response_enum.msg
        self.message = message or response_enum.msg
        super().__init__(self.message)


class BaseException(Exception):
    code: int
    busiMsg: str
    busiCode: str

    def __init__(self, resEnmu: ResponseEnum, msg: str = None):
        self.code = resEnmu.HttpCode
        self.busiCode = resEnmu.code
        self.busiMsg = f"{resEnmu.msg},{msg}" if msg else resEnmu.msg
        super().__init__(self.busiMsg)

    def __call__(self, *args, **kwargs) -> JSONResponse:
        return JSONResponse(status_code=self.code,
                            content={
                                "code": self.code,
                                "busiCode": self.busiCode,
                                "busiMsg": self.busiMsg
                            })


def register_exception_handlers(app: FastAPI):
    # 覆盖原生 HTTPException 处理器（处理其他 HTTP 错误）
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "busiMsg": exc.to_response(),
                "busiCode": exc.status_code
            },
        )

    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "busiMsg": str(exc),
                "busiCode": 400
            },
        )

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


# 自定义异常类
class TableNameError(Exception):
    __doc__ = "数据库表名命名规则验证错误"  # 数据库表名不符合命名规则时抛出的异常


class ColumnNameError(Exception):
    __doc__ = "数据库表属性命名规则验证错误"  # 数据库表属性不符合命名规则时抛出的异常


class RepetitiveError(Exception):
    __doc__ = "数据库表字段重复错误"  # 数据库表字段重复时抛出的异常


class DataNotFoundError(Exception):
    __doc__ = "数据库数据未找到"  # 查询数据库时未找到数据时抛出的异常


class ParamLackError(Exception):
    __doc__ = "缺少参数"  # 请求中缺少必要参数时抛出的异常


class ParamValidatedError(Exception):
    __doc__ = "自定义参数格式不正确"  # 参数格式不正确时抛出的异常


class AlreadyExistsError(Exception):
    __doc__ = "资源已存在"  # 资源已经存在时抛出的异常


class CustomRaiseError(Exception):
    __doc__ = "封装自定义报错"  # 封装自定义报错信息
    """
    使用框架自动捕获异常时候使用
    use:
        raise CustomRaiseError(*e.args, int)
    params:
        *e.args: 原始的错误信息
        int: 想要的业务报错信息code
    """
