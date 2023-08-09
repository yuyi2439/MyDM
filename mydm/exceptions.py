"""
定义所有自定义Exception和Error
"""

__all__ = [
    'ApiCallFailed',
    'ApiCallTimeout',
    'WebSocketConnected',
    'WebSocketNotConnected',
    'DataFormatError',
]


class ApiCallFailed(Exception):
    """Api调用失败"""

    def __init__(self, msg: str, wording: str):
        super().__init__(msg, wording)


class ApiCallTimeout(BaseException):
    """Api调用超时"""


class WebSocketConnected(Exception):
    """WebSocket已连接"""


class WebSocketNotConnected(Exception):
    """WebSocket未连接"""


class DataFormatError(Exception):
    """Event格式错误"""
