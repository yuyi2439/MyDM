"""
定义所有消息类型
"""

__all__ = [
    'MessageSegment',
    'MessageSegmentReceive',
    'MessageSegmentSend',
    'Message',
]


from typing import Literal, Optional
from mydm.exceptions import DataFormatError


class MessageSegment(dict):
    def __init__(self, data: dict):
        """
        从dict构建MessageSegment
        """
        super().__init__(data)
        try:
            _ = self.type
        except KeyError as e:
            raise DataFormatError(e)

    def __add__(self, __other) -> 'Message':
        """
        合并Message
        """
        return Message(self, __other)

    def __eq__(self, __value: 'MessageSegment') -> bool:
        return self.type == __value.type and self.data == __value.data

    @property
    def type(self) -> Literal['text', 'face', 'record', 'video', 'at', 'share', 'image', 'reply', 'xml', 'json', 'redbag', 'forward', 'share', 'music', 'poke', 'gift', 'node', 'cardimage', 'tts']:
        """消息段类型"""
        return self['type']

    @property
    def data(self) -> Optional[dict]:
        """数据"""
        return self.get('data')


class MessageSegmentReceive(MessageSegment):
    def __init__(self, data: dict):
        """
        从dict构建MessageSegmentReceive
        """
        super().__init__(data)
        try:
            _ = self.type
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def type(self) -> Literal['text', 'face', 'record', 'video', 'at', 'share', 'image', 'reply', 'xml', 'json', 'redbag', 'forward']:
        """消息段类型"""
        return self['type']


class MessageSegmentSend(MessageSegment):
    def __init__(self, data: dict):
        """
        从dict构建MessageSegmentSend
        """
        super().__init__(data)
        try:
            _ = self.type
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def type(self) -> Literal['text', 'face', 'record', 'video', 'at', 'share', 'image', 'reply', 'xml', 'json', 'share', 'music', 'poke', 'gift', 'node', 'cardimage', 'tts']:
        """消息段类型"""
        return self['type']


class Message(list[MessageSegment]):
    def __init__(self, *data):
        """
        从dict构建Message
        """
        if not data:
            raise DataFormatError('data is empty')
        super().__init__()
        for segment in data:
            if isinstance(segment, Message):
                self.extend(segment)
            elif isinstance(segment, MessageSegment):
                self.append(segment)
            elif isinstance(segment, (list, tuple)):
                self.extend(MessageSegment(s) for s in segment)
            elif isinstance(segment, dict):
                self.append(MessageSegment(segment))
            else:
                raise DataFormatError(f'{segment} is not a MessageSegment or Message')

    def __add__(self, __other):
        """合并Message"""
        return Message(self, __other)
