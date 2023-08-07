from typing import Callable, Any

from mydm.interactor import Base as BaseInteractor

class Bot:
    def __init__(self, interactor: BaseInteractor):
        self.interactor = interactor
        self.interactor.add_handler(self)
        
        self.handlers: list[Callable[[dict], Any]] = []
    
    def add_handler(self, func: Callable[[dict], Any]):
        self.handlers.append(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    async def __call__(self, e: dict):
        for handler in self.handlers:
            await handler(e)

    async def send(self, action: str, params: dict|None = None) -> dict:
        return await self.interactor.send(action, params)
        