"""
定义实用工具
"""

import asyncio
import sys
from typing import Any

from .exceptions import ApiCallTimeout


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
            future = cls._echos.get(echo)
            if future:
                future.set_result(data)
    
    @classmethod
    async def wait(cls, echo: int, timeout: float) -> dict:
        """等待echo被set，返回整条消息"""
        future = asyncio.get_event_loop().create_future()
        cls._echos[echo] = future
        try:
            await asyncio.wait_for(future, timeout)
            return future.result()
        except asyncio.TimeoutError:
            raise ApiCallTimeout
        finally:
            cls._echos.pop(echo)

