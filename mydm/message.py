"""
定义所有消息类型
"""

__all__ = [
    'MessageSegment',
    'MessageSegmentReceive',
    'MessageSegmentSend',
    'Message',
]


from typing import Iterable, Literal
from .exceptions import DataFormatError


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

    @property
    def type(self) -> Literal['text', 'face', 'record', 'video', 'at', 'share', 'image', 'reply', 'xml', 'json']:
        """消息段类型"""
        return self['type']

    @property
    def data(self) -> dict | None:
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

    @staticmethod
    def build(type: str, **data):
        """
        构建MessageSegmentSend
        """
        return MessageSegmentSend({
            'type': type,
            'data': data
        })

    @staticmethod
    def at(qq: int | Literal['all'], name: str = ''):
        """
        @某人
        - `qq`: @的 QQ 号, all 表示全体成员
        - `name`: 当在群中找不到此QQ号的名称时才会生效
        """
        if name == '':
            return MessageSegmentSend.build('at', qq=qq)
        else:
            return MessageSegmentSend.build('at', qq=qq, name=name)


class Message(list[MessageSegment]):
    def __init__(self, data: Iterable):
        """
        从dict构建MessageSegmentSend
        """
        segments = []
        for segment in data:
            if isinstance(segment, Message):
                segments.extend(segment)
            elif isinstance(segment, MessageSegment):
                segments.append(segment)
            elif isinstance(segment, dict):
                segments.append(MessageSegment(segment))
            else:
                raise TypeError(
                    f'{segment} is not a MessageSegment or Message')
        super().__init__(segments)
