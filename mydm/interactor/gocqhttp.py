from mydm.interactor import WebSocket


class GoCqhttp(WebSocket):
    async def send(self, action: str, params: dict|None = None):
        if self.conn == False:
            raise ConnectionError('Connection is closed.')
        if params == None:
            params = {}
        data = {
            'action': action,
            'params': params
        }
        return await self.ws_session.send_json(data)
    
    async def receive(self):
        while True:
            msg = await self.ws_session.receive()
            await self.bot.event(msg.json())