"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .decorators import check_availability
from .exceptions import NotEnoughEnergy, TamagochiIsGone
from .models import Food, Medicine

INITIAL_HP = 80
INITIAL_HUNGER = 20
INITIAL_HAPPINESS = 50
INITIAL_ENERGY = 80

SICKNESS_THRESHOLD = 40
HUNGER_THRESHOLD = 75
HAPPINESS_THRESHOLD = 70

SICKNESS_HP_DRAIN = 10
SICKNESS_HAPPINESS_DRAIN = 5
SICKNESS_ENERGY_DRAIN = 10

HUNGER_HP_DRAIN = 10
HUNGER_HAPPINESS_DRAIN = 5
HUNGER_ENERGY_DRAIN = 5

HAPPINESS_ENERGY_BOOST = 5

HUNGER_ACCUMULATION = 3
ENERGY_DRAIN = 5
HAPPINESS_DRAIN = 5

REST_ENERGY_GAIN = 10
PLAY_HAPPINESS_GAIN = 20


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
    """Интерфейс логики тамагочи."""

    def __init__(self, name: str = 'Tama'):
        """
        Инициализация тамагочи.

        :param name: имя тамагочи
        """
        self._name = name  # Заготовка для возможности называть питомца.
        self._hunger = INITIAL_HUNGER
        self._hp = INITIAL_HP
        self._happiness = INITIAL_HAPPINESS
        self._energy = INITIAL_ENERGY

    @staticmethod
    def _valid_range(value: int, lowest: int = 0, highest: int = 100) -> int:
        """
        Метод для указания границ допустимых значений состояний.

        :param value: значение для валидации
        :param lowest: нижняя граница значения
        :param highest: верхняя граница значения
        :return: значение в диапазоне [lowest, highest]
        """
        return max(lowest, min(highest, value))

    @property
    def name(self) -> str:
        """
        Свойство для доступа к имени тамагочи

        :return: список с имеющимися (купленными) объектами лекарств
        """
        return self._name

    @property
    def hunger(self) -> int:
        """
        Свойство для доступа к текущему уровню голода.

        :return: уровень голода
        """
        return self._hunger

    @hunger.setter
    def hunger(self, value: int) -> None:
        """
        Устанавливает уровень голода с валидацией диапазона.

        :param value: новое значение голода
        """
        self._hunger = self._valid_range(value)

    @property
    def happiness(self) -> int:
        """
        Свойство для доступа к текущему уровню счастья.

        :return: уровень счастья
        """
        return self._happiness

    @happiness.setter
    def happiness(self, value: int) -> None:
        """
        Устанавливает уровень счастья с валидацией диапазона.

        :param value: новое значение счастья
        """
        self._happiness = self._valid_range(value)

    @property
    def energy(self) -> int:
        """
        Свойство для доступа к текущему уровню энергии.

        :return: уровень энергии
        """
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        """
        Устанавливает уровень энергии с валидацией диапазона.

        :param value: новое значение энергии
        """
        self._energy = self._valid_range(value)

    @property
    def hp(self) -> int:
        """
        Свойство для доступа к текущему уровню здоровья.

        :return: уровень здоровья
        """
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """
        Устанавливает уровень здоровья с валидацией диапазона.

        :param value: новое значение здоровья
        """
        self._hp = self._valid_range(value)

    def is_alive(self) -> bool:
        """
        Метод проверяет, жив ли тамагочи.

        :return: ``True``, если здоровье больше нуля, иначе ``False``
        """
        return self._hp > 0

    def check_is_alive(self) -> None:
        """
        Метод проверяет, что тамагочи жив, иначе бросает исключение.

        :raises TamagochiIsGone: если здоровье равно нулю
        """
        if not self.is_alive():
            raise TamagochiIsGone(f'{self.name} умер')

    def is_sick(self) -> bool:
        """
        Метод проверяет, болеет ли тамагочи.

        Питомец считается больным, если здоровье не выше 40.

        :return: ``True``, если здоровье <= 40, иначе ``False``
        """
        return self.hp <= 40

    # Этот декоратор здесь - вынужденная мера из-за update,
    # который напрямую вызывается в main.
    @check_availability('продолжать')
    def update(self) -> None:
        """
        Метод отвечает за тик времени: меняет состояния и проверяет смерть.
        Вызывается после каждого взаимодействия с тамагочи.

        :raises TamagochiIsGone: если тамагочи мёртв (проверка в начале)
        """
        self.check_is_alive()
        if self.is_sick():
            self.energy -= SICKNESS_ENERGY_DRAIN
            self.happiness -= SICKNESS_HAPPINESS_DRAIN
            self.hp -= SICKNESS_HP_DRAIN
        if self.hunger >= HUNGER_THRESHOLD:
            self.hp -= HUNGER_HP_DRAIN
            self.happiness -= HUNGER_HAPPINESS_DRAIN
            self.energy -= HUNGER_ENERGY_DRAIN
        if self.happiness >= HAPPINESS_THRESHOLD:
            # Будем считать, что довольный Тамагочи бодрее.
            self.energy += HAPPINESS_ENERGY_BOOST

        self.hunger += HUNGER_ACCUMULATION
        self.energy -= ENERGY_DRAIN
        self.happiness -= HAPPINESS_DRAIN

    def feed(self, food: Food) -> None:
        """
        Метод кормит тамагочи.

        :param food: объект еды для кормления
        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self.check_is_alive()
        self.hunger -= food.satiety
        self.happiness += food.satiety // 5

    def play(self) -> None:
        """
        Метод для игры с тамагочи.
        Если энергии меньше 5 — игра невозможна.

        :raises TamagochiIsGone: если тамагочи мёртв
        :raises NotEnoughEnergy: если энергии меньше 5
        """
        self.check_is_alive()
        if self.energy >= ENERGY_DRAIN:
            self.happiness += PLAY_HAPPINESS_GAIN
            self.energy -= ENERGY_DRAIN  # На игры уходит больше энергии.
        else:
            raise NotEnoughEnergy(
                    f'{self.name} слишком устал, чтобы играть'
                )

    def rest(self) -> None:
        """
        Метод отвечает за отдых тамагочи.

        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self.check_is_alive()
        if not self.is_sick():
            self.energy += REST_ENERGY_GAIN
        self.energy += REST_ENERGY_GAIN

    def heal(self, medicine: Medicine) -> None:
        """
        Метод Лечит тамагочи.

        :param medicine: лекарство для лечения
        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self.check_is_alive()
        self.hp += medicine.heal_hp
        # Лекарства не слишком вкусные и тамагочи их не любит.
        self.happiness -= HAPPINESS_DRAIN

    @property
    def status(self) -> dict[str, int]:
        """
        Метод возвращает сводка всех характеристик тамагочи.

        :return: словарь с ключами ``hunger``, ``happiness``,
                 ``energy``, ``hp``
        """
        return {
            'hunger': self.hunger,
            'happiness': self.happiness,
            'energy': self.energy,
            'hp': self.hp
            }
