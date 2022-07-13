import random
from typing import List
from itertools import groupby

from .base_generator import BaseGenerator
from ..cell import Cell
from ..maze import Maze


class EulerGenerator(BaseGenerator):
    """
    Генератор лабиринта с помощью алгоритма Эйлера.
    """

    def __init__(self) -> None:
        """
        Инициализация генератора параметрами для лабиринта.
        """

        self.__MIN_WIDTH = 2
        self.__MIN_HEIGHT = 2

    @property
    def min_width(self) -> int:
        return self.__MIN_WIDTH

    @min_width.setter
    def min_width(self, new_width: int) -> None:
        self.__MIN_WIDTH = new_width

    @property
    def min_height(self) -> int:
        return self.__MIN_HEIGHT

    @min_height.setter
    def min_height(self, new_height: int) -> None:
        self.__MIN_HEIGHT = new_height

    def generate(self, height: int, width: int) -> Maze:
        """
        Генерация лабиринта.

        :param height: Высота лабиринта.
        :param width: Ширина лабиринта.
        :return: Объект лабиринта.
        """

        # Проверка параметров лабиринта.
        if width < self.__MIN_WIDTH:
            raise ValueError(f'Ширина лабиринта не может быть меньше '
                             f'{self.__MIN_WIDTH}')
        if height < self.__MIN_HEIGHT:
            raise ValueError(f'Высота лабиринта не может быть меньше '
                             f'{self.__MIN_HEIGHT}')

        # Заранее заполняем карту лабиринта ячейками.
        map = [[Cell() for _ in range(width)] for _ in range(height)]
        # Создаем объект лабиринта.
        maze = Maze(map)

        # Присваиваем начальные множества ячейкам в первой строке.
        # Все множества здесь будут уникальными, и каждая ячейка будет
        # единственной в своем множестве.
        first_marks = range(width)
        for i, cell in enumerate(map[0]):
            cell.marker = first_marks[i]
        # Соединяем случайным образом ячейки из разных множеств.
        self._horizontal_connection_cells(map[0])
        self._vertical_connections_cells(map[0])

        # Заполняем все строки между первой и последней.
        prev_row = map[0]
        for i in range(1, height - 1):
            current_row = map[i]
            # В последующих ячейка нам не нужны верхние границы, поэтому
            # удаляем их.
            for cell in current_row:
                cell.t_border = False
            # Ячейки в ряду maze[i] скопируют маркеры из ячеек в ряду
            # maze[i - 1], если у тех есть проход вниз.
            # Остальные ячейки в maze[i] нужно промарикровать новыми
            # уникальными маркерами.
            self._unique_marked_cells(current_row, prev_row)
            # Также соединяем ячейки случайным образом.
            self._horizontal_connection_cells(current_row)
            self._vertical_connections_cells(current_row)
            prev_row = current_row

        # Обрабатываем последнюю строку лабиринта.
        # Обработка этой строки от строк между начальной и последней
        # отличает методом соединения горизонтальных ячеек, а также
        # здесь не нужно убирает нижнии границы ячеек.
        last_row = map[len(map) - 1]
        prev_last_row = map[len(map) - 2]
        self._unique_marked_cells(last_row, prev_last_row)
        self._horizontal_connection_last_cells(last_row)
        for cell in last_row:
            cell.t_border = False

        return maze

    @staticmethod
    def _unique_marked_cells(row: List[Cell], prev_row: List[Cell]) -> None:
        """
        Маркировка строки row уникальными метками с учетом меток
        предыдущего ряда.

        :param row: Маркируемая строка.
        :param prev_row: Предыдущая строка.
        """

        # Копируем марки из ячеек предыдущей строки, где нет нижней границы.
        for i in range(len(row)):
            if not prev_row[i].b_border:
                row[i].marker = prev_row[i].marker

        # Генерируем уникальные марки с учетом тех, что уже есть.
        unique_markers = list(
            set(range(len(row)))
                .difference(set([cell.marker for cell in prev_row
                                 if cell.marker is not None]))
        )

        # Присваиваем уникальные марки оставшимся пустым ячейкам (без марок).
        for cell in row:
            if cell.marker is None:
                cell.marker = unique_markers.pop()

    @staticmethod
    def _horizontal_connection_last_cells(row: List[Cell]) -> None:
        """
        Горизонтальное соединение ячеек последнего ряда.

        Соединяем все ячейки из разных множеств.

        :param row: Обрабатываемая строка.
        """

        for i in range(len(row) - 1):
            # Соединяем все ячейки из разных множеств.
            current_cell = row[i]
            next_cell = row[i + 1]
            if current_cell.marker != next_cell.marker:
                current_cell.r_border = False
                next_cell.l_border = False
                changed_marker = next_cell.marker
                for cell in row:
                    if cell.marker == changed_marker:
                        cell.marker = current_cell.marker

    @staticmethod
    def _horizontal_connection_cells(row: List[Cell]) -> None:
        """
        Горизонтальное соединение ячеек n-ой строки случайным образом.

        :param row: Обрабатываемая строка.
        """

        for i in range(len(row) - 1):
            current_cell = row[i]
            next_cell = row[i + 1]
            # Соединяем ячейки только из разных множеств.
            if current_cell.marker != next_cell.marker:
                # Решаем случайным образом, соединять или нет.
                connect_cells = bool(random.randint(0, 1))
                if connect_cells:
                    current_cell.r_border = False
                    next_cell.l_border = False
                    changed_marker = next_cell.marker
                    # Если соединяем, то меняем марку у всех элементов строки
                    # с маркой, которую заменяем, на марку текущего элемента.
                    # Таким образом мы говорим, что эта ячейка (у которой за
                    # меняем марку) соединена с множеством ячеек множества
                    # текущей ячейки.
                    for cell in row:
                        if cell.marker == changed_marker:
                            cell.marker = current_cell.marker

    @staticmethod
    def _vertical_connections_cells(row: List[Cell]) -> None:
        """
        Вертикальное соединение ячеек строки.

        Для каждого множества делаем хотя бы один проход виз, убирая
        нижнюю границу.

        :param row: Обрабатываемая строка.
        """

        # Группировка ячеек по маркерам. Получаем итератор вида (mark: cells).
        # Создаем для каждого множества ХОТЯ БЫ одну "дырку" снизу.
        for _, grouper in groupby(row, key=lambda cell: cell.marker):
            # Получаем ячейки.
            cells: List[Cell] = list(grouper)
            # Флаг нажен на случай, если случайным образом не была разрушена
            # ни одна стенка снизу.
            has_hole = False
            for cell in cells:
                # Случайным образом решаем, делать "дыру" или нет.
                destroy_bottom_border = bool(random.randint(0, 1))
                if destroy_bottom_border:
                    cell.b_border = False
                    has_hole = True
            # Если дыра вдруг не была сделана для текущего множества, делаем
            # сами одну дырочку.
            if not has_hole:
                random.choice(cells).b_border = False
