import sys
import asyncio
from typing import Any, Callable, Coroutine, TYPE_CHECKING

from mydm.event import *
from mydm.exceptions import ApiCallTimeout

if TYPE_CHECKING:
    from asyncio import Future

__all__ = [
    'EchoHandler',
    'EventHandler',
    'event_handler_sort',
]


class EchoHandler:
    _seq = 0
    _echos: dict[int, 'Future'] = {}

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
    def add_future(cls, echo: int):
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
        if not self.condition:
            return True
        try:
            for key, value in self.condition.items():
                if isinstance(value, list):
                    for v in value:
                        if condition[key] == v:
                            return True
                else:
                    if condition[key] == value:
                        return True
        except KeyError:
            return False
        return False

    async def __call__(self, raw_event: 'Event'):
        post_type = self.condition.get('post_type')
        match post_type:
            case 'message' | 'message_sent':
                event = EventMessage(raw_event)
            case 'request':
                event = EventRequest(raw_event)
            case 'notice':
                event = EventNotice(raw_event)
            case 'meta_event':
                event = EventMeta(raw_event)
            case _:
                event = raw_event
        handler = self.handler(event)
        if isinstance(handler, Coroutine):
            return await handler
        else:
            return handler


def event_handler_sort(handlers: list[EventHandler]) -> list[EventHandler]:
    """事件处理器排序"""
    def key(handler: EventHandler):
        value = handler.priority
        return (True, 0) if value == 0 else (value < 0, abs(value))
    sorted_handlers = [k for k in sorted(handlers, key=key)]
    return sorted_handlers
