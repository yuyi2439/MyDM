__all__ = [
    'ApiCallFailed',
    'ApiCallTimeout',
    'WebSocketNotConnected',
    'DataFormatError',
    'StopEventProcessing',
]


class ApiCallFailed(Exception):
    """Api调用失败"""

    def __init__(self, msg: str, wording: str):
        super().__init__(msg, wording)


class ApiCallTimeout(BaseException):
    """Api调用超时"""


class WebSocketNotConnected(Exception):
    """WebSocket未连接"""


class DataFormatError(TypeError):
    """数据格式错误"""


class StopEventProcessing(Exception):
    """截停事件处理"""
