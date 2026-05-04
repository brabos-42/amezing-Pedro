import numpy as np
from enum import Enum
import random
from utils import Cell
import sys
sys.setrecursionlimit(100000000)


class MazeGenerator(Cell):
    """
    Generates and exports a maze using a recursive backtracking algorithm.

    The maze is internally represented as a NumPy grid where:
        1   -> wall
        0   -> carved path
        0.5 -> visited cell during generation
        2   -> protected pattern (i.e., "42" shape)
        3   -> entry/exit
        4   -> reserved (unused here but supported in rendering)

    The class supports:
        - Perfect mazes (single path between any two points)
        - Imperfect mazes (with loops via deformation)
        - Hexadecimal encoding of maze cells
        - Colored terminal visualization
    """
    def __init__(self,
                 width: int,
                 height: int,
                 path: str,
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
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self._cell = Cell(1, 1, 1, 1, 1)


    def create_maze(self):
        """
        Create, generate, validate, and export the maze.

        Steps:
            1. Initialize grid with walls.
            2. Insert special "42" pattern.
            3. Generate maze paths using recursive backtracking.
            4. Optionally deform maze to create loops.
            5. Validate entry and exit positions.
            6. Export hexadecimal representation to file.
            7. Print colored maze to terminal.
        """
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
        if (self.perfect is False):
            self.deform_maze(1, 1, self.maze)
        if not self._is_valid_position_set(self.entry):
            print("ERROR: Entry position not available")
            sys.exit()
        if not self._is_valid_position_set(self.exit):
            print("ERROR: Exit position not available")
            sys.exit()
        maze = self.generate_hexa_maze()
        with open(self.path, "w") as f:
            for row in maze:
                f.write(row)
            f.write("\n")
            x, y = self.entry
            f.write(f"{x},{y}")
            f.write("\n")
            x, y = self.exit
            f.write(f"{x},{y}")
            f.write("\n")
            x, y = self.entry

        maze_lines = self.generate_final_maze("\033[48;2;50;180;180m")
        for line in maze_lines:
            print(line)

    def generate(self, coord_x, coord_y, grid):
        """
        Recursively carve paths in the maze using depth-first search.

        Args:
            coord_x (int): Current x-coordinate.
            coord_y (int): Current y-coordinate.
            grid (np.ndarray): Maze grid.

        Notes:
            - Marks visited cells as 0.5.
            - Randomly explores directions.
        - Removes walls between current and next cell.
        """
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
        """
        Check if a cell has already been visited or is blocked.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            grid (np.ndarray): Maze grid.

        Returns:
            bool: True if cell is visited or out of bounds, False otherwise.
        """
        if 0 < y < self.height and 0 < x < self.width:
            return grid[y, x] == 0.5 or grid[y, x] == 2
        return True

    def add_42_maze(self) -> None:
        """
        Embed a fixed '42' pattern into the maze.

        The pattern is placed at the center of the maze
        and marked with value 2,
        making it unmodifiable during maze generation.
        """
        if (self.maze is not None):
            coord_x = self.width // 2
            coord_y = self.height // 2
            offsets: list[tuple[int, int]] = [
                (-4, -5),
                (-3, -5),
                (-2, -5),
                (-1, -5),
                (0, -5),
                (0, -4),
                (0, -3),
                (0, -2),
                (0, -1),
                (1, -1),
                (2, -1),
                (3, -1),
                (4, -1),
                (-4, 1),
                (-4, 2),
                (-4, 3),
                (-4, 4),
                (-4, 5),
                (-3, 5),
                (-2, 5),
                (-1, 5),
                (0, 5),
                (0, 4),
                (0, 3),
                (0, 2),
                (0, 1),
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 1),
                (4, 2),
                (4, 3),
                (4, 4),
                (4, 5),
            ]
            for dy, dx in offsets:
                self.maze[coord_y + dy, coord_x + dx] = 2

    def generate_final_maze(self, wall_color):
        """
        Convert the maze grid into a colored terminal representation.

        Returns:
            list[str]: List of strings, each representing a colored row.
        """
        final_output = []
        color_wall = wall_color if wall_color else self._cell._color_wall

        for y in range(self.height):
            line = ""
            for x in range(self.width):
                valor = self.maze[y, x]
                if valor == 1:
                    color =  color_wall
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
        """
        Validate and mark a position as entry or exit.

        Args:
            position (tuple[int, int]): Logical (y, x) position.

        Returns:
            bool: True if position is valid and set, False otherwise.

        Notes:
            - Converts logical coordinates to grid coordinates.
            - Marks valid positions with value 3.
            - Rejects positions overlapping protected areas (value 2).
        """
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
        """
        Convert the maze into a hexadecimal string representation.

        Each logical cell is encoded using bitwise wall information.

        Returns:
            list[str]: List of strings representing the maze in hex format.
        """
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

    def deform_maze(self, coord_x, coord_y, grid):
        """
        Modify the maze to introduce loops (non-perfect maze).

        Args:
            coord_x (int): Starting x-coordinate (unused in loop).
            coord_y (int): Starting y-coordinate (unused in loop).
            grid (np.ndarray): Maze grid.

        Notes:
            - Breaks selected walls to create alternative paths.
            - Avoids modifying protected cells (value 2).
        """
        for coord_y in range(self.height - 2):
            for coord_x in range(self.width - 2):
                if (self.maze[coord_y, coord_x] == 1 and not
                   self.maze[coord_y + 1, coord_x + 1] == 2):
                    self.maze[coord_y + 1, coord_x + 1] = 0


class Directions(Enum):
    """
    Enumeration of possible movement directions in the maze.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
