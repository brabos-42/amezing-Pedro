import numpy as np
from enum import Enum
import random
from utils import Cell
import sys
sys.setrecursionlimit(100000000)


class MazeGenerator(Cell):
    def __init__(self,
                 width: int,
                 height: int,
                 path: str,
                 display_map: bool,
                 entry: tuple,
                 exit: tuple,
                 perfect: bool):
        width *= 2
        height *= 2
        if (width % 2 == 0):
            width += 1
        if (height % 2 == 0):
            height += 1

        self.width = width
        self.height = height
        self.path = path
        self.display_map = display_map
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self._cell = Cell(1, 1, 1, 1, 1)

    def create_maze(self):
        maze = np.zeros((self.height, self.width), dtype=np.float64)

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 != 1 or j % 2 != 1:
                    maze[i, j] = 1
                if (i == 0 or j == 0
                   or i == self.height - 1 or j == self.width - 1):
                    maze[i, j] = 1
        self.maze = maze
        self.add_42_maze()
        self.generate(1, 1, self.maze)
        if not self._is_valid_position_set(self.entry):
            print("ERROR: Entry position not available")
        if not self._is_valid_position_set(self.exit):
            print("ERROR: Exit position not available")
        if (self.display_map):
            maze_lines = self.generate_final_maze()
            for line in maze_lines:
                print(line)
        else:
            for row in self.generate_hexa_maze():
                print(row, end="")

    def generate(self, coord_x, coord_y, grid):
        grid[coord_y, coord_x] = 0.5
        if (self.is_visited(coord_x, coord_y - 2, grid) and
           self.is_visited(coord_x, coord_y + 2, grid) and
           self.is_visited(coord_x - 2, coord_y, grid) and
           self.is_visited(coord_x + 2, coord_y, grid)):
            pass
        else:
            li = [1, 2, 3, 4]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                if dir == Directions.UP.value:
                    next_cell_x = coord_x
                    middle_cell_x = coord_x
                    next_cell_y = coord_y - 2
                    middle_cell_y = coord_y - 1
                elif dir == Directions.DOWN.value:
                    next_cell_x = coord_x
                    middle_cell_x = coord_x
                    next_cell_y = coord_y + 2
                    middle_cell_y = coord_y + 1
                elif dir == Directions.LEFT.value:
                    next_cell_x = coord_x - 2
                    middle_cell_x = coord_x - 1
                    next_cell_y = coord_y
                    middle_cell_y = coord_y
                elif dir == Directions.RIGHT.value:
                    next_cell_x = coord_x + 2
                    middle_cell_x = coord_x + 1
                    next_cell_y = coord_y
                    middle_cell_y = coord_y
                else:
                    next_cell_x = coord_x
                    middle_cell_x = coord_x
                    next_cell_y = coord_y
                    middle_cell_y = coord_y

                if (0 <= next_cell_x < self.width and
                   0 <= next_cell_y < self.height and
                   grid[next_cell_y, next_cell_x] != 0.5 and
                   grid[next_cell_y, next_cell_x] != 2 and
                   grid[middle_cell_y, middle_cell_x] != 2):
                    grid[middle_cell_y, middle_cell_x] = 0
                    self.generate(next_cell_x, next_cell_y, grid)

    def is_visited(self, x, y, grid):
        if 0 < y < self.height and 0 < x < self.width:
            return grid[y, x] == 0.5 or grid[y, x] == 2
        return True

    def add_42_maze(self) -> None:
        if (self.maze is not None):
            coord_x = self.width // 2
            coord_y = self.height // 2
            offsets: list[tuple[int, int]] = [
                (-5, -5),
                (-4, -5),
                (-3, -5),
                (-2, -5),
                (-1, -5),
                (-1, -4),
                (-1, -3),
                (-1, -2),
                (-1, -1),
                (0, -1),
                (1, -1),
                (2, -1),
                (3, -1),
                (-5, 1),
                (-5, 2),
                (-5, 3),
                (-5, 4),
                (-5, 5),
                (-4, 5),
                (-3, 5),
                (-2, 5),
                (-1, 5),
                (-1, 4),
                (-1, 3),
                (-1, 2),
                (-1, 1),
                (0, 1),
                (1, 1),
                (2, 1),
                (3, 1),
                (3, 2),
                (3, 3),
                (3, 4),
                (3, 5),
            ]
            for dy, dx in offsets:
                self.maze[coord_y + dy, coord_x + dx] = 2

    def generate_final_maze(self):
        final_output = []

        for y in range(self.height):
            line = ""
            for x in range(self.width):
                valor = self.maze[y, x]

                if valor == 1:
                    color = "\033[48;2;237;180;161m"
                elif valor == 2:
                    color = "\033[48;2;118;68;98m"
                elif valor == 0.5:
                    color = "\033[48;2;44;33;55m"
                elif valor == 3:
                    color = "\033[48;2;169;104;104m"
                else:
                    color = "\033[48;2;44;33;55m"
                # color for entry and exit or path idk "\033[48;2;169;104;104m"
                line += f"{color}  \033[0m"  # two spaces + reset

            final_output.append(line)

        return final_output

    def _is_valid_position_set(self, position: tuple[int, int]) -> bool:
        y, x = position
        x = (x * 2) + 1
        y = (y * 2) + 1
        if (y >= 0 and y < self.height - 1 and x >= 0 and x < self.width):
            if (self.maze[y, x] == 2):
                return False
            self.maze[y, x] = 3
            return True
        return False

    def generate_hexa_maze(self):
        final_output = []

        for y in range(self.height):
            line = ""

            for x in range(self.width):
                if x % 2 != 0 and y % 2 != 0:
                    self._cell.set_bit_cell(
                        self.maze[y, x - 1],
                        self.maze[y + 1, x],
                        self.maze[y, x + 1],
                        self.maze[y - 1, x],
                        1
                    )

                    line += self._cell.translate_cell()

            if line != "":
                final_output.append(line + "\n")

        return final_output


class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
