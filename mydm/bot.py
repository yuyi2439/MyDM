from typing import Callable, Any


class Bot:
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, func: Callable[[dict], Any]):
        self.handlers.append(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    async def event(self, e: dict):
        for handler in self.handlers:
            await handler(e)