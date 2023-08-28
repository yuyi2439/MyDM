from typing import Callable, Optional, TYPE_CHECKING, Union

from mydm.utils import event_handler_sort, EventHandler
from mydm.exceptions import StopEventProcessing

if TYPE_CHECKING:
    from mydm.type import POST_TYPE, HANDLER
    from mydm.event import Event

__all__ = [
    'Bot',
]


class Bot:
    def __init__(self):
        self.handlers: list['EventHandler'] = []

    async def __call__(self, event: 'Event') -> None:
        """
        根据优先级依次执行处理函数
        """
        sorted_handlers = event_handler_sort(self.handlers)
        try:
            for handler in sorted_handlers:
                if handler.assert_condition(event):
                    await handler(event)
        except StopEventProcessing:
            return

    def on(
        self,
        *,
        priority: int = 0,
        post_type: Optional[Union['POST_TYPE', list['POST_TYPE']]] = None,
        **condition: str | list
    ) -> Callable:
        """注册事件处理函数
        - `priority`: 优先级：正数中，越小优先级越高；0为无优先级，其次执行；负数最后执行；如果优先级相同，则按照添加顺序执行
        - `post_type`: 上报类型，默认为全部类型
        - `**condition`: 事件满足条件才会触发
        """
        def decorator(func: 'HANDLER'):
            if func.__code__.co_argcount != 1:
                raise TypeError('Handler function must have only one arg')
            if post_type is not None:
                condition.update({'post_type': post_type})
            self.handlers.append(
                EventHandler(func, priority=priority, condition=condition)
            )
            return func

        return decorator
