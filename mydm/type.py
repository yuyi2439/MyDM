"""
用于放置所有自定义数据类型
"""

from typing import Any

from .exceptions import ApiCallFailed

try:
    import ujson as json
except ImportError:
    import json


class ApiResponse(dict):
    def __init__(
            self, resp: dict | str
            ):
        super().__init__()
        if isinstance(resp, str):
            resp = json.loads(resp)
        if isinstance(resp, str): raise
        try:
            retcode = resp['retcode']
            if retcode == 0:
                # api调用成功
                self.update(resp['data'])
            elif retcode == 1:
                # api已提交 async 处理
                self.update({})
            else:
                # 操作失败
                raise ApiCallFailed(resp['msg'], resp['wording'])
        except KeyError:
            pass

