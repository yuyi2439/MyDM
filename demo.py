import asyncio

import mydm.cqcode as cc
from mydm.bot import Bot
from mydm.event import Event, EventMessage
from mydm.interactor.aiohttp import InteractorWebSocket

itat = InteractorWebSocket('(WS地址)')  # (WS地址)
bot = Bot()


@bot.on()
async def print_event(event: 'Event'):
    print(event)


@bot.on(post_type='message', message_type='group')
async def echo(event: 'EventMessage'):
    await itat.call(
        'send_group_msg',
        group_id=event['group_id'],
        message=cc.at(event.sender.user_id) + event.message
    )


async def main():
    await itat.connect(asyncio.get_event_loop())
    itat.handlers.append(bot)


asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()
