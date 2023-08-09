"""
定义交互器，用于和OneBot实现交互
包括Http和正向WebSocket通讯协议
包括调用Api和接收Event

InteractorApi：
    将信息发出去以后，异步等待返回，消息返回后由InteractorEvent处理，最后返回 ApiResponse 对象
InteractorEvent：
    使用event.py将接收到的Event(dict)，转换为Event对象，并且交由自己的handlers处理
"""

from abc import ABC, abstractmethod
import asyncio
from typing import Any, Callable

import aiohttp

try:
    import ujson as json
except ImportError:
    import json

from .type import ApiResponse
from .utils import EchoHandler
from .event import Event
from .exceptions import WebSocketConnected, WebSocketNotConnected

__all__ = [
    'Interactor',
    'InteractorApi',
    'InteractorEvent',
    'InteractorHttpApi',
    'InteractorHttpEvent',
    'InteractorWebSocket',
]


class Interactor:
    def __init__(
            self, url: str, *,
            access_token: str = '',
    ):

        self.url = url
        self.access_token = access_token
        self.session = aiohttp.ClientSession(json_serialize=json.dumps)


class InteractorApi(Interactor, ABC):
    def __init__(
            self, url: str, *,
            access_token: str = '',
            timeout: float = 10
    ):
        super().__init__(url, access_token=access_token)
        # 默认超时时长为10秒
        self._timeout = timeout

    @abstractmethod
    async def call(self, action: str, **params) -> 'ApiResponse':
        """请求OneBot实现，并获取返回值"""


class InteractorEvent(Interactor, ABC):
    def __init__(
            self, url: str, *,
            access_token: str = '',
    ):
        super().__init__(url, access_token=access_token)
        self.handlers: list[Callable[['Event'], Any]] = []

    @abstractmethod
    async def _receive(self):
        """接收Event"""

    async def receive(self):
        asyncio.get_event_loop().create_task(self._receive())


class InteractorHttpApi(InteractorApi):
    async def call(self, action: str, **params) -> 'ApiResponse':
        data = {
            'action': action,
            'params': params,
        }
        async with self.session.post(self.url, data=data, timeout=self._timeout) as msg:
            resp = await msg.json()
        resp = ApiResponse(resp)
        return resp


class InteractorHttpEvent(InteractorApi):
    """暂未实现"""


class InteractorWebSocket(InteractorApi, InteractorEvent):
    def __init__(
            self, url: str, *,
            access_token: str = '',
            timeout: float = 10
    ):
        super().__init__(url, access_token=access_token, timeout=timeout)
        self.conn = False

    async def connect(self):
        if self.conn:
            raise WebSocketConnected

        self.ws_session = await self.session.ws_connect(self.url)
        self.conn = True

        await self.receive()

    async def close(self):
        if not self.conn:
            raise WebSocketNotConnected

        await self.ws_session.close()
        self.conn = False

    async def call(self, action: str, **params) -> 'ApiResponse':
        if not self.conn:
            raise WebSocketNotConnected

        echo = EchoHandler.next()
        EchoHandler.add_fut(echo)
        data = {
            'action': action,
            'params': params,
            'echo': echo,
        }
        await self.ws_session.send_json(data)

        resp = await EchoHandler.wait(echo, self._timeout)
        resp = ApiResponse(resp)
        return resp

    async def _receive(self):
        while True:
            data = await self.ws_session.receive_json()
            if data.get('echo') is None:
                # 正常上报
                event = Event(data)
                if isinstance(event, Event):
                    asyncio.gather(*[handler(event)
                                   for handler in self.handlers])
            else:
                # echo上报
                EchoHandler.set(data)
