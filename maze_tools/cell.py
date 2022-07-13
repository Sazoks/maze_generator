from typing import (
    Optional,
    Tuple,
)


class Cell:
    """
    Класс ячейки лабиринта.

    Содержит в себе границы ячейки.
    Границы нужны для проверки, можно ли пройти через
    текущую ячейку через определенную границу.
    """

    def __init__(self,
                 l_border: bool = True, t_border: bool = True,
                 r_border: bool = True, b_border: bool = True) -> None:
        """
        Инициализация ячейка лабиринта.

        :param l_border: Левая граница.
        :param t_border: Верхняя граница.
        :param r_border: Правая граница.
        :param b_border: Нижняя граница.
        """

        self.l_border = l_border
        self.t_border = t_border
        self.r_border = r_border
        self.b_border = b_border
        self.marker: Optional[int] = None
        self.heuristic = -1
        self.range = -1
        self.best_cords: Optional[Tuple] = None

    def get_weight(self) -> int:
        return self.heuristic + self.range
