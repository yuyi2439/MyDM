"""
定义与Bot相关的东西
Bot需要将自己（或某个method）设置为Interactor的handler，一个Bot可以绑定多个Interactor
Bot提供on（及其附属）装饰器，接收优先级，并注册handler
在Bot接收到Event时，按照优先级依次使用handler处理消息，根据handler的参数类型来输入参数
"""


from typing import Any, Callable, Literal, get_type_hints

from mydm.type import POST_TYPE
from mydm.utils import event_handler_sort, EventHandler
from mydm.event import Event
from mydm.exceptions import StopEventProcessing

__all__ = [
    'Bot',
]


class Bot:
    def __init__(self):
        self.handlers: list[EventHandler] = []

    async def __call__(self, event: 'Event'):
        """
        根据优先级依次执行处理函数
        """
        sorted_handlers = event_handler_sort(self.handlers)
        try:
            for handler in sorted_handlers:
                if handler.assert_condition(event):
                    await handler(event)
                else:
                    # TODO 这里应该弄一个warn的log
                    pass
        except StopEventProcessing:
            return

    def on(
        self,
        *,
        priority: int = 0,
        post_type: POST_TYPE | list[POST_TYPE] | Literal['all'] = 'all',
        **condition: str | list
    ) -> Callable:
        """注册事件处理函数
        - `priority`: 优先级：正数中，越小优先级越高；0为无优先级，其次执行；负数最后执行；如果优先级冲突，则按照添加顺序执行
        - `post_type`: 上报类型，默认为全部类型
        - `**condition`: 事件满足条件才会触发
        """
        def decorator(func: Callable[['Event'], Any]):
            type_hints = get_type_hints(func)
            if 'return' in type_hints:
                type_hints.pop('return')
            if len(type_hints.items()) != 1:
                raise TypeError('Handler function must have only one arg')
            condition.update({'post_type': post_type})
            self.handlers.append(EventHandler(func, priority=priority, condition=condition))
            return func

        return decorator
