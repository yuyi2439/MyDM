"""
用于放置其余自定义类型
"""

from typing import Literal

from .exceptions import ApiCallFailed, DataFormatError

try:
    import ujson as json
except ImportError:
    import json

__all__ = [
    'ApiResponse',
    'Sender',
    'SenderTemp',
    'SenderGroup',
]


class ApiResponse(dict):
    def __init__(
        self, resp: dict | str
    ):
        super().__init__()
        if isinstance(resp, str):
            resp = json.loads(resp)
        if isinstance(resp, str):
            # Pylance无法识别，只好这样
            raise
        try:
            retcode = resp['retcode']
            if retcode == 0:
                # api调用成功
                self.update(resp['data'])
            elif retcode == 1:
                # api已提交 async 处理
                pass
            else:
                # 操作失败
                raise ApiCallFailed(resp['msg'], resp['wording'])
        except KeyError:
            pass


class Sender(dict):
    def __init__(self, data: dict):
        """
        从dict构建Sender
        """
        super().__init__(data)
        try:
            _ = self.user_id, self.nickname, self.sex, self.age
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def user_id(self) -> int:
        """QQ号"""
        return self['user_id']

    @property
    def nickname(self) -> str:
        """昵称"""
        return self['nickname']

    @property
    def sex(self) -> Literal['male', 'female', 'unknown']:
        """性别"""
        return self['sex']

    @property
    def age(self) -> int:
        """年龄"""
        return self['age']


class SenderTemp(Sender):
    def __init__(self, data: dict):
        """
        从dict构建SenderTemp
        """
        super().__init__(data)
        try:
            _ = self.group_id
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def group_id(self) -> int | None:
        """临时群消息来源群号"""
        return self['group_id']


class SenderGroup(Sender):
    def __init__(self, data: dict):
        """
        从dict构建SenderGroup
        """
        super().__init__(data)
        try:
            _ = self.card, self.area, self.level, self.role, self.title
        except KeyError as e:
            raise DataFormatError(e)

    @property
    def card(self) -> str:
        """群名片/备注"""
        return self['card']

    @property
    def area(self) -> str:
        """地区"""
        return self['area']

    @property
    def level(self) -> str:
        """等级"""
        return self['level']

    @property
    def role(self) -> Literal['owner', 'admin', 'member']:
        """角色"""
        return self['role']

    @property
    def title(self) -> str:
        """头衔"""
        return self['title']
