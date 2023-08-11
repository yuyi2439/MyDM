"""
定义与Bot相关的东西
Bot需要将自己（或某个method）设置为Interactor的handler，一个Bot可以绑定多个Interactor
Bot提供on（及其附属）装饰器，接收优先级，并注册handler
在Bot接收到Event时，按照优先级依次使用handler处理消息，根据handler的参数类型来输入参数
"""


from typing import Any, Callable

from .event import Event
from .exceptions import TruncateEventProcessing


class Bot:
    def __init__(self):
        self.handlers: list[Callable[['Event'], Any]] = []

    def __call__(self, event: 'Event'):
        try:
            for handler in self.handlers:
                handler(event)
        except TruncateEventProcessing:
            pass

    def on(self, priority: int, handler: Callable):
        pass  # TODO
