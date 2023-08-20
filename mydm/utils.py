"""
定义实用工具
"""

import asyncio
import sys
from typing import Any, Callable

from .event import *
from .exceptions import ApiCallTimeout

__all__ = [
    'EchoHandler',
    'EventHandler',
    'event_handler_sort',
]


class EchoHandler:
    _seq = 0
    _echos: dict[int, asyncio.Future] = {}

    @classmethod
    def next(cls) -> int:
        """获取下一个echo号"""
        seq = cls._seq
        cls._seq = (cls._seq + 1) % sys.maxsize
        return seq

    @classmethod
    def set(cls, data: dict):
        """设置echo"""
        echo = data.get('echo')
        if isinstance(echo, int):
            future = cls._echos[echo]
            future.set_result(data)

    @classmethod
    def add_fut(cls, echo: int):
        future = asyncio.get_event_loop().create_future()
        cls._echos[echo] = future

    @classmethod
    async def wait(cls, echo: int, timeout: float) -> dict:
        """等待echo被set，返回整条消息"""
        future = cls._echos[echo]
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise ApiCallTimeout
        finally:
            cls._echos.pop(echo)


class EventHandler:
    def __init__(
        self, handler: Callable[['Event'], Any], 
        priority: int = 0,
        condition: dict | None = None
        ):
        self.handler = handler
        self.priority = priority
        self.condition = condition or {}
    
    def assert_condition(self, condition: dict) -> bool:
        """判断condition"""
        try:
            for key, value in self.condition.items():
                if condition[key] != value:
                    return False
        except KeyError:
            return False
        return True
    
    def __call__(self, raw_event: 'Event') -> Any:
        post_type = self.condition.get('post_type')
        if post_type == 'message' or post_type == 'message_sent':
            return self.handler(EventMessage(raw_event))
        elif post_type == 'request':
            return self.handler(EventRequest(raw_event))
        elif post_type == 'notice':
            return self.handler(EventNotice(raw_event))
        elif post_type == 'meta_event':
            return self.handler(EventMeta(raw_event))
        else:
            return self.handler(raw_event)


def event_handler_sort(handlers: list[EventHandler]) -> list[EventHandler]:
    """事件处理器排序"""
    def key(handler: EventHandler):
        value = handler.priority
        return (True, 0) if value == 0 else (value < 0, abs(value))
    sorted_handlers = [k for k in sorted(handlers, key=key)]
    return sorted_handlers

