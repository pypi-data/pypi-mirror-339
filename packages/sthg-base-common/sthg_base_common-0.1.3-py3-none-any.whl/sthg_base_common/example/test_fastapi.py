import uvicorn
from fastapi import FastAPI

from sthg_base_common.base_code.exception import BaseException
from sthg_base_common.base_code.httpCodeEnmu import ResponseEnum
from sthg_base_common.base_code.response import BaseResponse
from sthg_base_common.example.test_utils import test_util

app = FastAPI()


@app.get("/test_response", name="测试返回")
def test_response():
    return BaseResponse(ResponseEnum.OK, data=None)


@app.get("/test_response_msg", name="测试添加msg")
async def test_response():
    data = test_util()
    return BaseResponse(ResponseEnum.OK, msg="正确返回", data=data)


@app.get("/test_response_data", name="测试添加数据")
def test_response():
    return BaseResponse(ResponseEnum.OK, data=[{"id": 1}], msg="正确返回")


@app.get("/test_reset_response_msg", name="测试重制返回")
def test_response():
    old_base = BaseResponse(ResponseEnum.OK, data=[{"id": 1}], msg="正确返回")
    old_base.build_reset(resEnmu=ResponseEnum.AccessDenied, msg="重制返回")
    return old_base


@app.get("/test_reset_response_count", name="测试增加count")
def test_response():
    return BaseResponse(ResponseEnum.OK, data=[{"id": 1}], msg="正确返回", count=10)


@app.get("/test_reset_is_success", name="测试is_success")
def test_response():
    old_base = BaseResponse(ResponseEnum.OK, data=[{"id": 1}], msg="正确返回")
    data = old_base.is_success()
    return BaseResponse(ResponseEnum.OK, data={"data": data})


@app.get("/test_expection", name="测试报错")
def test_expection():
    return BaseException(ResponseEnum.AccessDenied)


if __name__ == '__main__':
    uvicorn.run('test_fastapi:app', port=7080, host='0.0.0.0', proxy_headers=False, debug=False,
                timeout_keep_alive=300)
