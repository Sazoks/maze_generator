from abc import (
    ABC,
    abstractmethod,
)

from ..maze import Maze


class BaseGenerator(ABC):
    """
    Абстрактный класс генератора.
    """

    @abstractmethod
    def generate(self, height: int, width: int) -> Maze:
        pass

    @property
    @abstractmethod
    def min_width(self) -> int:
        pass

    @property
    @abstractmethod
    def min_height(self) -> int:
        pass
