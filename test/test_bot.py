import unittest
import asyncio

from mydm.bot import Bot
from mydm.event import Event

base_event = Event({
    'time': 123, 
    'self_id': 114514, 
    'post_type': 'message'
})


class TestBot(unittest.TestCase):
    def test_when_post_type_is_None(self):
        bot = Bot()
        @bot.on()
        async def _(event: 'Event'):
            self.assertEqual(event, base_event)
            return event
        asyncio.run(bot(base_event))
    
    def test_handler_without_async(self):
        bot = Bot()
        @bot.on()
        def _(event: 'Event'):
            self.assertTrue(True)
            return event
        asyncio.run(bot(base_event))
    
    def test_when_handler_no_type_hint(self):
        bot = Bot()
        @bot.on()
        async def _(event):
            self.assertTrue(True)
            return event
        asyncio.run(bot(base_event))
