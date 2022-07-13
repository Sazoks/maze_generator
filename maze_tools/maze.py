from typing import (
    Tuple,
    Optional,
    List,
)
from collections import namedtuple

from .cell import Cell


class Maze:
    """
    Класс лабиринта.
    """

    # Именованный кортеж для хранения координат соседних ячеек.
    AdjacentCords = namedtuple(
        'AdjacentCords',
        ['left_cords', 'right_cords', 'top_cords', 'bottom_cords'],
    )

    def __init__(self, map: List[List[Cell]],
                 start: Optional[Tuple[int, int]] = None,
                 end: Optional[Tuple[int, int]] = None) -> None:
        """
        Инициализатор лабиринта.

        :param map: Карта лабиринта.
        :param start: Начало лабиринта - кортеж с индексами ячейки.
        :param end: Конец лабиринта - кортеж с индексами ячейки.
        """

        self.__map = map
        self.__start = start
        self.__end = end
        self.__resolve: List[Tuple[int, int]] = []

    @property
    def resolve(self) -> List[Tuple[int, int]]:
        return self.__resolve

    @resolve.setter
    def resolve(self, new_resolve) -> None:
        self.__resolve = new_resolve

    @property
    def map(self) -> List[List[Cell]]:
        return self.__map

    @property
    def start(self) -> Optional[Tuple[int, int]]:
        return self.__start

    @start.setter
    def start(self, new_start: Tuple[int, int]) -> None:
        self.__start = new_start

    @property
    def end(self) -> Optional[Tuple[int, int]]:
        return self.__end

    @end.setter
    def end(self, new_end: Tuple[int, int]) -> None:
        self.__end = new_end

    @property
    def shape(self) -> Tuple[int, int]:
        """
        Получение размерности лабиринта.
        :return: Возвращает размерность в виде Tuple[HEIGHT, WIDTH].
        """

        return len(self.__map), len(self.__map[0])

    def get_adjacent_cells(self, current_cell: Tuple[int, int]) -> AdjacentCords:
        """
        Получение координат соседних ячеек относительно текущей.

        :param current_cell: Координаты текущей ячейки.
        :return: Именованный кортеж с координатами соседних ячеек.
        """

        left, right, top, bottom = (-1, -1), (-1, -1), (-1, -1), (-1, -1)

        if current_cell[1] > 0:
            left = (current_cell[0], current_cell[1] - 1)
        if current_cell[1] < len(self.map[0]) - 1:
            right = (current_cell[0], current_cell[1] + 1)
        if current_cell[0] > 0:
            top = (current_cell[0] - 1, current_cell[1])
        if current_cell[0] < len(self.map) - 1:
            bottom = (current_cell[0] + 1, current_cell[1])

        adjacent_cells = self.AdjacentCords(
            left_cords=left,
            right_cords=right,
            top_cords=top,
            bottom_cords=bottom,
        )

        return adjacent_cells

    def cords_to_cell(self, cords: Tuple[int, int]) -> Cell:
        """
        Перевод координат в объект ячейки.

        :param cords: Координаты ячейки.
        :return: Объект ячейки.
        """

        return self.map[cords[0]][cords[1]]
