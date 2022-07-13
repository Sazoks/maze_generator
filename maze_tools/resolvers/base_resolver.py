from typing import (
    List,
    Tuple,
)
from abc import (
    ABC,
    abstractmethod,
)

from ..maze import Maze


class BaseResolver(ABC):
    """
    Абстрактный класс резолвера лабиринтов.
    """

    @abstractmethod
    def create_path(self, maze: Maze) -> List[Tuple[int, int]]:
        pass
