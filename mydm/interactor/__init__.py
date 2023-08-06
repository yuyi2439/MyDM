import asyncio
from abc import ABC, abstractmethod

import aiohttp

from mydm.bot import Bot


class Base(ABC):
    def __init__(
        self, url: str, *, 
        access_token: str = ''
        ):
        
        self.url = url
        self.access_token = access_token
        self.session = aiohttp.ClientSession()


class Http(Base):
    @abstractmethod
    async def send(self, action: str, params: dict) -> dict:
        '''
        向OneBot实现发送信息并获取返回值
        '''


class HttpWebhook(Base):
    @abstractmethod
    async def start(self):
        '''
        启动服务端
        '''
    
    @abstractmethod
    async def receive(self) -> dict:
        '''
        从OneBot实现获取信息
        '''


class WebSocketBase(Base):
    def __init__(
        self, url: str, bot: Bot, *, 
        access_token: str = ''
        ):
        
        super().__init__(url, access_token=access_token)
        self.bot = bot
        self.conn = False
    
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
    async def send(self, action: str, params: dict) -> dict:
        '''
        向OneBot实现发送信息 并 获取返回值
        '''
    
    @abstractmethod
    async def receive(self):
        '''
        消息接收并送到`self.bot.event`函数处理
        '''


class WebSocket(WebSocketBase):
    async def start(self):
        self.ws_session = await self.session.ws_connect(self.url)
        self.conn = True
        
        # 连接上后立即开始接收信息
        asyncio.get_event_loop().create_task(self.receive())
    
    async def stop(self):
        await self.session.close()
        self.conn = False


class WebSocketReverse(WebSocketBase):
    # 我在这方面不是很熟悉，知道怎么定义的可以发issue或pr
    pass