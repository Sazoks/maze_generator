from typing import (
    List,
    Tuple,
)

from .base_resolver import BaseResolver
from ..maze import Maze
from ..cell import Cell


class AStarResolver(BaseResolver):
    """
    Резолвер лабиринтов с помощью алгоритма A*.
    """

    def __init__(self) -> None:
        """Инициализатор класса"""

        # Открытый и закрытый списки.
        # В открытом хранятся ячейки, доступные к переходу.
        # В закрытом - пройденные ячейки, которые больше не участвуют
        # в построении пути.
        self.__open_list: List[Tuple[int, int]] = []
        self.__closed_list: List[Cell] = []

    def create_path(self, maze: Maze) -> List[Tuple[int, int]]:
        """
        Создание маршрута, который будет являться решение лабиринта.

        :param maze: Объекта лабиринта.
        :return: Список координат ячеек, которые входят в решение.
        """

        result_path = []

        # Делаем стартовую ячейку активной.
        active_cords = maze.start
        if active_cords is None:
            raise ValueError('Не существуют стартовой ячейки')

        # Выполняем алгоритм, пока активная ячейка не станет конечной.
        while active_cords != maze.end:
            current_cell = maze.cords_to_cell(active_cords)
            self.__closed_list.append(current_cell)
            # Составляем список доступных ячеек и считаем их вес.
            near_cords = self._calc_near_cells(maze, active_cords)

            # Если количество доступных ячеек, которых нет в закрытом списке,
            # равно 0, значит, мы попали в тупик. В этом случае делаем
            # акитвной ячейку предыдущую лучшую. Для нее будет то же самое,
            # либо она выберет другую ячейку, который нет в закрытом списке.
            if len(near_cords) == 0:
                active_cords = current_cell.best_cords
                continue

            # Добавляем узлы в открытый список.
            self.__open_list.extend(near_cords)

            # Выбираем ячейку с наименьшим весом.
            min_weight_cell_cords = min(
                near_cords,
                key=lambda cord: maze.cords_to_cell(cord).get_weight(),
            )

            # Делаем ячейку с наименьшим весом активным и идем дальше.
            active_cords = min_weight_cell_cords

        # В active_node находится финальная ячейка. Следуем обратно к первой
        # ячейке по лучшим предыдущим нодам и добавляем их в результирующий
        # список.
        while active_cords != maze.start:
            result_path.append(active_cords)
            active_cords = maze.cords_to_cell(active_cords).best_cords

        # Добавим сам старт в маршрут.
        # Список будет содежрать ноды от конца до старта.
        # Каждая нода имеет ссылку на предыдущую "лучшую" ноду, которая
        # приближает от конца к старту (или наоборот).
        result_path.append(maze.start)

        # Очистим списки.
        self.__open_list.clear()
        self.__closed_list.clear()

        return result_path

    def _calc_near_cells(
            self,
            maze: Maze,
            current_cords: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """
        Вычисление координат доступных соседних ячеек.

        :param maze: Объект лабиринта.
        :param current_cords: Координаты текущей ячейки.
        :return: Список координат доступных сосдених ячеек.
        """

        near_nodes = []

        # Текущая и все соседние ячейки.
        current_cell = maze.cords_to_cell(current_cords)
        adj_cords = maze.get_adjacent_cells(current_cords)

        # Берем ячейки, которые доступны из текущей.
        left_cords = adj_cords.left_cords \
            if not current_cell.l_border else None
        right_cords = adj_cords.right_cords \
            if not current_cell.r_border else None
        top_cords = adj_cords.top_cords \
            if not current_cell.t_border else None
        bottom_cords = adj_cords.bottom_cords \
            if not current_cell.b_border else None

        # У соседних ячеек могут быть свои стенки, поэтому добавляем координаты
        # только тех ячеек, у которых стенок между ней и текущей ячейкой нет.
        # Также эта ячейка не должна быть в закрытом списке.
        if left_cords is not None:
            left_cell = maze.cords_to_cell(left_cords)
            if not left_cell.r_border and left_cell not in self.__closed_list:
                # Считаем эврестическое расстояние до финиша лабиринта.
                new_heuristic = self._get_manhattan_range(
                    left_cords,
                    maze.end,
                )
                # Считаем расстояние от элемента, из которого мы можем
                # попасть в текущий.
                new_range = current_cell.range + 1
                # Если новое расстояние ячейки не посчитано - считаем.
                # Или если расстояние ячейки посчитано и оно больше,
                # чем новое - обновляем значения и лучшую ячейку.
                if left_cell.get_weight() < 0 or left_cell.range > new_range:
                    left_cell.range = new_range
                    left_cell.heuristic = new_heuristic
                    left_cell.best_cords = current_cords
                near_nodes.append(left_cords)

        if right_cords is not None:
            right_cell = maze.cords_to_cell(right_cords)
            if not right_cell.l_border and right_cell not in self.__closed_list:
                # Считаем эврестическое расстояние до финиша лабиринта.
                new_heuristic = self._get_manhattan_range(
                    right_cords,
                    maze.end,
                )
                new_range = current_cell.range + 1
                if right_cell.get_weight() < 0 or right_cell.range > new_range:
                    right_cell.range = new_range
                    right_cell.heuristic = new_heuristic
                    right_cell.best_cords = current_cords
                near_nodes.append(right_cords)

        if top_cords is not None:
            top_cell = maze.cords_to_cell(top_cords)
            if not top_cell.b_border and top_cell not in self.__closed_list:
                new_heuristic = self._get_manhattan_range(
                    top_cords,
                    maze.end,
                )
                new_range = current_cell.range + 1
                if top_cell.get_weight() < 0 or top_cell.range > new_range:
                    top_cell.range = new_range
                    top_cell.heuristic = new_heuristic
                    top_cell.best_cords = current_cords
                near_nodes.append(top_cords)

        if bottom_cords is not None:
            bottom_cell = maze.cords_to_cell(bottom_cords)
            if not bottom_cell.t_border and bottom_cell not in self.__closed_list:
                new_heuristic = self._get_manhattan_range(
                    bottom_cords,
                    maze.end,
                )
                new_range = current_cell.range + 1
                if bottom_cell.get_weight() < 0 or bottom_cell.range > new_range:
                    bottom_cell.range = new_range
                    bottom_cell.heuristic = new_heuristic
                    bottom_cell.best_cords = current_cords
                near_nodes.append(bottom_cords)

        return near_nodes

    @staticmethod
    def _get_manhattan_range(
            current_cords: Tuple[int, int],
            end_cords: Tuple[int, int],
    ) -> int:
        """
        Метод Манхеттена для вычисления приближения от ячейки
        к концу лабиринта.

        :param current_cords: Координаты текущей ячейки.
        :param end_cords: Координаты конечной ячейки.
        :return: Расстояние, обозанчающее приближение от одно ячейки к другой.
        """

        horizontal_range = abs(end_cords[1] - current_cords[1])
        vertical_range = abs(end_cords[0] - current_cords[0])
        result_range = horizontal_range + vertical_range

        return result_range


