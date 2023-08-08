"""
定义所有自定义Exception和Error
"""


class ApiCallFailed(Exception):
    """Api调用失败"""
    
    def __init__(self, msg: str, wording: str):
        super().__init__(msg, wording)


class ApiCallTimeout(BaseException): """Api调用超时"""
# class EventReceiving(Exception): """Event接收中"""
# class EventNotReceiving(Exception): """Event还未开始接收"""
class WebSocketConnected(Exception): """WebSocket已连接"""
class WebSocketNotConnected(Exception): """WebSocket未连接"""