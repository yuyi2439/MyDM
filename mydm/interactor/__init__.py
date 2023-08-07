import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable

import aiohttp

class Base(ABC):
    def __init__(
        self, url: str, *, 
        access_token: str = ''
        ):
        
        self.url = url
        self.access_token = access_token
        self.session = aiohttp.ClientSession()
        
        self.echos: list[int] = []
        self.msgs: list[dict] = []
        self.bots: list[Callable[[dict], Any]] = []
        self.conn = False
    
    def add_handler(self, bot: Callable[[dict], Any]):
        '''
        添加handler到`self.handlers`
        '''
        self.bots.append(bot)
    
    @abstractmethod
    async def start(self):
        '''
        连接OneBot实现 或 启动服务端
        '''
    
    @abstractmethod
    async def stop(self):
        '''
        断连OneBot实现 或 关闭服务端
        '''
    
    @abstractmethod
    async def send(self, action: str, params: dict|None = None) -> dict:
        '''
        向OneBot实现发送信息
        '''
    
    @abstractmethod
    async def _receive(self):
        '''
        接收消息并添加到`self.msgs`中
        '''
    
    @abstractmethod
    async def msg_handler(self):
        '''
        处理信息
        '''


class WebSocket(Base):
    async def start(self):
        self.ws_session = await self.session.ws_connect(self.url)
        self.conn = True
        
        # 连接上后立即开始接收信息
        asyncio.get_event_loop().create_task(self._receive())
    
    async def stop(self):
        await self.session.close()
        self.conn = False
        
    async def _receive(self):
        while True:
            msg = await self.ws_session.receive()
            self.msgs.append(msg.json())
            await self.msg_handler()


class WebSocketReverse(Base):
    # 我在这方面不是很熟悉，知道怎么定义的可以发issue或pr
    pass