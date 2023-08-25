"""
定义所有消息类型
"""

__all__ = [
    'MessageSegment',
    'MessageSegmentReceive',
    'MessageSegmentSend',
    'Message',
]


from typing import Literal
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

    def __add__(self, other) -> 'Message':
        """
        合并Message
        """
        return Message(self, other)

    @property
    def type(self) -> Literal['text', 'face', 'record', 'video', 'at', 'share', 'image', 'reply', 'xml', 'json', 'redbag', 'forward', 'share', 'music', 'poke', 'gift', 'node', 'cardimage', 'tts']:
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
    def build(type: str, **data):  # TODO 下面的CQ码构造并没有写全，参考https://docs.go-cqhttp.org/cqcode/
        """
        构建MessageSegmentSend
        """
        return MessageSegmentSend({
            'type': type,
            'data': data
        })

    @staticmethod
    def text(text: str):
        """纯文本
        - `text`: 文本
        """
        return MessageSegmentSend.build('text', text=text)

    @staticmethod
    def face(id: int):
        """QQ 表情
        - `id`: QQ 表情 ID，参考https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
        """
        return MessageSegmentSend.build('face', id=id)

    @staticmethod
    def at(qq: int | Literal['all'], name: str = ''):
        """@某人
        - `qq`: @的 QQ 号, all 表示全体成员
        - `name`: 当在群中找不到此QQ号的名称时才会生效
        """
        if name == '':
            return MessageSegmentSend.build('at', qq=qq)
        else:
            return MessageSegmentSend.build('at', qq=qq, name=name)


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

    def __add__(self, other):
        """合并Message"""
        return Message(self, other)
