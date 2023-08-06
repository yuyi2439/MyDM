import asyncio
from typing import Coroutine


__version__ = "0.0.1"


def run(coro: Coroutine):
    asyncio.get_event_loop().create_task(coro)
    asyncio.get_event_loop().run_forever()