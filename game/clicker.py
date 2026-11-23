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
        self._total_income = 0

    @property
    def income_per_click(self) -> int:
        return self._income_per_click

    def click(self) -> None:
        print('дзынь!')
        self._total_income += self.income_per_click

    def play(self) -> int:
        """Метод для процесса игры и возврата монет."""
        print(
         'нажмите enter чтобы копать золото'
         'или введите любой символ, чтобы перестать'
        )
        while True:
            if not input():
                self.click()
            else:
                break
        return self._total_income
