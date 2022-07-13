from pathlib import Path
from abc import (
    ABC,
    abstractmethod,
)

from ..maze import Maze


class BaseConverter(ABC):
    """
    Абстрактный класс конвертера лабиринта.
    """

    @abstractmethod
    def unload(self) -> None:
        pass

    @abstractmethod
    def load(self) -> Maze:
        pass

    @property
    @abstractmethod
    def maze(self) -> Maze:
        pass

    @property
    @abstractmethod
    def path_to_file(self) -> Path:
        pass
