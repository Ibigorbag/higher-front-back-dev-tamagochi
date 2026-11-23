"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod


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
    def __init__(self, income_per_click=1) -> None:
        self._income_per_click = income_per_click
        self._current_income = 0

    @property
    def income_per_click(self) -> int:
        return self._income_per_click

    def click(self) -> int:
        # Странно, что по ТЗ кликер ничего кроме дохода за клик не возвращает.
        # Т.е. это метод для накапливания монет, но у кликера нет метода для
        # возврата накопленных монет, поэтому я это исправил
        self._current_income += self.income_per_click
        return self._current_income
