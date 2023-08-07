import asyncio
from typing import Coroutine


def run(coro: Coroutine):
    asyncio.get_event_loop().create_task(coro)
    asyncio.get_event_loop().run_forever()