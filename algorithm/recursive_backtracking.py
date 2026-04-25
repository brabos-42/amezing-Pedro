import numpy as np
from enum import Enum
import random
from utils import Cell


class backtracking(Cell):
    def __init__(self, width: int, height: int, path):
        width = (width * 2) + 1
        height = (height * 2) + 1

        self.width = width
        self.height = height
        self.path = path
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
        print("MESH BEFORE\n")
        print(self.maze)
        print("\n")
        self.generate(1, 1, self.maze)
        print("MESH AFTER\n")
        print(self.maze)
        print("\n")
        self.generate_final_maze()

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
                   grid[next_cell_y, next_cell_x] != 0.5):
                    grid[middle_cell_y, middle_cell_x] = 0
                    self.generate(next_cell_x, next_cell_y, grid)

    def is_visited(self, x, y, grid):
        if 0 < y < self.height and 0 < x < self.width:
            return grid[y, x] == 0.5
        return True

    def add_42_maze(self) -> None:
        if (self.maze is not None):
            coord_x = self.width // 2
            coord_y = self.height // 2
            offsets: list[tuple[int, int]] = [
                (-5, -5),
                (-3, -5),
                (-1, -5),
                (-1, -3),
                (-1, -1),
                (1, -1),
                (3, -1),
                (-5, 1),
                (-5, 3),
                (-5, 5),
                (-3, 5),
                (-1, 5),
                (-1, 3),
                (-1, 1),
                (1, 1),
                (3, 1),
                (3, 3),
                (3, 5),
            ]
            for dy, dx in offsets:
                self.maze[coord_y + dy, coord_x + dx] = 2

    def generate_final_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                valor = self.maze[y, x]
                self._cell.set_bit_cell(1, 0, 0, 0, valor)
                self._cell.show_type_cell()


class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
