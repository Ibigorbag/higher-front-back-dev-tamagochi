from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import ParamSpec, TypeVar

from .exceptions import GameError

P = ParamSpec("P")
R = TypeVar("R")


def check_availability(action: str) -> Callable[
                                                [Callable[P, R]],
                                                Callable[P, R | None]]:
    """Декоратор для обработки ошибок невозможности действий."""
    def decorator(func) -> Callable[P, R | None]:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except GameError as e:
                print(f'Нельзя {action}: {e}')
                sleep(3)  # Чтобы можно было успеть прочесть
                return None
        return wrapper
    return decorator
