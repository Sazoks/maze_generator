from pathlib import Path
from typing import (
    Tuple,
)
from PIL import (
    Image,
    ImageDraw,
)

from .base_converter import BaseConverter
from ..maze import Maze
from ..cell import Cell


class ImageConverter(BaseConverter):
    """
    Класс для выгрузки и загрузки лабиринта в виде изображения.
    """

    def __init__(self, maze: Maze, path_to_file: Path, max_size: int,
                 background_color: str, cell_border_color: str,
                 cell_result_color: str) -> None:
        """
        Инициализатор класса.

        :param maze: Лабиринт.
        :param path_to_file: Путь до файла, куда нужно сохранить.
        :param max_size: Максимальный размер изображения.
        :param cell_color: Цвет ячейки.
        :param cell_border_color: Цвет стенки.
        """

        # Путь до файла, куда будет сохранено изображение, и объект лабиринта.
        self.__path_to_file = path_to_file
        self.__maze = maze

        # Объект изображения и объекта для рисования.
        self.__img = Image.new('RGB', (max_size, max_size), color=background_color)
        self.__id_raw = ImageDraw.Draw(self.__img)

        self.__max_size = max_size
        self.__background_color = background_color
        self.__cell_border_color = cell_border_color
        self.__cell_result_color = cell_result_color

        # Выбираем наибольшее значение из высоты и ширины карты.
        max_count_nodes = max(len(maze.map), len(maze.map[0]))
        # Расчитываем размер одной ячейки.
        self.__size_node = (max_size - 1) // max_count_nodes

        # Толщина стенки.
        self.__border_width = self.__size_node // 30

    @property
    def max_size(self) -> int:
        return self.__max_size

    @max_size.setter
    def max_size(self, new_max_size: int) -> None:
        self.__max_size = new_max_size

    @property
    def path_to_file(self) -> Path:
        return self.__path_to_file

    @path_to_file.setter
    def path_to_file(self, new_path: Path) -> None:
        self.__path_to_file = new_path

    @property
    def maze(self) -> Maze:
        return self.__maze

    @maze.setter
    def maze(self, new_maze: Maze) -> None:
        self.__maze = new_maze

    @property
    def background_color(self) -> str:
        return self.__background_color

    @background_color.setter
    def background_color(self, new_color) -> None:
        self.__background_color = new_color

    @property
    def cell_border_color(self) -> str:
        return self.__cell_border_color

    @cell_border_color.setter
    def cell_border_color(self, new_color) -> None:
        self.__cell_border_color = new_color

    def load(self) -> Maze:
        ...

    def unload(self) -> None:
        """
        Метод сохранения лабиринта в изображение.
        """

        map = self.__maze.map

        # Координаты для отрисовки ячейки.
        pos_x, pos_y = 0, 0
        for i in range(len(map)):
            for k in range(len(map[0])):
                self._draw_node((i, k), pos_x, pos_y)
                # Изменяем координаты для следующей ноды после отрисовки
                # текущей.
                pos_x += self.__size_node
            # После конца строк снова меняем координаты для отрисовки.
            pos_x = 0
            pos_y += self.__size_node

        # Сохраняем готовое изображение.
        self.__img.save(self.__path_to_file)

    def _draw_node(self, cords: Tuple[int, int],
                          pos_x: int, pos_y: int) -> None:
        """
        Отрисовка границ узла.

        :param node: Узел лабиринта.
        :param pos_x: Позиция верхнего левого угла по оси X.
        :param pos_y: Позиция верхнего левого угла по оси Y.
        """

        part_size_node = self.__size_node // 1.25
        if cords in self.__maze.resolve:
            self.__id_raw.rectangle(
                xy=(pos_x + part_size_node, pos_y + part_size_node,
                    pos_x + self.__size_node - part_size_node,
                    pos_y + self.__size_node - part_size_node),
                fill=self.__cell_result_color,
            )

        cell: Cell = self.__maze.cords_to_cell(cords)

        # Если есть левая стенка, отрисовываем ее тогда, когда у предыдущей
        # ячейки нет правой стенки или ячейки вообще нет.
        if cell.l_border:
            self.__id_raw.line(
                xy=(pos_x, pos_y, pos_x, pos_y + self.__size_node),
                fill=self.__cell_border_color,
                width=self.__border_width,
            )
        # Если есть правая стенка, отрисовываем ее тогда, когда у следующей
        # ячейки нет левой стенки или ячейки вообще нет.
        if cell.r_border:
            self.__id_raw.line(
                xy=(pos_x + self.__size_node, pos_y,
                    pos_x + self.__size_node, pos_y + self.__size_node),
                fill=self.__cell_border_color,
                width=self.__border_width,
            )
        # Для верхней и нижней стенок поступаем аналогично левым и правым.
        if cell.t_border:
            self.__id_raw.line(
                xy=(pos_x, pos_y,
                    pos_x + self.__size_node, pos_y),
                fill=self.__cell_border_color,
                width=self.__border_width,
            )
        if cell.b_border:
            self.__id_raw.line(
                xy=(pos_x, pos_y + self.__size_node,
                    pos_x + self.__size_node, pos_y + self.__size_node),
                fill=self.__cell_border_color,
                width=self.__border_width,
            )
