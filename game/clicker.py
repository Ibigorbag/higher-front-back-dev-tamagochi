"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint

MAX_INCOME = 5
MIN_INCOME = 1


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Класс для реализации кликера."""

    def __init__(self) -> None:
        """Инициализация класса кликера."""
        self._income_per_click = None
        self.min_income = MIN_INCOME
        self.max_income = MAX_INCOME

    @property
    def income_per_click(self) -> int:
        """
        Метод для возврата монет за клик.

        :return: доход за один клик
        """
        return self._income_per_click

    def click(self) -> None:
        """Метод для случайного определения дохода за клик."""
        # Сделаю передачу монет через self,
        # чтобы не нарушать аннотацию из прекода.
        self._income_per_click = randint(self.min_income,
                                         self.max_income)
