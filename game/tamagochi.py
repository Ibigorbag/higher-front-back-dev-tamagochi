"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod
from functools import wraps
from time import sleep

from .exceptions import GameError, NotEnoughEnergy, TamagochiIsGone
from .models import Food, Medicine

# Стоит вынести декоратор в отдельный файл, но это не поддерживается
# архитектурой проекта.


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


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class Tamagochi(AbstractTamagochi):

    def __init__(self, name='Tama'):
        self._name = name  # Заготовка для возможности называть питомца.
        self._hunger = 20
        self._hp = 80
        self._happiness = 50
        self._energy = 80

    @staticmethod
    def _valid_range(value: int, lowest: int = 0, highest: int = 100) -> int:
        """Метод для указания границ допустимых значений состояний."""
        return max(lowest, min(highest, value))

    @property
    def name(self) -> str:
        return self._name

    @property
    def hunger(self) -> int:
        return self._hunger

    @hunger.setter
    def hunger(self, value: int) -> None:
        self._hunger = self._valid_range(value)

    @property
    def happiness(self) -> int:
        return self._happiness

    @happiness.setter
    def happiness(self, value: int) -> None:
        self._happiness = self._valid_range(value)

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        self._energy = self._valid_range(value)

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = self._valid_range(value)

    def is_alive(self) -> bool:
        return self._hp > 0

    def check_is_alive(self) -> None:
        if not self.is_alive():
            raise TamagochiIsGone(f'{self.name} умер')

    def is_sick(self) -> bool:
        return self.hp <= 40

    # Этот декоратор здесь - вынужденная мера из-за update,
    # который напрямую вызывается в main.
    @check_availability('продолжать')
    def update(self) -> None:
        self.check_is_alive()
        if self.is_sick():
            self.energy -= 10
            self.happiness -= 5
        if self.hunger >= 75:
            self.hp -= 10
            self.happiness -= 5
            self.energy -= 5
        if self.happiness >= 75:
            # Будем считать, что довольный Тамагочи бодрее.
            self.energy += 3

        self.hunger += 3
        self.energy -= 5
        self.happiness -= 5

    def feed(self, food: Food) -> None:
        self.check_is_alive()
        self.hunger -= food.satiety
        self.happiness += food.satiety // 5

    def play(self) -> None:
        self.check_is_alive()
        if self.energy >= 5:
            self.happiness += 20
            self.energy -= 5  # На игры уходит дополнительная энергия.
        else:
            raise NotEnoughEnergy(
                    f'{self.name} слишком устал, чтобы играть'
                )

    def rest(self) -> None:
        self.check_is_alive()
        if not self.is_sick():
            self.energy += 10
        self.energy += 10

    def heal(self, medicine: Medicine) -> None:
        self.check_is_alive()
        self.hp += medicine.heal_hp
        self.happiness -= 10  # Лекарства не вкусные и тамагочи их не любит.

    @property
    def status(self) -> dict[str, int]:
        return {
            'hunger': self.hunger,
            'happiness': self.happiness,
            'energy': self.energy,
            'hp': self.hp
            }
