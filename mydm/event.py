from typing import Literal, TYPE_CHECKING

from mydm.type import Sender
from mydm.message import Message
from mydm.exceptions import DataFormatError

if TYPE_CHECKING:
    from mydm.type import POST_TYPE


__all__ = [
    'Event',
    'EventMessage',
    'EventRequest',
    'EventNotice',
    'EventMeta',
]


class Event(dict):
    """事件"""

    def __init__(self, data: dict):
        """
        从dict构建Event
        """
        super().__init__(data)
        try:
            _ = self.time, self.self_id, self.post_type
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def time(self) -> int:
        """事件发生的unix时间戳"""
        return self['time']

    @property
    def self_id(self) -> int:
        """收到事件的机器人的 QQ 号"""
        return self['self_id']

    @property
    def post_type(self) -> 'POST_TYPE':
        """上报类型"""
        return self['post_type']


class EventMessage(Event):
    """
    消息事件
    """

    def __init__(self, data: dict):
        """
        从dict构建EventMessage
        """
        super().__init__(data)
        try:
            self._message = Message(self['message'])
            self._sender = Sender(self['sender'])
            _ = self.post_type, self.message_type, self.sub_type, self.message_id, self.user_id, self.raw_message, self.font
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def post_type(self) -> Literal['message', 'message_sent']:
        """上报类型"""
        return self['post_type']

    @property
    def message_type(self) -> Literal['private', 'group']:
        """消息类型"""
        return self['message_type']

    @property
    def sub_type(self) -> Literal['friend', 'normal', 'anonymous', 'group_self', 'group', 'notice']:
        """消息子类型"""
        return self['sub_type']

    @property
    def message_id(self) -> int:
        """消息ID"""
        return self['message_id']

    @property
    def user_id(self) -> int:
        """消息发送者的 QQ 号"""
        return self['user_id']

    @property
    def message(self) -> 'Message':
        """消息内容"""
        return self._message

    @property
    def raw_message(self) -> str:
        """原始消息内容"""
        return self['raw_message']

    @property
    def font(self) -> int:
        """字体"""
        return self['font']

    @property
    def sender(self) -> 'Sender':
        """消息发送者"""
        return self._sender


class EventRequest(Event):
    def __init__(self, data: dict):
        """
        从dict构建EventRequest
        """
        super().__init__(data)
        try:
            _ = self.post_type, self.request_type
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def post_type(self) -> Literal['request']:
        """上报类型"""
        return self['post_type']

    @property
    def request_type(self) -> Literal['friend', 'group']:
        """请求类型"""
        return self['request_type']


class EventNotice(Event):
    def __init__(self, data: dict):
        """
        从dict构建EventNotice
        """
        super().__init__(data)
        try:
            _ = self.post_type, self.notice_type
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def post_type(self) -> Literal['request']:
        """上报类型"""
        return self['post_type']

    @property
    def notice_type(self) -> Literal['group_upload', 'group_admin', 'group_decrease', 'group_increase', 'group_ban', 'friend_add', 'group_recall', 'friend_recall', 'group_card', 'offline_file', 'client_status', 'essence', 'notify']:
        """请求类型"""
        return self['notice_type']


class EventMeta(Event):
    def __init__(self, data: dict):
        """
        从dict构建EventMeta
        """
        super().__init__(data)
        try:
            _ = self.meta_event_type
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def meta_event_type(self) -> Literal['lifecycle', 'heartbeat']:
        """元事件类型"""
        return self['meta_event_type']
