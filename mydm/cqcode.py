from typing import Literal, Optional
from mydm.message import MessageSegmentSend

__all__ = [
    'text',
    'face',
    'at',
    'reply',
]


# TODO 下面的CQ码构造并没有写全，参考https://docs.go-cqhttp.org/cqcode/

def build(type: str, **data):
    """
    构建MessageSegmentSend
    """
    for k in list(data.keys()):
        if data[k] is None:
            data.pop(k)
        elif isinstance(data[k], int):
            data[k] = str(data[k])
    return MessageSegmentSend({
        'type': type,
        'data': data
    })


def text(text: str):
    """纯文本
    - `text`: 文本
    """
    return build('text', text=text)


def face(id: int):
    """QQ 表情
    - `id`: QQ 表情 ID，参考https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
    """
    return build('face', id=id)


def at(qq: int | Literal['all'], name: Optional[str] = None):
    """@某人
    - `qq`: @的 QQ 号, all 表示全体成员
    - `name`: 当在群中找不到此QQ号的名称时才会生效
    """
    return build('at', qq=qq, name=name)


def reply(
    id: int, *,
    text: Optional[str] = None,
    qq: Optional[int] = None,
    time: Optional[int] = None,
    seq: Optional[int] = None,
):
    """回复
    - `id`: 回复时所引用的消息id, 必须为本群消息
    - `text`: 自定义回复的信息
    - `qq`: 自定义回复时的自定义QQ, 如果使用自定义信息必须指定
    - `time`: 自定义回复时的时间, 格式为Unix时间
    - `seq`: 起始消息序号, 可通过 `get_msg` 获得
    """
    return build('reply', id=id, text=text, qq=qq, time=time, seq=seq)
