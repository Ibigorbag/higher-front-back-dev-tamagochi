"""Модуль с исключениями"""


class GameError(Exception):
    """Абстрактное исключение для игровых ситуаций."""


class TamagochiIsGone(GameError):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(GameError):
    """Ошибка когда не хватает монет для покупки."""


class NotEnoughEnergy(GameError):
    """Ошибка когда не хватает энергии для игры с питомцем."""


class NotEnoughUses(GameError):
    """Ошибка когда не хватает использований предмета."""


class InvalidChoice(GameError):
    """Ошибка когда выбран несуществующий вариант."""
