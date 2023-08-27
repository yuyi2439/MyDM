import unittest

from mydm.cqcode import *
from mydm.message import MessageSegment


class TestCqcode(unittest.TestCase):
    def test_assert_equal(self):
        """测试`MessageSegment`的`__eq__`"""
        self.assertTrue(MessageSegment({'type': 'at', 'data': {'qq': 12345}}) == at(12345))