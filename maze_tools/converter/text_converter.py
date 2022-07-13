from pathlib import Path

from .base_converter import BaseConverter
from ..maze import Maze


class TextConverter(BaseConverter):
    """
    Класс для загрузки/выгрузки лабиринта в текстовом виде.
    """

    def __init__(self, maze: Maze, path_to_file: Path,
                 result_symbol: str) -> None:
        """
        Инициализатор класса.

        :param maze: Объект лабиринта.
        :param path_to_file: Путь до файла.
        """

        self.__path_to_file = path_to_file
        self.__maze = maze
        self.__result_symbol = result_symbol

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

    def load(self) -> Maze:
        ...

    def unload(self) -> None:
        """
        Метод сохранения лабиринта в текстовом виде.
        """

        map = self.__maze.map
        with open(self.__path_to_file, mode='w') as file:
            for _ in range(self.__maze.shape[1]):
                file.write('+----')
            file.write('+\n')
            for i, row in enumerate(map):
                file.write('|')
                for k, cell in enumerate(row):
                    if cell.r_border:
                        file.write(f' {self.__result_symbol if (i, k) in self.__maze.resolve else " "}  |')
                    else:
                        file.write(f'  {self.__result_symbol if (i, k) in self.__maze.resolve else " "}  ')
                file.write('\n+')
                for cell in row:
                    if cell.b_border:
                        file.write('----')
                    else:
                        file.write('    ')
                    file.write('+')
                file.write('\n')
