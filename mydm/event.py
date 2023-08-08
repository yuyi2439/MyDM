"""
定义Event类型
"""

from typing import Literal, Union


class Event(dict):
    """
    将 dict 类型的Event封装为对象，并提供property函数来获取数据
    """
    
    @staticmethod
    def load(data: dict) -> Union['Event', dict]:
        """
        从dict构建Event
        """
        try:
            e = Event(data)
            _ = e.time, e.self_id, e.post_type
            return e
        except KeyError:
            return data
    
    @property
    def time(self) -> int:
        """事件发生的unix时间戳"""
        return self['time']
    
    @property
    def self_id(self) -> int:
        """收到事件的机器人的 QQ 号"""
        return self['self_id']

    @property
    def post_type(self) -> Literal['message', 'message_sent', 'request', 'notice', 'meta_event']:
        """收到事件的机器人的 QQ 号"""
        return self['post_type']

