import asyncio
import random

from mydm.interactor import WebSocket


class GoCqhttp(WebSocket):
    async def send(self, action: str, params: dict|None = None) -> dict:
        if self.conn == False:
            raise ConnectionError('连接未启动')
        while True:
            echo = random.randint(10000, 99999)
            if echo not in self.echos:
                break
        self.echos.append(echo)
        
        if params is None:
            await self.ws_session.send_json({
                'action': action,
                'echo': echo
            })
        else:
            await self.ws_session.send_json({
                'action': action,
                'params': params,
                'echo': echo
            })
        
        fut = asyncio.get_event_loop().create_future()
        while True:
            if self.msgs:
                await self.msg_handler(echo=echo, fut=fut)
                if fut.done():
                    return fut.result()
            else:
                await asyncio.sleep(0.001) # TODO 这里不是很完美
        
    async def msg_handler(self, *, echo: int, fut: asyncio.Future|None = None):
        for msg in self.msgs:
            if msg.get('echo') is None:
                self.msgs.remove(msg)
                for bot in self.bots:
                    await bot(msg)
            else:
                if fut is None or echo is None:
                    return
                if msg.get('echo') != echo:
                    return
                fut.set_result(msg)
                self.msgs.remove(msg)
