import asyncio

from mydm.bot import Bot
from mydm.event import Event, EventMessage
from mydm.message import MessageSegmentSend
from mydm.interactor import InteractorWebSocket

itat = InteractorWebSocket('ws://192.168.0.102:8080')
bot = Bot()


@bot.on()
async def print_event(event: 'Event'):
    print(event)


@bot.on(post_type='message', message_type='group')
async def echo(event: 'EventMessage'):
    await itat.call(
        'send_group_msg',
        group_id=event['group_id'],
        message=MessageSegmentSend.at(event.sender.user_id) + event.message
    )


async def main():
    await itat.connect(asyncio.get_event_loop())
    itat.handlers.append(bot)


asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()
