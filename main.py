from pathlib import Path

from maze_tools.generators.euler_generator import EulerGenerator
from maze_tools.resolvers.astar_resolver import AStarResolver
from maze_tools.converter.image_converter import ImageConverter
from maze_tools.converter.text_converter import TextConverter


def main():
    """Главная функция"""

    WIDTH_MAZE = 100
    HEIGTH_MAZE = 100

    # Генерация лабиринта.
    maze_generator = EulerGenerator()
    maze = maze_generator.generate(HEIGTH_MAZE, WIDTH_MAZE)
    maze.start = (0, 0)
    maze.end = (len(maze.map) - 1, len(maze.map[0]) - 1)

    # Выгрузка лабиринта в изображение.
    image_converter = ImageConverter(
        maze=maze,
        path_to_file=Path('mazes/source_maze_image.png'),
        max_size=700,
        background_color='white',
        cell_border_color='black',
        cell_result_color='green',
    )
    image_converter.unload()
    # Выгрузка лабиринта в текстовый вид.
    text_converter = TextConverter(maze, Path('mazes/source_maze_text.txt'), '#')
    text_converter.unload()

    # Решение лабиринта.
    resolver = AStarResolver()
    maze.resolve = resolver.create_path(maze)

    # Выгрузка лабиринта с решением в изображение.
    image_converter.path_to_file = 'mazes/resolve_maze_image.png'
    image_converter.unload()
    # Выгрузка лабиринта с решением в текстовый вид.
    text_converter.path_to_file = 'mazes/resolve_maze_text.txt'
    text_converter.unload()


if __name__ == '__main__':
    main()
