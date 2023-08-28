from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from mydm.type import HANDLER, ApiResponse

__all__ = [
    'InteractorApi',
    'InteractorEvent',
]


class InteractorApi(ABC):
    def __init__(
        self, url: str,
        *,
        access_token: str = '',
        timeout: float = 10
    ):
        self.url = url
        self.access_token = access_token
        self._timeout = timeout

    @abstractmethod
    async def call(self, action: str, **params) -> 'ApiResponse':
        """请求并获取返回值"""


class InteractorEvent(ABC):
    def __init__(
        self, url: str,
        *,
        access_token: str = '',
    ):
        self.url = url
        self.access_token = access_token
        self.handlers: list[HANDLER] = []

    @abstractmethod
    async def _receiver(self):
        """接收Event"""

    async def receive(self, event_loop: 'AbstractEventLoop'):
        event_loop.create_task(self._receiver())
