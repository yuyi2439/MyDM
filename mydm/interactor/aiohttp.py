import asyncio
import aiohttp

try:
    import ujson as json
except ImportError:
    import json

from mydm.type import ApiResponse
from mydm.event import Event
from mydm.utils import EchoHandler
from mydm.interactor import InteractorApi, InteractorEvent
from mydm.exceptions import WebSocketNotConnected

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from mydm.type import HANDLER


__all__ = [
    'InteractorApiHttp',
    'InteractorWebSocket',
]


class InteractorApiHttp(InteractorApi):
    def __init__(
        self, url: str,
        *,
        access_token: str = '',
        timeout: float = 10
    ):
        super().__init__(url, access_token=access_token, timeout=timeout)
        self.session = aiohttp.ClientSession(json_serialize=json.dumps)

    async def call(self, action: str, **params) -> 'ApiResponse':
        data = {
            'action': action,
            'params': params,
        }
        async with self.session.post(self.url, data=data, timeout=self._timeout) as msg:
            resp = await msg.json()
        resp = ApiResponse(resp)
        return resp


class InteractorWebSocket(InteractorApi, InteractorEvent):
    def __init__(
        self, url: str,
        *,
        access_token: str = '',
        timeout: float = 10
    ):
        super().__init__(url, access_token=access_token, timeout=timeout)
        self.session = aiohttp.ClientSession(json_serialize=json.dumps)
        self.handlers: list['HANDLER'] = []
        self.conn = False

    async def connect(self, event_loop: 'AbstractEventLoop'):
        self.ws_session = await self.session.ws_connect(self.url)
        self.conn = True
        await self.receive(event_loop)

    async def close(self):
        if not self.conn:
            raise WebSocketNotConnected
        await self.ws_session.close()
        self.conn = False

    async def call(self, action: str, **params) -> 'ApiResponse':
        if not self.conn:
            raise WebSocketNotConnected

        echo = EchoHandler.next()
        EchoHandler.add_future(echo)
        data = {
            'action': action,
            'params': params,
            'echo': echo,
        }
        await self.ws_session.send_json(data)

        resp = await EchoHandler.wait(echo, self._timeout)
        resp = ApiResponse(resp)
        return resp

    async def _receiver(self):
        while True:
            data = await self.ws_session.receive_json()
            if data.get('echo') is None:
                # 正常上报
                event = Event(data)
                asyncio.gather(*[handler(event) for handler in self.handlers])
            else:
                # echo上报
                EchoHandler.set(data)
