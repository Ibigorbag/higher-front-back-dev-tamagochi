"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from functools import wraps
from random import randint
from time import sleep
from typing import Any

from .clicker import AbstractClicker
from .exceptions import GameError, InvalidChoice, NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class Game(AbstractGame):
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        super().__init__(tamagochi, clicker, all_food, all_medicine)
        self._money = 100
        self._food = []
        self._medicine = []

    @staticmethod
    def check_availability(action: str):
        """Декоратор для обработки ошибок невозможности действий."""
        def decorator(func):
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

    def _choose(self, items: list, prompt: str):
        """Метод для реализации интерфейса выбора предмета."""
        if not items:
            raise InvalidChoice('Список пуст')
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
        try:
            idx = int(input(prompt)) - 1
            if 0 <= idx < len(items):
                return items[idx]
        except (ValueError, IndexError):
            raise InvalidChoice('Некорректный выбор')

    @property
    def food(self) -> list[Food]:
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        return self._medicine

    @check_availability('уложить спать')
    def rest_tamagochi(self) -> None:
        self.tamagochi.rest()

    @check_availability('играть')
    def play_with_tamagochi(self) -> None:
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        tamagochi_status = self.tamagochi.status
        return {
            'hunger': tamagochi_status['hunger'],
            'hp': tamagochi_status['hp'],
            'energy': tamagochi_status['energy'],
            'coins': self._money,
            # happiness Не используется в main, но является статусом тамагочи
            'happiness': tamagochi_status['happiness']
        }

    @check_availability('работать')
    def work(self) -> int:
        # Честно говоря, я не очень понял, что от меня нужно
        # в плане реализации кликера, поэтому это скорее заглушка пока.
        for _ in range(randint(1, 10)):
            income = self.clicker.click()

        self._money += income
        self.tamagochi.update()
        return income

    @check_availability('купить еду')
    def buy_food(self) -> None:
        food = self._choose(self.all_food, 'Какую еду купить? ')
        if self._money < food.price:
            raise NotEnoughMoney(
                f'Нужно {food.price} монет, но у вас {self._money}'
            )
        self._money -= food.price
        self._food.append(food)

    @check_availability('купить лекарства')
    def buy_medicine(self) -> None:
        medicine = self._choose(self.all_medicine, 'Какое лекарство купить? ')
        if self._money < medicine.price:
            raise NotEnoughMoney(
                f'Нужно {medicine.price} монет, но у вас {self._money}'
            )
        self._money -= medicine.price
        self._medicine.append(medicine)

    @check_availability('покормить')
    def feed_tamagochi(self) -> None:
        food = self._choose(self._food, 'Чем кормить? ')
        self.tamagochi.feed(food)
        self._food.remove(food)

    @check_availability('лечить')
    def heal_tamagochi(self) -> None:
        medicine = self._choose(self._medicine, 'Чем лечить? ')
        self.tamagochi.heal(medicine)
        medicine.uses += 1
        if medicine.is_empty():
            self._medicine.remove(medicine)
