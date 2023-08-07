from enum import Enum, unique


@unique
class CQcodeType(Enum):
    '''
    - 仅包含go-cqhttp已实现的部分
    - 顺序参考 https://docs.go-cqhttp.org/cqcode/
    '''
    FACE = 'face'
    RECORD = 'record'
    VIDEO = 'video'
    AT = 'at'
    SHARE = 'share'
    MUSIC = 'music'
    IMAGE = 'image'
    REPLY = 'reply'
    REDBAG = 'redbag'
    POKE = 'poke'
    GIFT = 'gift'
    FORWARD = 'forward'
    NODE = 'node'
    XML = 'xml'
    JSON = 'json'
    CARDIMAGE = 'cardimage'
    TTS = 'tts'


class CQcode:
    def __init__(self, type: CQcodeType, data: dict):
        self.type = type
        self.data = data
    
    def __str__(self) -> str:
        data = ''
        for param, value in self.data.items():
            data = f'{param}={value}'
        return f'[CQ:{self.type.value},{data}]'
    
    def __add__(self, other) -> str:
        return self.__str__() + other