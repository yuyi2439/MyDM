import unittest

from mydm.bot import Bot
from mydm.event import Event


class TestBot(unittest.TestCase):
    async def test_when_post_type_is_None(self):
        bot = Bot()
        @bot.on(priority=1)
        def _(event):
            return event
        r = await bot(Event({'msg': 'test'}))
        self.assertTrue(r == Event({'msg': 'test'}))
