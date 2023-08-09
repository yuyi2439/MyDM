import asyncio

from mydm.event import Event, EventMessage
from mydm.message import MessageSegmentSend, Message
from mydm.interactor import InteractorWebSocket

interactor = InteractorWebSocket('ws://192.168.0.102:8080')


async def print_event(event: 'Event'):
    print(event)


async def echo(event: 'Event'):
    if event.post_type == 'message':
        event = EventMessage(event)
        if event.message_type == 'group':
            await interactor.call(
                'send_group_msg', group_id=event['group_id'],
                message=Message([
                    MessageSegmentSend.at(event.sender.user_id),
                    event.message
                ])
            )


async def main():
    interactor.handlers.append(print_event)
    interactor.handlers.append(echo)
    await interactor.connect()
    print(await interactor.call('get_login_info'))


asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()
